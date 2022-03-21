import nacl.secret
import nacl.utils
from benchmarking.unix_time import unix_time
import mmh3
#less than a second to decrypt 100 000 record from different users.
#https://cryptobook.nakov.com/symmetric-key-ciphers/popular-symmetric-algorithms
#the hash always takes less time than the decryption - is this still the case for checking the bloom filter?

def main():
    for i in range(100000):
        # This must be kept secret, this is the combination to your safe
        key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

        # This is your safe, you can use it to encrypt or decrypt messages
        box = nacl.secret.SecretBox(key)

        # This is our message to send, it must be a bytestring as SecretBox will
        #   treat it as just a binary blob of data.
        message = b"The president will be exiting through the lower levels"

        # Encrypt our message, it will be exactly 40 bytes longer than the
        #   original message as it stores authentication information and the
        #   nonce alongside it.
        encrypted = box.encrypt(message)

        # Decrypt our message, an exception will be raised if the encryption was
        #   tampered with or there was otherwise an error.
        plaintext = box.decrypt(encrypted)

print(unix_time(main))