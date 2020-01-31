import json
from collections import OrderedDict

from django.forms import Media
from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe

from .extras import generate_field_name


class DictionaryWidget(widgets.MultiWidget):
    """
    Renders JSON as a list of inputs
    """

    input_type = 'json'
    help_text = None
    template_name = 'dictionaryfield/row.html'

    def __init__(self, *args, **kwargs):
        # Fields are passed as a parameter
        super(DictionaryWidget, self).__init__([])

    def decompress(self, values):
        if values:
            try:
                v = json.loads(values)
                if isinstance(v, dict):
                    return v
            except Exception:
                return {}

        return {}

    def get_context(self, name, value, attrs=None):
        # value is a list of values, each corresponding to a widget in self.widgets.
        if not isinstance(value, dict):
            value = self.decompress(value)

        child_widgets = OrderedDict()

        for key, field in self.fields.items():
            widget = field.widget
            widget.is_required = field.required and self.is_required

            try:
                item_value = value.get(key)
            except IndexError:
                item_value = None

            widget_name = generate_field_name(name, key)
            # get rid of [] that may come from nested dictionary fields
            widget_id = widget_name.replace("[", "_").replace("]", "")
            widget_attrs = {"id": "id_%s" % widget_id}
            if attrs:
                widget_attrs.update(attrs)
            widget_output = widget.render(widget_name, item_value, widget_attrs)
            child_widgets[key] = {'id': widget_id, 'name': widget_name, 'label': field.label, 'widget': widget_output,
                                  'help_text': field.help_text, 'value': item_value, 'required': widget.is_required}
        return {'widgets': child_widgets}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))

    def value_from_datadict(self, data, files, name):
        """
        Creates dictionary with keys and values from datadictionary iterating through sub-widgets
        """
        res = {}
        for field_name, field in self.fields.items():
            res[field_name] = field.widget.value_from_datadict(data, files, generate_field_name(name, field_name))
        return res

    @property
    def media(self):
        """
        Media for a multiwidget is the combination of all media of the subwidgets
        """
        media = Media()
        for name, field in self.fields.items():
            try:
                media = media + field.widget.media
            except Exception as e:
                pass

        return media

    @property
    def is_hidden(self):
        return False

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ = 'dictionaryfield_' + id_
        return id_


def parse_dict_from_post(name, params):
    filtered_params = dict(
        (key[key.find('[') + 1:key.find(']')], value) for key, value in params.iteritems() if key.count('[')
    )

    return filtered_params
