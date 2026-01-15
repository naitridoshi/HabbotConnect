from libs.utils.common.type_helpers.src.constants import Boolean


def convert_custom_boolean_to_bool(boolean: Boolean | bool):
    if isinstance(boolean, Boolean):
        return boolean == Boolean.TRUE or boolean == Boolean.true
    else:
        return boolean
