import argparse
import sys
import logging
from config import load_env

import sys
import os

# Will re-work when installed as pckg
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reports import (
    simple_user_print,
    get_group_details,
    print_group_details,
    export_csv_report,
)

from arcgis_client import gis_connection
from users import user_search
from groups import group_search
from utils import parse_args, format_datetime

log = logging.getLogger(__name__)


def main():
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Establishing source
    if args.agol:
        gis_source = "AGOL"
    if args.portal:
        gis_source = "PORTAL"

    # Setup env
    env = load_env(source=gis_source)
    gis = gis_connection(
        org_url=env.get("url"),
        username=env.get("username"),
        password=env.get("password"),
    )

    if args.search_user:
        user = user_search(gis=gis, identifier=args.search_user)
        if user:
            simple_user_print(user=user)
            # raise NotImplementedError("Portal support coming soon")

    if args.search_group:
        group = group_search(gis=gis, identifier=args.search_group)
        if group:
            group_details = get_group_details(group=group)
            print_group_details(group_details)
            if args.export_csv:
                export_csv_report(group_details)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )
    main()
