import logging
from arcgis.gis import GIS, User

log = logging.getLogger(__name__)


def user_search(gis: GIS, identifier: str) -> User | None:
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
        return results
    elif len(results) == 1:
        return results[0]

    return None
