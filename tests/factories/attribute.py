import factory
from factory.alchemy import SQLAlchemyOptions
import faker

from app.models.enums import AttributeGroupEnum
from app.models.models import Attribute


# class AttributeFactory(factory.alchemy.SQLAlchemyModelFactory):
#     _options_class = SQLAlchemyOptions
#
#     class Meta:  # type: ignore
#         model = Attribute
#         sqlalchemy_session_mode = "commit"
#
#     value = faker.Faker().random_object_name()
#     attribute_group = faker.Faker().random_choices(
#         elements=[e.value for e in AttributeGroupEnum]
#     )
#     stock_quantity = faker.Faker().random_int(min=0, max=100)
#     price_modifier = faker.Faker().random_int(min=0, max=200)
