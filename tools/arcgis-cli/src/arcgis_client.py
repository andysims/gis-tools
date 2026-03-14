from arcgis.gis import GIS
import logging

log = logging.getLogger(__name__)
logging.getLogger("arcgis").setLevel(logging.ERROR)


def gis_connection(org_url: str, username: str, password: str) -> GIS:
    """Connect to ArcGIS (Online or Portal). Raises on failure."""

    try:
        log.info(f"Attempting connection to: {org_url}")
        gis = GIS(
            org_url=org_url,
            username=username,
            password=password,
        )
        log.info(f"Successfully connected as {gis.users.me.username}")
        return gis
    # except Exception as e:
    #     log.error(f"ArcGIS authentication error: {e}")
    #   raise GISConnectionError(f"Failed to connect to {org_url}") from e

    except Exception as e:
        log.error(f"Unexpected error connecting to {org_url}: {e}")
        # raise GISConnectionError(f"Unexpected connection failure to {org_url}") from e
