from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode
import hashlib
class ECBCipher(object):
    def __init__(self):
        self.key = "27rf7add6j7523ckb9a17m6rt7q69x80"
        self.__cipher = AES.new(self.key.encode(),  AES.MODE_ECB)

    def __pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    def __unpad(self, s):
        return s[:-ord(s[-1:])]

    def encrypted(self, msg):
        try:
            return b64encode(self.__cipher.encrypt(self.__pad(msg).encode())).decode()
        except:
            return None

    def decrypted(self, encode_str):
        try:
            decode_str = self.__unpad(
                self.__cipher.decrypt(b64decode(encode_str))).decode()
            return decode_str if decode_str else None
        except:
            return None


def tokenDecode(token):
    ecbObj = ECBCipher()
    token = ecbObj.decrypted(token)
    if(token == None):
        return token
    else:
        result = {
            "id": token[0:-10],
            "time": int(token[-10:])
        }
        return result

def getMd5(text):
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf8'))
    md5 = hl.hexdigest()
    return str(md5)