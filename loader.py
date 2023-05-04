# Moudle:
#   loader::aes::decrypt
#   loader::Loader::{read,load_source}
# by d13x

from base64 import b64decode
from Crypto.Cipher import AES

class aes:
    def decrypt( crypted_text:str, key:str) -> str:
        chiper_text = b64decode(crypted_text.encode('utf-8'))
        nonce = chiper_text[:16]
        tag = chiper_text[-16:]
        chiper_text = chiper_text[16:-16]

        chiper = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
        text = chiper.decrypt_and_verify(chiper_text, tag)

        return text.decode('utf-8')


class Loader:
    def read(crypted_source_filename='data.bin', decryption_key='') -> str:
        file = open(crypted_source_filename, 'r')

        if not file.readable():
            raise Exception('File %s not readable' % crypted_source_filename)

        return aes.decrypt(file.read(), decryption_key)


    def load_source(source:(str|list), use_other_globals=False, other_globals=None):
        if not use_other_globals:
            global globals
            glob = globals()
        else:
            glob = other_globals

        if type(source) == list:
            for code in source:
                exec(code, glob)
        else:
            exec(source, glob)


if __name__ == '__main__':
    print('Trying to read "_example_payload.bin"')
    print('If you not changed a "_example_payload.bin" the key is "Mrdf4bi9LU4FoE059hS8Dx5579t{fzM3"')
    payload = Loader.read('_example_payload.bin', input('[?] Enter key: '))
    print('Loading(Executing) payload')
    Loader.load_source(payload)