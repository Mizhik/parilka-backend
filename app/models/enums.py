from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    WORKER = "worker"


class Status(Enum):
    NEW = "new"
    PAID = "paid"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Payment(Enum):
    CARD = "card"
    CASH = "cash"


class Delivery(Enum):
    NOVAPOSHTA = "novaposhta"
    UKRPOSHTA = "ukrposhta"


class ProductStatus(str, Enum):
    POPULAR = "popular"
    NEW = "new"
    DISCOUNT = "discount"
    NONE = "none"


class AttributeGroupEnum(str, Enum):
    TASTE = "taste"
    VOLUME = "volume"
    COLOR = "color"


class BundleTypeEnum(str, Enum):
    NONE = "none"
    DIY = "diy"
