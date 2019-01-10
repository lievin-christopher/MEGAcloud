from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from getpass import getpass
import json
from subprocess import Popen, PIPE

class Compte:
    def __init__(self,compte_json):
        for k, v in compte_json.items():
            setattr(self, k, v)
        self._session = None

    def __repr__(self):
        session_tmp = self._session
        del self._session
        json.dumps(self, default=lambda x: x.__dict__, indent=4)
        tmp_repr = json.dumps(self.__dict__)
        self._session = session_tmp
        return tmp_repr

    def encrypt_passwd(self,passwd=None):
        if passwd == None:
            passwd = SHA256.new(getpass("Enter MasterPassword : ").encode('utf-8')).hexdigest()[:32].encode('utf-8')
        aes = AES.new(passwd,AES.MODE_GCM)
        ciphertext, tag = aes.encrypt_and_digest(self.passwd.encode())
        json_k = [ 'nonce', 'ciphertext', 'tag' ]
        json_v = [ b64encode(x).decode('utf-8') for x in [aes.nonce, ciphertext, tag] ]
        self.passwd = json.dumps(dict(zip(json_k, json_v)))
    
    def decrypt_passwd(self,passwd=None,init=False):
        if passwd == None:
            passwd = SHA256.new(getpass("Enter MasterPassword : ").encode('utf-8')).hexdigest()[:32].encode('utf-8')
        json_k = [ 'nonce', 'ciphertext', 'tag' ]
        if not isinstance(self.passwd, dict):
            self.passwd = json.loads(self.passwd)
        json_v = {k:b64decode(self.passwd[k]) for k in json_k}
        aes = AES.new(passwd,AES.MODE_GCM,nonce=json_v['nonce'])
        tmp_ret = None
        while tmp_ret == None:
            try:
	            tmp_ret = aes.decrypt_and_verify(json_v['ciphertext'], json_v['tag'])
            except Exception:
                if init:
                    raise Exception("Incorrect MasterPassword,failed to init")    
                print("Incorrect MasterPassword")
                passwd = SHA256.new(getpass("Enter MasterPassword : ").encode('utf-8')).hexdigest()[:32].encode('utf-8')
                aes = AES.new(passwd,AES.MODE_GCM,nonce=json_v['nonce'])
        return tmp_ret