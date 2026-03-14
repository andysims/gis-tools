import argparse
import sys
import logging

from config import load_env

log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="ArcGIS Online / Portal CLI for Admin")

    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--portal", action="store_true", help="Flag searched ArcGIS Enterprise Portal"
    )
    source_group.add_argument(
        "--agol", action="store_true", help="Flag searched ArcGIS Online"
    )

    parser.add_argument("--search-user", type=str, help="Search on username or email")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.portal:
        load_env(source="portal")
    elif args.agol:
        load_env(source="agol")


if __name__ == "__main__":
    main()
