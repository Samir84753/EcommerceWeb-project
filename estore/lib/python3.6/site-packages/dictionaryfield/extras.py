def generate_field_name(parent_field, child_field):
    """
    :param parent_field str: name of dictionary field itself
    :param child_field str: name of child field
    :return str:
    """
    return "%s__%s" % (parent_field, child_field)
