import secrets
import string

def generate_unique_random_string(length=6, existing_strings=None):
    alphabet = string.ascii_letters + string.digits  # Use letters and digits for randomness
    while True:
        # Generate a random string of the specified length
        random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        # Check if the generated string is unique
        if existing_strings is None or random_string not in existing_strings:
            return random_string