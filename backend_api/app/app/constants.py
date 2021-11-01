import enum


class OrderStatusEnum(enum.Enum):
    active = 1
    completed = 2
    canceled = 3


class OrderTypeEnum(enum.Enum):
    buy = 1
    sell = 2


class ProviderEnum(enum.Enum):
    bearbounty = 1
    google = 2
