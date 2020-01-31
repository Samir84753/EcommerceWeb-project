try:
    import simplejson as json
except ImportError:
    import json

from collections import OrderedDict
import datetime

from django.core.exceptions import ValidationError
from django.forms.forms import pretty_name
from django.forms.utils import ErrorList, flatatt
from django.utils import six
from django.forms import fields
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
try:
    from django.forms.boundfield import UNSET
except ImportError:
    UNSET = object()

from jsonfield import JSONField
from jsonfield.fields import JSONFormFieldBase

from .extras import generate_field_name
from .widgets import DictionaryWidget


class BoundFields(OrderedDict):
    """
    Analogue of django.forms.fields.BoundField that can
    handle dictionary of fields
    """

    def __init__(self, form, name, *args, **kwargs):
        """
        :param form: Parent form
        :param name: Field name
        """
        super(BoundFields, self).__init__(*args, **kwargs)

        self.form = form
        self.name = name
        self.field = form.fields[name]
        self.label = pretty_name(name) if self.field.label is None else self.field.label
        self.help_text = self.field.help_text
        self.html_name = form.add_prefix(name)
        self.html_initial_name = form.add_initial_prefix(name)
        self.extract_errors(form, name)
        self._initial_value = UNSET
        self.update_initial()
        # Convert children to bound fields
        for f_name, field in self.items():
            self[f_name] = field.get_bound_field(form, self.child_name(name, f_name))


    def update_initial(self):
        """
        Convert nested dictionary to a flat hash so bound child fields could
        get access to values. E.g.
        ```
        { "dict_field": { "f1": "1", "f2": "2" }
        ```
        to
        ```
        { "dict_field__f1": "1", "dict_field__f2": "2" }
        """
        initial = self.form.initial.get(self.name)
        if not initial:
            return

        # Convert JSON string to a dictionary
        # https://code.djangoproject.com/ticket/23549
        if isinstance(initial, six.string_types):
            initial = json.loads(initial)

        if not isinstance(initial, dict):
            return  # maybe JSON string was empty

        for k, v in initial.items():
            key = self.child_name(self.name, k)
            self.form.initial[key] = v

    def extract_errors(self, form, name):
        """
        Errors are combined into one in DictionaryFormField.clean()
        Extract them so each child
        :param form Form:
        :param name str: form field name
        """
        fields_errors = self.errors
        if not fields_errors:
            return

        for e in fields_errors.as_data():
            key = e.message[0]
            errors = e.message[1]
            form._errors[self.child_name(name, key)] = ErrorList(errors)

    def __str__(self):
        """
        Renders this field as an HTML widget.
        """
        return self.as_widget()

    @property
    def errors(self):
        return self.form.errors.get(self.name, self.form.error_class())

    @property
    def is_hidden(self):
        return False

    def child_name(self, field_name, child_name):
        return generate_field_name(field_name, child_name)

    def label_tag(self, contents=None, attrs=None, *args, **kwargs):
        """
        Like BoundField's method
        :param contents:
        :param attrs:
        :return:
        """
        attrs = flatatt(attrs) if attrs else ''
        if contents:
            contents = mark_safe('<div class="dict-header">%s</div>' % contents)
        html = format_html('<div{}>{}</div>', attrs, contents)
        return mark_safe(html)

    def css_classes(self, extra_classes=None):
        """
        Just like BoundField's method
        :param extra_classes:
        :return str:
        """
        return ' '.join(set(extra_classes or []))

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """
        Like as_widget() method of BoundField
        Renders the field by rendering the passed widget, adding any HTML
        attributes passed as attrs.  If no widget is specified, then the
        field's default widget will be used.
        """
        if not widget:
            widget = self.field.widget

        if self.field.localize:
            widget.is_localized = True

        attrs = attrs or {}
        if self.field.disabled:
            attrs['disabled'] = True

        if not only_initial:
            name = self.html_name
        else:
            name = self.html_initial_name
        return force_text(widget.render(name, self.value(), attrs=attrs))

    def value(self):
        """
        Returns the value for this BoundField, using the initial value if
        the form is not bound or the data otherwise.
        """
        if not self.form.is_bound:
            data = self.form.initial.get(self.name, self.field.initial)
            if callable(data):
                if self._initial_value is not UNSET:
                    data = self._initial_value
                else:
                    data = data()
                    # If this is an auto-generated default date, nix the
                    # microseconds for standardized handling. See #22502.
                    if (isinstance(data, (datetime.datetime, datetime.time)) and
                            not self.field.widget.supports_microseconds):
                        data = data.replace(microsecond=0)
                    self._initial_value = data
        else:
            data = self.field.bound_data(
                self.data, self.form.initial.get(self.name, self.field.initial)
            )
        return self.field.prepare_value(data)

    @property
    def data(self):
        """
        Returns the data for this BoundField, or None if it wasn't given.
        """
        return self.field.widget.value_from_datadict(self.form.data, self.form.files, self.html_name)


class DictionaryFormField(JSONFormFieldBase, fields.Field):
    """
    Form field
    """

    widget = DictionaryWidget
    default_error_messages = {
        'required': 'Please enter %s'
    }

    def __init__(self, fields, *args, **kwargs):
        self.fields = fields

        # Allow only DictionaryWidget and its subclasses to act as widget
        if 'widget' in kwargs and not (
                    isinstance(kwargs['widget'], DictionaryWidget) or issubclass(kwargs['widget'], DictionaryWidget)):
            kwargs.pop('widget')

        # Django 1.7 passes max_length for some reason
        kwargs.pop('max_length', None)

        super(DictionaryFormField, self).__init__(*args, **kwargs)

        self.widget.fields = self.fields

    def get_bound_field(self, form, field_name):
        """
        Instead of BoundField return special BoundFields that supports dictionary of sub-fields
        :param form Form:
        :param field_name str: field name
        """
        return BoundFields(form, field_name, self.fields)


    def clean(self, value):
        """
        Call .clean of each child and combine exceptions into one
        :param value:
        :return:
        """
        clean_data = {}
        errors_dict = []
        for key, field in self.fields.items():
            try:
                clean_data[key] = field.clean(value.get(key))
            except ValidationError as e:
                # Store tuple of field name and errors
                # so it be easy to figure out what sub-field caused an error
                errors_dict.append((key, e.messages))

        if errors_dict:
            raise ValidationError(errors_dict)

        return clean_data

    def has_changed(self, initial, data):
        # make sure initial is deserialized before comparing
        if isinstance(initial, six.string_types):
            try:
                initial = json.loads(initial)
            except (TypeError, ValueError):
                pass

        return any([
            field.has_changed(initial.get(key), data.get(key))
            for key, field in self.fields.items()
        ])


class DictionaryField(JSONField):
    """
    Model field based on JSONField.
    It's structure predefined by fields param that uses set of corresponding widgets for edit
    """
    form_class = DictionaryFormField

    def __init__(self, *args, **kwargs):
        self.fields = kwargs.pop('fields', ())
        super(DictionaryField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'fields': self.fields,
            'widget': self.form_class.widget
        }
        defaults.update(kwargs)
        field = super(DictionaryField, self).formfield(**defaults)
        field.is_hidden = False
        # we don't this artifact here
        if field.help_text == "Enter valid JSON":
            field.help_text = ""

        return field
