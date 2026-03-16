import logging
from arcgis.gis import GIS, Group
from utils import format_datetime

log = logging.getLogger(__name__)


def group_search(gis: GIS, identifier: str) -> Group | None:
    """
    Finds a group by either group name or group ID.

    - If identifier is 32 chars, treated as group ID
    - Otherwise, treated as group name

    Returns a single Group object, or None if not found.
    """
    if not identifier:
        log.error("Group identifier not provided")
        return None

    identifier = identifier.strip()

    if len(identifier) == 32 and " " not in identifier:
        results = gis.groups.search(query=f"id:{identifier}", max_groups=10)
    else:
        results = gis.groups.search(query=f"title:{identifier}", max_groups=100)

    if not results:
        log.info(f"No group found for: {identifier}")
        return None

    if len(results) == 1:
        log.info(f"Group found: {results[0].title}")
        return results[0]

    # Multiple results — prompt user to pick
    print(f"\nMultiple groups found for '{identifier}':")
    for i, group in enumerate(results, start=1):
        print(f"  {i}. {group.title} (ID: {group.id})")

    while True:
        choice = input("\nEnter number of group to select (or 'q' to quit): ").strip()
        if choice.lower() == "q":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            selected = results[int(choice) - 1]
            log.info(f"Group: {selected.title}")
            return selected
        print(f"  Invalid choice, enter 1-{len(results)} or 'q'")
