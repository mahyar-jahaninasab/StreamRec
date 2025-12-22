from pydantic import BaseModel, HttpUrl


class DataCollectorConfig(BaseModel):
    type: str
    value: str
    description: str 
    href: HttpUrl 