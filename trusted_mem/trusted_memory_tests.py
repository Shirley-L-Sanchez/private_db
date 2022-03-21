from trusted_mem.trusted_memory import TrustedMemory

def test_trusted_mem_basic_funcs():
    #create a trusted mem object
    trusted_mem = TrustedMemory()
    #create bloom filter 
    items_count = 19000
    fp_prob = 0.02
    bf1 = trusted_mem.create_bloom_filter(("NUMERIC", 0, 100), items_count, fp_prob)
    bf2 = trusted_mem.create_bloom_filter(("NUMERIC", 100, 200), items_count, fp_prob)
    #get bloom filters
    bf1 = trusted_mem.get_bloom_filter(("NUMERIC", 0, 100))
    bf2 = trusted_mem.get_bloom_filter(("NUMERIC", 100, 200))
    #test values 
    if bf1.fp_prob == fp_prob and bf1.items_count == items_count and \
        bf2.fp_prob == fp_prob and bf2.items_count == items_count and \
        bf1.id != bf2.id:
        print("Bloom Filters successfully created!")
    else:
        assert("Could not create Bloom Filters correctly - attributes are not as expected.")
    #delete bloom filter and has bloom filter
    if trusted_mem.has_bloom_filter(("NUMERIC", 0, 100)) == True and \
        trusted_mem.has_bloom_filter(("NUMERIC", 100, 200)) == True:
        print("Has Bloom Filter successfully passed!")
    else: 
        assert("Missing Bloom Filter - test failed!")
    trusted_mem.delete_bloom_filter(("NUMERIC", 0, 100))
    if trusted_mem.has_bloom_filter(("NUMERIC", 0, 100)) == False and \
        trusted_mem.has_bloom_filter(("NUMERIC", 100, 200)) == True:
        print("Deletion of Bloomm Filter Test: successfully completed!")
    else:
        print("Deletion of Bloom Filter failed!")
    #create and get private_user_id
    userid1 = "1234567865432"
    trusted_mem.create_private_userid(userid1)
    private_userid1 = trusted_mem.get_private_userid(userid1)
    userid2 = "6583974982423"
    trusted_mem.create_private_userid(userid2)
    private_userid2 = trusted_mem.get_private_userid(userid2)
    if private_userid1 != private_userid2:
        print("private user ids successfully cretaed!")
    else:
        print("test failed! assigned private ids were identical!")
    #delete private_user_id
    trusted_mem.delete_private_userid(userid1)
    try:
        trusted_mem.get_private_userid(userid1)
        print("Test failed! user's private id was not deleted!")
    except Exception as e:
        print('''Test successfully completed! You got the error meesage:\n{}
            when attempting to get a deleted private_user_id'''.format(e.args[0]))
    #create and get key:
    trusted_mem.create_key(userid1)
    trusted_mem.create_key(userid2)
    if trusted_mem.get_key(userid1) != trusted_mem.get_key(userid2):
        print("Keys successfully created for each user!")
    else:
        print("Key creation failed - identical values!")
    #delete key
    trusted_mem.delete_key(userid2)
    try:
        trusted_mem.get_key(userid2)
        print("Test failed! user's key was not deleted!")
    except Exception as e:
        print('''Test successfully completed! You got the error meesage:\n{}
            when attempting to get a deleted key.'''.format(e.args[0]))


def main():
    test_trusted_mem_basic_funcs()

if __name__ == '__main__':
    main()