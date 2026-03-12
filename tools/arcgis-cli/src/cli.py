import argparse
import sys
import logging

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="ArcGIS Online / Portal CLI for Admin")

    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--portal", help="Flag searched ArcGIS Enterprise Portal")
    source_group.add_argument("--agol", help="Flag searched ArcGIS Online")

    return parser.parse_args()
