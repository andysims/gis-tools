from arcgis.gis import GIS
import logging


def gis_connection(org_url: str, username: str, password: str) -> GIS | None:
    log = logging.getLogger(__name__)

    try:
        log.info(f"Attempting connection to: {org_url}")
        gis = GIS(org_url, username, password)
        log.info("Connection succeeded")
        return gis
    except Exception as e:
        log.error(f"Unable to connect to {org_url}: {e}")
        return None
