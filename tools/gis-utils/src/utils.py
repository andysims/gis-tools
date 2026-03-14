from pyproj.exceptions import CRSError
from pyproj.crs import CRS
import logging

log = logging.getLogger(__name__)


def validate_epsg(epsg_code: int):
    try:
        print(CRS)
        crs = CRS.from_user_input(epsg_code)
        return crs.is_valid()
    except CRSError:
        log.error(f"Provided an invalid EPSG: {epsg_code}")
        raise ValueError(f"'{epsg_code}' is not a valid EPSG code")
