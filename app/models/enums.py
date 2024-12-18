from enum import Enum


class Role(Enum):
    USER = "user"
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