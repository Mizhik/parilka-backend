#!/usr/bin/env python
import asyncio
import logging
import typer
import faker as faker_
from app.database.db import get_db, sessionmanager
from app.models.base_model import Base
from app.models.enums import AttributeGroupEnum
from app.models.models import Attribute, Image
from app.schemas import manufacturer
from tests.factories.manufacturer import create_manufacturer
from tests.factories.category import create_category
from tests.factories.country import create_country
from tests.factories.product import create_product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

faker = faker_.Faker()
app = typer.Typer()


async def seed_database(
    num_manufacturers: int = 10,
    num_categories: int = 15,
    num_countries: int = 5,
    num_products: int = 15,
):
    async for session in get_db():
        try:
            logger.info(f"Creating {num_manufacturers} manufacturers")
            manufacturers = []

            for _ in range(num_manufacturers):
                manufacturer = await create_manufacturer(session)
                manufacturers.append(manufacturer)

            logger.info(f"Creating {num_categories} categories")
            categories = []
            for _ in range(num_categories):
                category = await create_category(session)
                categories.append(category)

            logger.info(f"Creating {num_countries} countries")
            countries = []
            for _ in range(num_countries):
                country = await create_country(session)
                countries.append(country)

            logger.info(f"Creating {num_products} products")
            for _ in range(num_products):
                await create_product(
                    session,
                    country=faker.random_element(elements=countries),
                    category=faker.random_element(elements=categories),
                    manufacturer=faker.random_element(elements=manufacturers),
                    attributes=[
                        Attribute(  # type: ignore
                            attribute_group=faker.random_element(
                                elements=[v for v in AttributeGroupEnum]
                            ),
                            price_modifier=faker.random_int(min=0, max=100),
                            stock_quantity=faker.random_int(min=0, max=10),
                            value=faker.word(part_of_speech="adjective"),
                            images=[
                                Image(
                                    image_url=faker.random_element(
                                        elements=[
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1741039138/190a1d131c9f48c582a82c52bd300b79_jo6g48.jpg",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1741039142/a70e31c120e060ca511aed51169327c1_vg4wjy.png",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1741039139/cb4399a1ba7388c85cba3ea1286d708f_yynabb.png",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1741039138/c5f6e6bd8a79b780c7da56753f4c7e56_ryvtju.jpg",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1742376294/Vaporesso_Luxe_X_hexxii.jpg",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1742375937/Voopoo_Vmate_Cartridge_wk08m3.jpg",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1742376782/%D0%90%D1%80%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80_Octobar_10ml_Apple_Grape_5mg_%D0%AF%D0%B1%D0%BB%D1%83%D0%BA%D0%BE_%D0%92%D0%B8%D0%BD%D0%BE%D0%B3%D1%80%D0%B0%D0%B4_cfnexe.jpg",
                                            "https://res.cloudinary.com/dq2bpferw/image/upload/v1745226365/%D1%88%D0%B0%D1%88%D0%BB%D1%8B%D0%BA_pvfyyu.jpg",
                                        ]
                                    )
                                )
                                for _ in range(faker.random_int(min=1, max=5))
                            ],
                        )
                        for _ in range(faker.random_int(min=1, max=3))
                    ],
                )

        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding database: {str(e)}")


@app.command()
def seed(
    manufacturers: int = typer.Option(10, help="Number of manufacturers to create"),
    categories: int = typer.Option(15, help="Number of manufacturers to create"),
    countries: int = typer.Option(5, help="Number of manufacturers to create"),
    products: int = typer.Option(15, help="Number of manufacturers to create"),
    clear_db: bool = typer.Option(False, help="Clear database before seeding"),
):
    async def main():
        if clear_db:
            logger.info("Clearing database")
            async for session in get_db():
                conn = await session.connection()
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
                break

        await seed_database(manufacturers, categories, countries, products)

    asyncio.run(main())


if __name__ == "__main__":
    app()
