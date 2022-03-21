from encryption.encryption import encrypt, decrypt, batch_encryption, batch_decryption
from Cryptodome.Random import get_random_bytes
from benchmarking.unix_time import unix_time

def test_integrity():
    password = get_random_bytes(32)
    message = "Hello, this is a testing message!"

    encrypted = encrypt(message, password)
    decrypted = decrypt(encrypted, password)

    if decrypted == message:
        print("Integrity test passed!")      
    else:
        print('''
        Integrity test failed! decrypted message is not as expected.''')

def test_AES_batch_encryption(n):
    keys = [get_random_bytes(32) for x in range(n)]
    messages = ["Hello, this is a testing message!" for x in range(n)]

    encrypted_lst = batch_encryption(messages, keys)
    decrypted_lst = batch_decryption(encrypted_lst, keys)

    if decrypted_lst == messages:
        print("Integrity tests passed!")      
    else:
        print('''
        Integrity tests failed! decrypted message is not as expected.''')

def benchmark_batch_encryption(n):
    keys = [get_random_bytes(32) for x in range(n)]
    messages = ["B" for x in range(n)]

    dict = unix_time(batch_encryption, (messages, keys))
    real = dict['real']
    sys = dict['sys']
    user = dict['user'] 
    return_val = dict['return_val']

    print("ENCRYPTION: \n")
    print("real time: {} s, sys time: {} s, user time: {} s \n".format(real,sys,user))

    dict = unix_time(batch_decryption, (return_val, keys))
    real = dict['real']
    sys = dict['sys']
    user = dict['user'] 

    print("DECRYPTION: \n")
    print("real time: {} s, sys time: {} s, user time: {} s".format(real,sys,user))


def main():
    benchmark_batch_encryption(100000)

if __name__ == '__main__':
    main()