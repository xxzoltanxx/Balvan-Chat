import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Constants import *
import json

class EncryptorService:
    def __init__(self, password, salt):
        encoded_salt = salt.encode('utf-8')
        self._kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=encoded_salt,
            iterations=PBKDF_ITERATIONS,
        )
        key = base64.urlsafe_b64encode(self._kdf.derive(password.encode('utf-8')))
        self._fernet = Fernet(key)
        

    #return bytearray
    def encrypt(self, msg):
        data = self._fernet.encrypt(json.dumps(msg).encode('utf-8'))
        return data
    
    #return json
    def decrypt(self, data):
        decrypted = self._fernet.decrypt(data)
        stringJson = decrypted.decode('utf-8')
        return json.loads(stringJson)