from enum import Enum, unique


@unique
class FieldType(Enum):
    STRING = "String"
    DATE = "Date"
    DATETIME = "DateTime"
    INTEGER = "Integer"
    FLOAT = "Float"
    BOOLEAN = "Boolean"
    DICTIONARY = "Dictionary"
