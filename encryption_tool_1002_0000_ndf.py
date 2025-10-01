# 代码生成时间: 2025-10-02 00:00:31
import os
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

"""
This is a Django application that provides an encryption tool for data transmission.
"""

# Check for the required secret key
if not getattr(settings, 'SECRET_KEY', None):
    raise ImproperlyConfigured("You must define a SECRET_KEY in your settings.")
    
# Generate a key for encryption
key = Fernet.generate_key()

# Save the key to a file for persistence
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Load the key from the file
def load_key():
    try:
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        return Fernet.generate_key()

class EncryptionTool:
    """
    A class to handle encryption and decryption of data.
    """
    def __init__(self):
        self.key = load_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, raw_data: str) -> str:
        """
        Encrypt the raw data using the Fernet symmetric encryption.
        :param raw_data: The data to be encrypted.
        :return: The encrypted data in a URL-safe base64-encoded string.
        """
        return self.cipher_suite.encrypt(raw_data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt the encrypted data using the Fernet symmetric encryption.
        :param encrypted_data: The data to be decrypted.
        :return: The decrypted data.
        """
        try:
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            raise ValueError('Invalid encryption key or data corruption.') from e

# Example usage
# encryption_tool = EncryptionTool()
# encrypted_message = encryption_tool.encrypt('Hello, World!')
# decrypted_message = encryption_tool.decrypt(encrypted_message)
# print(decrypted_message)