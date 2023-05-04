# Moudle:
#   loader::aes::decrypt
#   loader::Loader::{read,load_source}
# by d13x

from base64 import b64decode
from Crypto.Cipher import AES

class aes:
    '''Class for working with AES encryption'''
    def decrypt( crypted_text:str, key:str) -> str:
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
        return : str
            decrypted text

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

        return text.decode('utf-8')


class Loader:
    '''Class for working with encrypted by AES source'''
    def read(crypted_source_filename:str='data.bin', decryption_key:str='') -> str:
        '''
        this function read encrypted source file, decrypt and execute it

        Arguments
        =========
        crypted_source_filename : str = 'data.bin'
            Filename of crypted source file

        decryption_key : str = ''
            Key for decryption crypted source

        Return
        ======
        return : str
            Decrypted source code

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

        return aes.decrypt(file.read(), decryption_key)


    def load_source(source:(str|list[str]), use_other_globals:bool=False, other_globals:dict=None):
        '''
        this function load and execute source code

        Arguments
        =========
        source : (str|list)
            source to load or list of sources
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