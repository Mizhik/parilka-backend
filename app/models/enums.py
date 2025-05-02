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
    CARD = 'card'
    CASH = 'cash'

class Delivery(Enum):
    NOVAPOSHTA = 'novaposhta'
    UKRPOSHTA = 'ukrposhta'
<<<<<<< HEAD
=======

class ConstructorType(str, Enum):
    BANNER = 'banner'
    BUTTON = 'button'
    TEXT = 'text'
    BULLET_POINT = 'bullet_point'

class ConstructorTag(str, Enum):
    TOP_BANNER = "top_banner"
    ACCORDION = "accordion"


class ProductStatus(str, Enum):
    POPULAR = "popular"
    NEW = "new"
    DISCOUNT = "discount"
    NONE = "none"
>>>>>>> origin/feature/add-new-fields-to-product
