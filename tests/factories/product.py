# import factory
# from factory.alchemy import SQLAlchemyOptions
# import faker
#
# from app.models.enums import Status
# from app.models.models import Product
#
#
# class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
#     _options_class = SQLAlchemyOptions
#
#     class Meta:  # type: ignore
#         model = Product
#         sqlalchemy_session_mode = "commit"
#
#     title = faker.Faker().random_company_product()
#     description = faker.Faker().random_letters(length=50)
#     price = faker.Faker().random_int(min=10, max=200)
#     status = faker.Faker().random_choices(elements=[e.value for e in Status])
