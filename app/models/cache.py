from sqlalchemy import Column, Float, String

from app.database import Base


class CacheEntry(Base):
    __tablename__ = "cache"

    id = Column(String, primary_key=True, index=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    radius = Column(Float, nullable=False)
    geojson_data = Column(String, nullable=False)

