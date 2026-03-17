from arcgis.gis import Group, User
from utils import format_datetime
from pathlib import Path
from collections import OrderedDict
import logging
import pprint

log = logging.getLogger(__name__)


def simple_user_print(user: User):
    if isinstance(user, list):
        for u in user:
            usr_info = get_user_details(user=u)
            user_print_format(usr_info)
    elif user:
        usr_info = get_user_details(user=user)
        user_print_format(usr_info)


def user_print_format(user: dict):
    if not user:
        log.warning("User not provided")
        return

    print(f"\n{user['fullName']}")
    print("=" * len(user['fullName']))

    for k, v in user.items():
        if k != 'fullName':
            print(f"- {k}: {v}")



def get_user_details(user: User) -> dict:
    # pprint.pprint(dict(user), indent=4)

    # user_content = gis.content.search(query='owner:{}'.format(user.username), max_items=10000)
    # content_count = len(user_content)

    user_info = {
        "fullName": user.get('fullName', ''),
        "firstName": user.get('firstName', ''),
        "lastName": user.get('lastName', ''),
        "username": user.get('username', ''),
        "idpUsername": user.get('idpUsername', 'N/A'),
        "email": user.get('email', ''),
        "created": format_datetime(user.get('created', '')),
        "lastLogin": format_datetime(user.get('lastLogin', '')),
        "role": user.get('role', ''),
        "userLicenseTypeId": user.get('userLicenseTypeId', ''),
        "provider": user.get('provider', ''),
        # 'groups': user.get('groups', ''),
        "groupCount": len(user.get('groups', '')),
        "assignedCredits": user.get('assignedCredits', 'N/A'),
        "availableCredits": user.get('availableCredits', 'N/A'),
        "orgID": user.get('orgId', ''),
    }

    ordered_user_info = OrderedDict(user_info)
    # pprint.pprint(user_info, indent=4)
    return ordered_user_info


def simple_group_print(group: Group):
    print(f"{group.title} ({group.id})")
    print(f"\t")


def get_group_details(group: Group) -> dict | None:
    group_members = group.get_members()

    group_owner = group.owner
    group_admins = group_members["admins"]
    group_users = group_members["users"]  # get_users()

    total_users = 1 + len(group_admins) + len(group_users)  # 1 = owner

    item_count = len(group.content(max_items=-1))

    group_info = {
        "title": group.title,
        "id": group.id,
        "member_count": total_users,
        "owner": group_owner,
        "admins": group_admins,
        "users": group_users,
        "created": format_datetime(group.created),
        "items": item_count,
    }

    return group_info


def print_group_details(group: dict):
    print(f"\n{group['title']}")
    print("=" * len(group["title"]))

    print(f"- Group ID: {group["id"]}")
    print(f"- Created: {group["created"]}")
    print(f"- Item/Content Count: {group['items']}")
    print(f"- Members in group: {group['member_count']}")
    
    print("- Owner:")
    print(f"\t- {group["owner"]}")

    group_admins_len = len(group['admins'])
    
    if not group['admins']:
        print("- Admins: None")
    elif group_admins_len == 1:
        print("- Admin:")
        print(f"\t- {group['admins'][0]}")
    elif group_admins_len > 1:
        print("- Admins:")
        for admin in group['admins']:
            print(f"\t- {admin}")

    users_len = len(group['users'])
    if not group['users']:
        print("- Users: None")
    elif users_len == 1:
        print("- User:")
        print(f"\t- {group['users'][0]}")
    elif users_len > 1:
        print(f"- Users:")
        for user in group['users']:
            print(f"\t- {user}")


def export_csv_report(user_info: dict) -> Path:
    pass
