from typing import Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, Field

T = TypeVar("T")

class ResponseSchema(BaseModel, Generic[T]):
    message: Optional[str] = "success"
    data: Union[T, List[T]]

    model_config = {
        "from_attributes": True
    }
