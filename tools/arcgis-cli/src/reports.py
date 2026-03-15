def simple_user_print(user):
    if isinstance(user, list):
        print(f"Multiple users found:")
        for u in user:
            print(f"  - {u.fullName}: {u.email} ({u.username})")
    elif user:
        print(f"  - {user.fullName}: {user.email} ({user.username})")
    else:
        print("No user found.")
