from marshmallow import fields, Schema, validate


def get_dynamic_schema_from_field_name_and_type(field_name, field_type):
    marshmallow_module = __import__("marshmallow")
    fields_module = getattr(marshmallow_module, "fields")

    dynamic_schema = Schema.from_dict({
        field_name: getattr(fields_module, field_type)()
    })

    return dynamic_schema()
