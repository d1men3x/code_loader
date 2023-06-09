#!/usr/bin/python3
# Interactive Module:
#   payload_maker::aes::{gen_key,encrypt}
#   payload_maker::Payload::make
# by d13x

from sys import argv
from getpass import getpass
from marshal import dumps
from base64 import b64encode
from Crypto.Cipher import AES
from random import randint, choice

class aes:
    '''Class for working with AES encryption'''
    def gen_key() -> str:
        '''
        this function generate a key with 32 bytes len

        WARNING: This function unsecure for production use, 
        recommended to replace it by some other func

        Return
        ======
        return : str
            32 byte key

        '''
        key = ''
        for _count in range(32):
            for _random_count in range(randint(1,99)):
                n = choice( [randint(48,58),randint(97,123),randint(65,91)] )
            key += chr(n)
        return key


    def encrypt( text_bytes:bytes, key:str ) -> str:
        '''
        this function encrypt `text` by AES with `key`

        Arguments
        =========
        text_bytes : bytes
            Some text in bytes for encryption

        key : str
            Key for encryption (awaited 32 bytes len)

        
        Return
        ======
        return : str
            Encrypted text
        '''
        chiper = AES.new(key.encode('utf-8'), AES.MODE_EAX)
        chiper_text, tag = chiper.encrypt_and_digest(text_bytes)
        nonce = chiper.nonce
        
        return b64encode(nonce + chiper_text + tag).decode('utf-8')


class Payload:
    '''Module for working with payload'''
    def make(source_filename:str, encryption_key:str='', return_enycryption_key=False) -> (str or (str,str)):
        '''
        this function create a byte-code(payload) from source file 
        and encrypt it by `encryption_key`

        Arguments
        ========
        source_filename : str
            Filename of source file

        encryption_key : str = ''
            Key for encrypt byte-code, 
            if not setted they will be generated by `aes.gen_key()` also
            `return_encryption_key` set to True

        return_encryption_key : bool = False
            Flag, if setted to True `encryption_key` will be added to return


        Return
        ======
        return : str or (str,str)
            if return_encryption_key flag is False reutrn only encrypted payload
            if flag is True func will be return (<encrypted payload>, <encryption key>)
        '''
        if encryption_key == '':
            return_enycryption_key = True
            encryption_key = aes.gen_key()

        source = open(source_filename, 'r')
        byte_code = dumps( compile( source.read(), mode='exec', filename='<string>') )

        if not source.readable():
            raise Exception('File %s not readable' % source_filename)
        
        encrypted_source = aes.encrypt(byte_code, encryption_key)

        if return_enycryption_key:
            return (encrypted_source, encryption_key)
        return encrypted_source

if __name__ == '__main__':
    try:
        try:
            source_filename = argv[1]

            payload_file = open(argv[2],'w')
            if not payload_file.writable():
                raise Exception('File %s not writeable' % argv[2])

        except IndexError:
            print('Usage:\n./payload_maker.py <source filename> <payload filename> <encryption key (Insecure)>')
            exit(1)

        try:
            key = argv[3]

        except IndexError:
            key = getpass('[?] Enter key for encryption(empty for random): ')

        if len(key) != 32:
            print('[!] Key must be 32 bytes len')
            payload_file.close()
            exit(1)
            
        if key == '':
            print('[*] Encryption key not provided, they will be generated randomly')

        payload, key = Payload.make(source_filename, key, True)
        payload_file.write(payload); payload_file.close()
        print('[+] Payload was successfully created')
        print('[*] Encryption key: %s' % key)
        exit(0)

    except Exception as exc:
        print('[!] Error: %s' % exc)
        exit(1)