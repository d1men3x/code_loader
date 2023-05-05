#!/ust/bin/python3
# Interactive Moudle:
#   loader::aes::decrypt
#   loader::Loader::{read,load_source}
# by d13x

from sys import argv
from marshal import loads
from base64 import b64decode
from Crypto.Cipher import AES

class aes:
    '''Class for working with AES encryption'''
    def decrypt( crypted_text:str, key:str) -> bytes:
        '''
        this function decrypt `crypted_text` with `key`

        Arguments
        =========
        crypted_text : str
            text crypted by AES encryption

        key : str
            32 bytes key for decrypting `crypted_text`


        Return
        ======
        return : bytes
            Decrypted text in bytes

        Exceptions
        ==========
        Any exceptions may caused by:
        - Invalid key
        - Invalid encrypted source

        '''
        chiper_text = b64decode(crypted_text.encode('utf-8'))
        nonce = chiper_text[:16]
        tag = chiper_text[-16:]
        chiper_text = chiper_text[16:-16]

        chiper = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
        text = chiper.decrypt_and_verify(chiper_text, tag)

        return text


class Loader:
    '''Class for working with encrypted by AES source'''
    def read(crypted_source_filename:str='data.bin', decryption_key:str=''):
        '''
        this function read encrypted byte-code file and decrypt it

        Arguments
        =========
        crypted_source_filename : str = 'data.bin'
            Filename of crypted byte-code file

        decryption_key : str = ''
            Key for decryption crypted byte-code

        Return
        ======
        return : code
            Byte-code for executing via `exec()`

        Exceptions
        ==========
        FileNotFoundError
            Standart error (unhandled)
        Exception("File %s not readable")
            Can't read file by standart function, try to check file rights
        '''
        file = open(crypted_source_filename, 'r')

        if not file.readable():
            raise Exception('File %s not readable' % crypted_source_filename)

        return loads( aes.decrypt(file.read(), decryption_key) )


    def load_source(compiled_source, use_other_globals:bool=False, other_globals:dict=None):
        '''
        this function load and execute source code

        Arguments
        =========
        source : (code|list[code])
            compiled source to load or list of compiled sources
            list of sources will be loaded sequentially 
        
        use_other_globals : bool
            Flag for mark using of `other_globals`

        other_globals : dict
            Some dictionary that can be getted by call globals() in the zone of visibility you want
        '''
        if not use_other_globals:
            global globals
            glob = globals()
        else:
            glob = other_globals

        if type(compiled_source) == list:
            for code in compiled_source:
                exec(code, glob)
        else:
            exec(compiled_source, glob)


if __name__ == '__main__':
    try:
        try:
            encrypted_payload_filename = argv[1]
            key = argv[2]

            if len(key) != 32:
                print('[!] Key must be 32 bytes len')
                payload_file.close()
                exit(1)

        except IndexError:
            print('Usage:\n./loader.py <payload filename> <encryption key>')
            exit(1)

        payload = Loader.read(encrypted_payload_filename, key)
        print('[*] Payload decrypted. Executing..')
        Loader.load_source(payload)
        exit(0)

    except Exception as exc:
        print('[!] Error: %s' % exc)
        exit(1)