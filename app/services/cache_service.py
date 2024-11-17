import hashlib

from sqlalchemy.orm import Session

from app.models.cache import CacheEntry


def generate_cache_id(lon: float, lat: float, radius: float) -> str:
    """Генерация уникального идентификатора для кэша из координат и радиуса."""
    raw_string = f"{lon}_{lat}_{radius}"
    return hashlib.md5(raw_string.encode()).hexdigest()


def get_cache_entry(db: Session, cache_id: str):
    return db.query(CacheEntry).filter(CacheEntry.id == cache_id).first()


def save_cache_entry(
        db: Session,
        cache_id: str,
        lon: float,
        lat: float,
        radius: float,
        geojson_data: str
) -> None:
    new_cache_entry = CacheEntry(
        id=cache_id,
        lon=lon,
        lat=lat,
        radius=radius,
        geojson_data=geojson_data
    )
    db.add(new_cache_entry)
    db.commit()
