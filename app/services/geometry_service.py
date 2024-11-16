import asyncio
import geojson
from pyproj import CRS, Transformer
from shapely.geometry import Point, mapping
from shapely.lib import ShapelyError
from shapely.ops import transform
from fastapi import HTTPException


async def process_geometry(lon: float, lat: float, radius: float) -> str:
    await asyncio.sleep(7)
    try:
        proj_wgs84 = CRS("EPSG:4326")
        proj_aeqd = CRS(proj='aeqd', lat_0=lat, lon_0=lon)
        transformer_to_aeqd = Transformer.from_crs(proj_wgs84, proj_aeqd, always_xy=True)
        transformer_to_wgs84 = Transformer.from_crs(proj_aeqd, proj_wgs84, always_xy=True)

        point = Point(lon, lat)
        point_transformed = transform(transformer_to_aeqd.transform, point)
        buffer = point_transformed.buffer(radius)
        buffer_wgs84 = transform(transformer_to_wgs84.transform, buffer)

        geojson_feature = geojson.Feature(geometry=mapping(buffer_wgs84))
        geojson_data = geojson.dumps(geojson_feature)
        return geojson_data
    except ShapelyError:
        raise HTTPException(status_code=400, detail="Ошибка обработки геометрии.")
    except Exception:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")
