from pydantic import BaseModel, Field


class CircleRequest(BaseModel):
    lon: float = Field(ge=-180.0, le=180.0, description="Долгота в градусах")
    lat: float = Field(ge=-90.0, le=90.0, description="Широта в градусах")
    radius: float = Field(gt=0, description="Радиус в метрах")
