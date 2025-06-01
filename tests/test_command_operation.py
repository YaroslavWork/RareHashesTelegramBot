import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command_operation import ping, add_user, remove_user

def test_command_operations():
    test_file = 'test_users_data'

    with open(f'{test_file}.txt', 'w') as file:
        file.write('')

    assert ping([]) == '|PING|errno|NEXT|1'
    assert ping(['213', '123']) == '|PING|errno|NEXT|1'
    assert ping(['123']) == '|PING|123'

    assert add_user([], default_name=test_file) == '|ADD|errno|NEXT|1'
    assert add_user(['123'], default_name=test_file) == '|ADD|errno|NEXT|1'
    assert add_user(['123', 'T22', '123123'], default_name=test_file) == '|ADD|errno|NEXT|1'
    assert add_user(['123', 'T22'], default_name=test_file) == '|ADD|suc'
    assert add_user(['1456', 'M40'], default_name=test_file) == '|ADD|suc'
    assert add_user(['123', 'M33'], default_name=test_file) == '|ADD|errno|NEXT|3'
    assert add_user(['987', 'foo'], default_name=test_file) == '|ADD|errno|NEXT|2'

    assert remove_user([], default_name=test_file) == '|REM|errno|NEXT|1'
    assert remove_user(['4294', '1255912'], default_name=test_file) == '|REM|errno|NEXT|1'
    assert remove_user(['123'], default_name=test_file) == '|REM|suc'
    assert remove_user(['123'], default_name=test_file) == '|REM|errno|NEXT|2'