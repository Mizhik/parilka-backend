# import factory
# from factory.alchemy import SQLAlchemyOptions
# import faker
#
# from app.models.models import Image
#
#
# class ImageFactory(factory.alchemy.SQLAlchemyModelFactory):
#     _options_class = SQLAlchemyOptions
#
#     class Meta:  # type: ignore
#         model = Image
#         sqlalchemy_session_mode = "commit"
#
#     image_url = faker.Faker().random_letters(length=200)
