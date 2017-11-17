from django.contrib.auth.hashers import BasePasswordHasher,MD5PasswordHasher  
from django.contrib.auth.hashers import mask_hash  
import hashlib  
  
class MyMD5PasswordHasher(MD5PasswordHasher):  
    algorithm = "mymd5"
  
    def encode(self, password, salt):  
        assert password is not None  
        hash = hashlib.md5(password).hexdigest() 
        return hash  
  
    def verify(self, password, encoded):  
        encoded_2 = self.encode(password, '')  
        return encoded == encoded_2  
  
    def safe_summary(self, encoded):  
        return OrderedDict([  
                (_('algorithm'), algorithm),  
                (_('salt'), ''),  
                (_('hash'), mask_hash(hash)),  
                ])