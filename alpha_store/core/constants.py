from enum import IntEnum, StrEnum


class ErrorMessages(StrEnum):
    REQUESTED_OBJECT_NOT_FOUND = (
        "Запрашиваемый объект не найден"
    )
    REQUESTED_OBJECT_NOT_FOUND_IN_CART = REQUESTED_OBJECT_NOT_FOUND + " в вашей корзине"


class NumericalValues(IntEnum):
    NAME_MAX_LENGTH = 255
    NAME_TRUNCATE_VALUE = 30
    PRICE_MAX_VALUE = 100000
    PRICE_MIN_VALUE = 0
    ITEM_MIN_QUANTITY_IN_CART = 1
    ITEM_MAX_QUANTITY_IN_CART = 100
