import logging
from arcgis.gis import GIS, User

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


def search_user(gis: GIS, identifier: str) -> User | None:
    """
    Finds user by either username OR email.

    - If identifier contains '@', then email
    - Otherwise, treated as username

    Returns the User object if found, or None if not found.
    """
    if not identifier:
        log.error("User identifier not provided")
        return None

    identifier = identifier.lower().strip()

    if "@" in identifier:
        results = gis.users.search(query=f"email:{identifier}", max_users=100)
    else:
        results = gis.users.search(query=f"{identifier}", max_users=100)

    if len(results) > 1:
        log.info(f"Multiple users found for {identifier}: {len(results)}")
        for user in results:
            print(user.fullName, user.email)
        return results
    else:
        log.info(f"User found for: {identifier}")
        return gis.users.get(identifier)
