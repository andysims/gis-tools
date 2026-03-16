from arcgis.gis import Group
from utils import format_datetime


def simple_user_print(user):
    if isinstance(user, list):
        print(f"Multiple users found:")
        for u in user:
            print(f"  - {u.fullName}: {u.email} ({u.username})")
    elif user:
        print(f"  - {user.fullName}: {user.email} ({user.username})")
    else:
        print("No user found.")


def simple_group_print(group: Group):
    print(f"{group.title} ({group.id})")
    print(f"\t")


def get_group_details(group: Group) -> dict:
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

    print(f"\t- Group ID: {group["id"]}")
    print(f"\t- Created: {group["created"]}")
    print(f"\t- Item/Content Count: {group['items']}")
    print(f"\t- Members in group: {group['member_count']}")
    
    print(f"\t- Owner:")
    print(f"\t\t- {group["owner"]}")

    group_admins_len = len(group['admins'])
    
    if not group['admins']:
        print(f"\t- Admins: None")
    elif group_admins_len == 1:
        print(f"\t- Admin: {group['admins'][0]}")
    elif group_admins_len > 1:
        print(f"\t- Admins:")
        for admin in group['admins']:
            print(f"\t\t- {admin}")

    users_len = len(group['users'])
    if not group['users']:
        print(f"\t- Users: None")
    elif users_len == 1:
        print(f"\t- User: {group['users'][0]}")
    elif users_len > 1:
        print(f"\t- Users:")
        for user in group['users']:
            print(f"\t\t- {user}")
