from httpx import Response

from app.schemas.response import ResponseSchema


def parse_response(response: Response, schema_type):
    assert response.status_code == 200
    parsed = ResponseSchema[schema_type].model_validate(response.json())
    assert parsed.data is not None
    return parsed.data

