import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.settings import ALGORITHM, SECRET_KEY
from app.schemas.circle_request import CircleRequest
from app.services.auth import validate_token, oauth2_scheme
from app.services.cache_service import generate_cache_id, get_cache_entry, save_cache_entry
from app.services.geometry_service import process_geometry

router = APIRouter()


@router.post("/circle/")
async def get_circle(
    request: CircleRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Отправка запроса на получение геометрии в виде GeoJSON.
    Данные могут браться из кеша, если они существуют.
    Перед запросом необходимо получить токен по URL `/token/`.
    """
    validate_token(token, SECRET_KEY, [ALGORITHM])

    cache_id = generate_cache_id(request.lon, request.lat, request.radius)

    cache_entry = get_cache_entry(db, cache_id)
    if cache_entry:
        return json.loads(cache_entry.geojson_data)

    geojson_data = await process_geometry(request.lon, request.lat, request.radius)
    save_cache_entry(db, cache_id, request.lon, request.lat, request.radius, geojson_data)

    return json.loads(geojson_data)
