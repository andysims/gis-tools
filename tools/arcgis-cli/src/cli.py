import argparse
import sys
import logging
from config import load_env

from arcgis_client import gis_connection
from users import user_search
from utils import parse_args

log = logging.getLogger(__name__)


def main():
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.agol:
        gis_source = "AGOL"
    if args.portal:
        gis_source = "PORTAL"

    if args.search_user:
        if args.agol:
            env = load_env(source=gis_source)
            gis = gis_connection(
                org_url=env.get("url"),
                username=env.get("username"),
                password=env.get("password"),
            )
            user = user_search(gis=gis, identifier=args.search_user)
            if isinstance(user, list):
                print(f"Multiple users found:")
                for u in user:
                    print(f"  - {u.fullName}: {u.email} ({u.username})")
            elif user:
                print(f"  - {user.fullName}: {user.email} ({user.username})")
            else:
                print("No user found.")
        elif args.portal:
            raise NotImplementedError("Portal support coming soon")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )
    main()
