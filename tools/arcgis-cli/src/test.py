# from .utils import to_yyyymmdd
from utils import to_yyyymmdd as yd, format_datetime
from config import load_env
from arcgis_client import gis_connection, search_user
import logging

log = logging.getLogger(__name__)


def gis_users(gis_conn) -> list[dict]:
    users = gis_conn.users.search(max_users=15)

    log.info(f"Users returned: {len(users)}")

    user_list = [build_user_info(user) for user in users]

    return user_list


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )

    logging.getLogger("arcgis").setLevel(logging.ERROR)

    print(yd())

    print(format_datetime(esri_ts=1636006161232))

    my_env = load_env(source="agol")  # this would be passed in as args
    gis_conn = gis_connection(
        my_env.get("url"), my_env.get("username"), my_env.get("password")
    )

    t = search_user(gis=gis_conn, identifier="test")
    print(t)
