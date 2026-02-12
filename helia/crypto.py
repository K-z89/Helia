from cryptography.fernet import Fernet

class Crypto:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode())

    def decrypt(self, token):
        try:
            return self.cipher.decrypt(token).decode()
        except:
            return "[decrypt failed]"

    def get_key(self):
        return self.key.decode()
