import random
import string

def generate_random_code(length: int = 6) -> str:
    """
    Generate a random numeric code of specified length.

    Args:
        length (int): The length of the code to be generated. Default is 6.

    Returns:
        str: A string containing a random numeric code of the specified length.
    """
    
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))