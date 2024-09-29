from django.db import IntegrityError
from core.models import OTP
import random
import string

def generate_and_save_otps(email, role = None):
    otp =  None
    while True:
            # Generate a random number
            number = random.randint(100000, 999999)
            try:
                # Attempt to create and save a new OTP with the generated number
                otp = OTP(number=number, email=email, role = role)
                otp.save()
                break
            except IntegrityError:
                return False
    return otp.number

def generate_random_password(length=6):
    chars = string.ascii_letters + string.digits + string.punctuation
    
    # Ensure at least one character from each category
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    
    # Fill the rest of the password with random characters
    for _ in range(length - 4):
        password.append(random.choice(chars))
    
    # Shuffle the list to ensure randomness
    random.shuffle(password)
    
    # Join the characters into a single string
    return ''.join(password)
