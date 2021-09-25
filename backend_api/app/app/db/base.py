# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.exchange import Exchange  # noqa
from app.models.user_exchange import UserExchange  # noqa
from app.models.dca_bot import DCABot  # noqa
from app.models.order import Order  # noqa
