import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_operation import get_all_users_data, write_all_users_data, find_user, add_user, delete_user, change_rule, get_all_users, get_rule_from_user, set_verification_code, check_verification_code, get_command_from_verification


def test_database_operations():
    test_file = 'test_users_data'

    # Add test users
    with open('test_users_data.txt', 'w') as file:
        file.write("1234567-T100;45611251-M32;59212123-M40;")
    
    assert get_all_users_data(default_name="foo") == []  # File not exist
    assert get_all_users_data(default_name=test_file) == ['1234567-T100', '45611251-M32', '59212123-M40']  # All users data

    users_data = ['123123-T44', '76543210-M35', '571246412-T100']  # Create new data
    assert write_all_users_data(users_data, default_name=test_file) == 0  # Save in file

    with open('test_users_data.txt', 'r') as file:
        assert file.read() == "123123-T44;76543210-M35;571246412-T100;"  # Check if this data is save

    # Search all users
    assert find_user('123123', default_name=test_file) == 0
    assert find_user('76543210', default_name=test_file) == 1
    assert find_user('571246412', default_name=test_file) == 2
    assert find_user('134851', default_name=test_file) == -1  # Do not exist

    assert add_user('9879876', 'T1000', default_name=test_file) == 0  # Add new user
    assert find_user('9879876', default_name=test_file) == 3  # Find him
    assert add_user('9879876', 'M32', default_name=test_file) == -1  # Try to add existed user
    assert get_rule_from_user('9879876', default_name=test_file) == 'T1000'  # Check his rule

    assert change_rule('9879876', 'M32', default_name=test_file) == 0  # Changing rule
    assert find_user('9879876', default_name=test_file) == 3  # Find him
    assert get_rule_from_user('9879876', default_name=test_file) == 'M32'  # Check if rule is correcyt

    assert get_all_users(default_name=test_file) == ['123123', '76543210', '571246412', '9879876']  # Get all users id
    assert delete_user('76543210', default_name=test_file) == 0  # Delete user
    assert delete_user('123611', default_name=test_file) == -1  # Delete not existent user
    assert find_user('123123', default_name=test_file) == 0  # Check if users who left is in correct place
    assert find_user('76543210', default_name=test_file) == -1
    assert find_user('571246412', default_name=test_file) == 1
    assert find_user('9879876', default_name=test_file) == 2

    assert change_rule('123611', 'T9999', default_name=test_file) == -1  # Change rule for non-existed user
    assert get_rule_from_user('123611', default_name=test_file) == ""  # Get rule for non-existed user

    assert get_all_users_data(default_name=test_file) == ['123123-T44', '571246412-T100', '9879876-M32']  # Check all users data after operations
    
    # Verification code operations
    verification_file = 'test_users_verification'

    with open(f'{verification_file}.txt', 'w') as file:
        file.write("")

    assert set_verification_code('2131', '151242', '|ADD|2131|NEXT|M32', default_name=verification_file) == 0

    with open('test_users_verification.txt', 'r') as file:
        assert file.read() == "2131-151242-|ADD|2131|NEXT|M32;"
    assert set_verification_code('2131', '804219', '|REM|2131', default_name=verification_file) == 0  # Add same code again
    with open('test_users_verification.txt', 'r') as file:
        assert file.read() == "2131-804219-|REM|2131;"
    assert set_verification_code('4212', '804219', '|ADD|4212|NEXT|M32', default_name=verification_file) == 0  # Add code for non-existent user

    assert check_verification_code('2131', '151242', default_name=verification_file) == -2  # Check with old code
    assert check_verification_code('2131', '804219', default_name=verification_file) == 0  # Check with new code
    assert check_verification_code('1441', '804219', default_name=verification_file) == -1  # Check with non-existent user
    assert check_verification_code('4212', '804219', default_name=verification_file) == 0  # Check with non-existent user but with code

    assert get_command_from_verification('2131', default_name=verification_file) == '|REM|2131'  # Get command from verification code
    assert get_command_from_verification('4212', default_name=verification_file) == '|ADD|4212|NEXT|M32'  # Get command from verification code for non-existent user
    assert get_command_from_verification('1441', default_name=verification_file) == ''  # Get command from verification code for non-existent user without code
    assert get_command_from_verification('2131', default_name=verification_file) == ''  # Get command from verification code after is been used
    assert get_command_from_verification('4212', default_name=verification_file) == ''  # Get command from verification code after is been used