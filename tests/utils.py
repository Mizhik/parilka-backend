from typing import Awaitable, Callable, Iterable, List, TypeVar
from httpx import Response

from app.schemas.response import ResponseSchema


def parse_response(response: Response, schema_type):
    assert response.status_code == 200
    parsed = ResponseSchema[schema_type].model_validate(response.json())
    assert parsed.data is not None
    return parsed.data

T = TypeVar("T")
R = TypeVar("R")
def bulk_creator(factory: Callable[[], Awaitable[T]]) -> Callable[[int], Awaitable[List[T]]]:
    async def _create_many(count: int = 2) -> List[T]:
        return [await factory() for _ in range(count)]
    return _create_many

def bulk_creator_with_args(
        factory: Callable[[T], Awaitable[R]],
) -> Callable[[Iterable[T]], Awaitable[List[R]]]:
    async def _create_many(inputs: Iterable[T]) -> List[R]:
        results = []
        for item in inputs:
            result = await factory(item)
            results.append(result)
        return results
    return _create_many
