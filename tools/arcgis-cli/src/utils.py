# utils.py
# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
utils.py is used for simple and frequent functions/conversions ran

Example:
    >>> from gis_tools.utils import format_datetime
    >>> format_datetime(in_dt=user['lastModified'], fmt_type="short")
    >>>  2026-01-01 9:45
"""

from datetime import datetime
import logging
import argparse


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

    parser.add_argument("--search-group", help="Seach on group name or id")

    parser.add_argument(
        "--export-csv", action="store_true", help="Export list[dict] to CSV"
    )

    return parser.parse_args()


def format_datetime(esri_ts: float | int, fmt_type: str = None) -> str:
    log = logging.getLogger(__name__)

    try:
        if (
            esri_ts > 1_000_000_000_000
        ):  # rough check: > year ~30,000 if treated as seconds
            seconds = esri_ts / 1000.0
        else:
            seconds = float(esri_ts)
            log.warning(
                "Timestamp looks like seconds, not milliseconds – possible misuse?"
            )

        dt = datetime.fromtimestamp(seconds)
        fmt_type = fmt_type.lower().strip() if fmt_type else None

        # Formats to be returned in
        if fmt_type == "short":
            return dt.strftime("%Y-%m-%d %H:%M")
        elif fmt_type == "iso":
            return dt.isoformat()
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S %p")

    except Exception as e:
        log.error(f"Failed to format timestamp {esri_ts}: {e}")
        return "Invalid date"


def to_yyyymmdd(dt: datetime | None = None) -> str:
    log = logging.getLogger(__name__)
    fallback = datetime.now().strftime("%Y%m%d")

    if not isinstance(dt, datetime):
        if dt is not None:
            log.warning(f"Invalid type for date: {type(dt)} → using {fallback}")
        return fallback

    if dt > datetime.now():
        log.warning(f"Future date {dt} provided → using {fallback}")
        return fallback

    return dt.strftime("%Y%m%d")


if __name__ == "__main__":
    # format_datetime(esri_ts, fmt_type)
    print(format_datetime(esri_ts=1263404798000))
    print(format_datetime(esri_ts=1263404798000, fmt_type="short"))
    print(format_datetime(esri_ts=1263404798000, fmt_type="iso"))

    print()

    # format_runtime(in_dt)
    print(to_yyyymmdd())
    print(to_yyyymmdd(dt=datetime(2026, 10, 12, 14, 30)))
    print(to_yyyymmdd(dt=datetime(2025, 10, 12, 14, 30)))
