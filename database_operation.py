from notification import log

def get_all_users_data(default_name: str = 'users_data') -> list[str]:
    try:
        with open(f'{default_name}.txt', 'r') as file:
            return [uid for uid in file.read().strip().split(';') if uid]
    except FileNotFoundError:
        log("Database Operation (get_all_users_data)", f"File {default_name}.txt does not exist.")
        return []
    

def write_all_users_data(users_data: list[str], default_name: str = 'users_data') -> int:
    with open(f'{default_name}.txt', 'w') as file: 
        for i in range(len(users_data)):
            file.write(f'{users_data[i]};')
        return 0


def find_user(user_id: str, default_name: str = 'users_data') -> int:
    users_data = get_all_users_data(default_name)

    users_ids = [user_data.split('-')[0] for user_data in users_data]
    for i in range(len(users_data)):
        if user_id == users_ids[i]:
            return i
    return -1


def add_user(user_id, user_rule, default_name: str = 'users_data') -> int:
    user_index = find_user(user_id, default_name)
    if user_index == -1:
        with open(f'{default_name}.txt', 'a') as file:
            file.write(f'{user_id}-{user_rule};')
        return 0
    log("Database Operation (add_user)", f"User with id {user_id} is already in database.")
    return -1
        
    
def delete_user(user_id: str, default_name: str = 'users_data') -> int:
    users_data = get_all_users_data(default_name)

    user_index = find_user(user_id, default_name)
    if user_index != -1:
        del users_data[user_index]

        return write_all_users_data(users_data, default_name)
    log("Database Operation (delete_user)", f"User with id {user_id} does not exist.")
    return -1


def change_rule(user_id, user_rule, default_name: str = 'users_data') -> int:
    users_data = get_all_users_data(default_name)

    user_index = find_user(user_id, default_name)
    if user_index != -1:
        users_data[user_index] = f'{user_id}-{user_rule}'
        
        return write_all_users_data(users_data, default_name)
    log("Database Operation (change_rule)", f"User with id {user_id} does not exist.")
    return -1


def get_all_users(default_name: str = 'users_data') -> list[str]:
    users_data = get_all_users_data(default_name)

    return [user_data.split('-')[0] for user_data in users_data]


def get_rule_from_user(user_id: str, default_name: str = 'users_data') -> str:
    users_data = get_all_users_data(default_name)

    user_index = find_user(user_id, default_name)
    if user_index != -1:
        return users_data[user_index].split('-')[1]
    log("Database Operation (get_rule_from_user)", f"User with id {user_id} does not exist.")
    return ""
    
