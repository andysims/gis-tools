import logging
from pathlib import Path
import pandas as pd
from pyproj import Transformer
from utils import validate_epsg

log = logging.getLogger(__name__)


def re_project_columns(in_file: Path, in_epsg: int, out_epsg: int) -> Path | None:
    in_file = Path(in_file)

    log.info(f"Starting re-project tool on {in_file.name}")

    # Some defensive scripting
    if not in_file.exists():
        log.error(f"Provided path does not exist: {in_file}")
    if not in_file.is_file():
        log.error("Tool expects a file to be passed, not a dir")
        return None
    # Will extend, but for now, just pulls csv
    if in_file.suffix.lower() != ".csv":
        log.error(f"CSV file is expected, not {in_file.suffix().lower()}")

    # Attempt to re-project
    try:
        # Validation of in/out epsg
        validate_epsg(in_epsg)
        validate_epsg(out_epsg)

        log.info("Reading file into pandas df")
        df = pd.read_csv(f"{in_file}")
        log.info(f"Rows read: {len(df)}")

        df_cols_lower = [col.lower().strip() for col in df.columns]
        x_candidates = ["x", "longitude", "lat"]
        y_candidates = ["y", "latitude", "lat"]

        # Find original column names for X and Y
        x_col = next((col for col in df.columns if col.lower() in x_candidates), None)
        y_col = next((col for col in df.columns if col.lower() in y_candidates), None)

        if x_col is None or y_col is None:
            log.error("Missing one of three combos: X/Y, Lon/Lat, Longitude/Latitude")
            raise ValueError(
                "CSV must contain either 'X'/'Y', 'LONGITUDE'/'LATITUDE', or 'LON'/'LAT' columns"
            )

        # Log the chosen column names
        log.info(f"x column: {x_col}, y column: {y_col}")

        # Check if the columns exist in the DataFrame
        if x_col not in df.columns or y_col not in df.columns:
            raise KeyError(
                f"Columns '{x_col}' or '{y_col}' do not exist in the DataFrame."
            )

        # Create transformer from EPSG:2229 to EPSG:4326
        log.info(f"Converting EPSG: {in_epsg} to EPSG: {out_epsg}")
        transformer = Transformer.from_crs(
            f"EPSG:{in_epsg}", f"EPSG:{out_epsg}", always_xy=True
        )

        # Transform coordinates
        df[f"longitude_{out_epsg}"], df[f"latitude_{out_epsg}"] = transformer.transform(
            df[x_col].astype(float).values, df[y_col].astype(float).values
        )

        # Replace NaN with empty strings and save to CSV
        out_file = in_file.parent / f"{in_file.stem}_converted.csv"
        df.fillna("").to_csv(f"{out_file}", index=False)
        log.info(f"Out file: {out_file}")
    except Exception as e:
        log.error(e)
