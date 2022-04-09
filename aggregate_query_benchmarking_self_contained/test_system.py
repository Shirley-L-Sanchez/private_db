from init_system import initialize_system, process_data
from bloom_filter import BloomFilter
from unix_time import unix_time
from pympler import asizeof
import pandas as pd

def test_system():
    print("Find the number of users born in October. \n")
    path = "private_db_benchmarking_data.csv"
    t, u = initialize_system(path)

    size_of_ts = []
    size_of_bfss = []
    size_of_encrypted_datas = []
    reals = []
    syss = []
    userss = []
    iis = []
    rreals = []
    rsyss = []
    ruserss = []
    x = 0
    # #start test with N thousand users
    # N = 400
    # for i in range(N):
    #     file1 = open("mylog.txt", "a")
    #     file1.write(str(i) + " \n")
    # #We make sure that changes are reflected on disk
    # file1.close()
    # process_data(path, 1000*i, (i+1)*1000 - 1, t, u)
    for i in range(0, 1000):
        #We make sure that changes are reflected on disk
        file1 = open("mylog.txt", "a") 
        file1.write(str(i) + " \n")
        file1.close()
        print("Number of users tested: ", i*1000)

        if i % 100 == 0:
            data = pd.DataFrame(
            {'Number of Users in System': iis,
            'Size of Trusted Memory (b)': size_of_ts,
            'Size of Bitarrays in Untrusted Memory (b)': size_of_bfss,
            'Size of Encrypted Data in Untrusted Memory (b)': size_of_encrypted_datas,
            'Real Execution Time with Bloom Filters (s)': reals,
            'System Execution Time with Bloom Filters (s)': syss,
            'User Execution Time with Bloom Filters (s)': userss,
            'Real Execution Time without Bloom Filters (s)': rreals,
            'System Execution Time without Bloom Filters (s)': rsyss,
            'User Execution Time without Bloom Filters (s)': ruserss})
            data.to_csv('benchmarking_system_{}.csv'.format(x))
            x += 1
            size_of_ts = []
            size_of_bfss = []
            size_of_encrypted_datas = []
            reals = []
            syss = []
            userss = []
            iis = []
            rreals = []
            rsyss = []
            ruserss = []

        process_data(path, 1000*i, (i+1)*1000 - 1, t, u)

        size_of_t = asizeof.flatsize(t)
        size_of_bfs = asizeof.asizeof(u.bitarrays)
        size_of_encrypted_data = asizeof.asizeof(u.encrypted_data)
        size_of_ts.append(size_of_t)
        size_of_bfss.append(size_of_bfs)
        size_of_encrypted_datas.append(size_of_encrypted_data)

        dict = unix_time(count_users_born_in_october_bf, (t, u))
        real = dict["real"]
        sys = dict["sys"]
        user = dict["user"]
        reals.append(real)
        syss.append(sys)
        userss.append(user)
        iis.append((i+1)*1000)

        dict = unix_time(count_users_born_in_october, (t, u))
        real = dict["real"]
        sys = dict["sys"]
        user = dict["user"]
        rsyss.append(sys)
        ruserss.append(user)
        rreals.append(real)


    data = pd.DataFrame(
        {'Number of Users in System': iis,
        'Size of Trusted Memory (b)': size_of_ts,
        'Size of Bitarrays in Untrusted Memory (b)': size_of_bfss,
        'Size of Encrypted Data in Untrusted Memory (b)': size_of_encrypted_datas,
        'Real Execution Time with Bloom Filters (s)': reals,
        'System Execution Time with Bloom Filters (s)': syss,
        'User Execution Time with Bloom Filters (s)': userss,
        'Real Execution Time without Bloom Filters (s)': rreals,
        'System Execution Time without Bloom Filters (s)': rsyss,
        'User Execution Time without Bloom Filters (s)': ruserss})
    data.to_csv('benchmarking_system_FINAL.csv'.format(x))
    file1.close()

def count_users_born_in_october_bf(t, u):
    #sql query -> condition happens in PROXY
    #get condition key
    condition = ("Users", "month", 10)
    target_num = condition[2]
    target_column = condition[1]
    condition_for_column = None
    for c in t.conditions:
        if c[1] == "month" and c[3] <= target_num <= c[4]:
            condition_for_column = c
            #we make the assumption that only one bloom filter satifies condition
            break

    #get subset of users in bloom filter from condition
    userids = t.userids

    private_userids_from_bloom_filter = []
    for userid in userids:
        private_userid = t.get_private_userid(userid)
        satisfies_condition = t.get_bloom_filter(condition_for_column).check(str(private_userid))
        if satisfies_condition:
            private_userids_from_bloom_filter.append(private_userid)

    #get encrypted data and get count
    count = 0
    for private_userid in private_userids_from_bloom_filter:
        #encrypted_data 
        #{(table_name, column_name): encrypted_data, ...}
        #always access untrusted mem with private_userid
        encrypted_data = u.get_encrypted_data(private_userid)[("Users", target_column)]
        data = t.get_secret_box(private_userid).decrypt(encrypted_data)
        if data == '10'.encode():
            count += 1
    
    return count, len(private_userids_from_bloom_filter)

def count_users_born_in_october(t, u):
    #sql query -> condition happens in PROXY
    #get condition key
    condition = ("Users", "month", 10)
    target_column = condition[1]

    #get encrypted data and get count
    userids = t.userids
    global count
    count = 0

    def decryption(t, u, userid):
        private_userid = t.get_private_userid(userid)
        #always access untrusted mem with private_userid
        encrypted_data = u.get_encrypted_data(private_userid)[("Users", target_column)]
        data = t.get_secret_box(private_userid).decrypt(encrypted_data)
        if data == '10'.encode():
            global count
            count += 1

    for userid in userids:
        decryption(t, u, userid)

    return count

def main():
    test_system()
    print("Execution successful!")

if __name__ == "__main__":
    main()