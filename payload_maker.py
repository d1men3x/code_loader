# Module:
#   payload_maker::aes::{gen_key,encrypt}
#   payload_maker::Payload::make
# by d13x

from base64 import b64encode
from Crypto.Cipher import AES
from random import randint, choice

class aes:
    def gen_key() -> str:
            key = ''
            for _count in range(32):
                for _random_count in range(randint(1,99)):
                    n = choice( [randint(48,58),randint(97,123),randint(65,91)] )
                key += chr(n)
            return key


    def encrypt( text:str, key:str ) -> str:
        chiper = AES.new(key.encode('utf-8'), AES.MODE_EAX)
        chiper_text, tag = chiper.encrypt_and_digest(text.encode('utf-8'))
        nonce = chiper.nonce
        
        return b64encode(nonce + chiper_text + tag).decode('utf-8')


class Payload:
    def make(source_filename:str, encryption_key:str='', return_enycryption_key=False) -> (str or (str,str)):
        if encryption_key == '':
            return_enycryption_key = True
            encryption_key = aes.gen_key()

        source = open(source_filename, 'r')

        if not source.readable():
            raise Exception('File %s not readable' % source_filename)
        
        encrypted_source = aes.encrypt(source.read(), encryption_key)

        if return_enycryption_key:
            return (encrypted_source, encryption_key)
        return encrypted_source


if __name__ == '__main__':
    print('Generating payload of "_example_source.py"')
    payload, key = Payload.make('_example_source.py')
    payload_file = open('_example_payload.bin','w')
    payload_file.write(payload); payload_file.close()
    print('Encrypted payload placed to "_example_payload.bin"\nYour encryption key: %s' % key)