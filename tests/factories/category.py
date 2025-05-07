import factory
from factory.alchemy import SQLAlchemyOptions
import faker

from app.models.enums import Status
from app.models.models import Category


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    _options_class = SQLAlchemyOptions

    class Meta:  # type: ignore
        model = Category
        sqlalchemy_session_mode = "commit"

    title = faker.Faker().random_company_adjective()
