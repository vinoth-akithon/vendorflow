
purchase_order_items_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "item": {"type": "string"},
            "quantity": {"type": "integer", "minimum": 1}
        },
        "required": ["item", "quantity"],
        "additionalProperties": False
    },
    "minItems": 1,
}
