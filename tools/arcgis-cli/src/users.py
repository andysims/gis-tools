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
        log.info(f"Multiple users found for {identifier}: {len(results)}")
        for user in results:
            print(f"\t- {user.fullName}: {user.email} ({user.username})")
        return results
    elif len(results) == 1:
        log.info(f"User found: {identifier}")
        user = results[0]
        print(f"\t- {user.fullName}: {user.email} ({user.username})")
        return user
