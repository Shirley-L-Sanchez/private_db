# AES 256 encryption/decryption using pycryptodome library
# based on implementation from https://qvault.io/cryptography/aes-256-cipher-python-cryptography-examples/
#120MB/sec for single KEY
#8-9 sec/100000 with DIFFERENT KEYS - ~10 000 users/sec

from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def encrypt(plain_text, password):
    
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    #https://medium.com/coinmonks/very-basic-intro-to-aes-256-cipher-a60104847776
    #https://crypto.stackexchange.com/questions/35423/appropriate-scrypt-parameters-when-generating-an-scrypt-hash
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2, r=1, p=1, dklen=32)
    

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return salt.nonce.tag.cipher_text
    cipher_text,tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    cipher_text = b64encode(cipher_text).decode('utf-8')
    salt = b64encode(salt).decode('utf-8')
    nonce = b64encode(cipher_config.nonce).decode('utf-8')
    tag = b64encode(tag).decode('utf-8')

    # interesting post that supports storing nonce, salt, and tag with cipher_text
    # https://stackoverflow.com/questions/1905112/passphrase-salt-and-iv-do-i-need-all-of-these

    return salt + "." + nonce + "." + tag + "." + cipher_text


def decrypt(enc_str, password):
    # decode the encoded str entries from base64
    enc_lst = enc_str.split(".")
    salt = b64decode(enc_lst[0])
    nonce = b64decode(enc_lst[1])
    tag = b64decode(enc_lst[2])
    cipher_text = b64decode(enc_lst[3])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**6, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted.decode("utf-8") 

def batch_encryption(plain_texts, keys):
    '''Takes a list of plaintexts and keys. 
    Returns a list of corresponding nonce.ciphertext. 
    Note: This function does not implement scrypt hash.
    Keys are expected to be 256 random bytes.'''

    # create cipher configs
    cipher_configs = [AES.new(key, AES.MODE_GCM) for key in keys]

    # return salt.nonce.tag.cipher_text for each plain_text
    encrypted_lst = [None] * len(keys)
    n =  0

    for cipher_config, plain_text in zip(cipher_configs, plain_texts):
        cipher_text = cipher_config.encrypt(bytes(plain_text, 'utf-8'))
        cipher_text = b64encode(cipher_text).decode('utf-8')
        nonce = b64encode(cipher_config.nonce).decode('utf-8')
        encrypted_lst[n] = nonce + "." + cipher_text
        n += 1
    
    return encrypted_lst

def batch_decryption(encrypted_lst, keys):
    '''Takes a list of nonce.ciphertext and keys. 
    Returns a list of corresponding decrypted messages. 
    Note: This function does not implement scrypt hash.
    Keys are expected to be 256 random bytes.'''

    # return plain_text for each salt.nonce.tag.cipher_text
    decrypted_lst = [None] * len(keys)
    n = 0

    for encrypted_txt, key in zip(encrypted_lst, keys):
        # decode the encoded str entries from base64
        enc_lst = encrypted_txt.split(".")
        nonce = b64decode(enc_lst[0])
        cipher_text = b64decode(enc_lst[1])

        # create the cipher config
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        # decrypt the cipher text
        decrypted = cipher.decrypt(cipher_text).decode("utf-8") 
        decrypted_lst[n] = decrypted
        n += 1


    return decrypted_lst