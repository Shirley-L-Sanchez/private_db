from datetime import date
from trusted_memory import TrustedMemory
from untrusted_memory import UntrustedMemory
from process_data import get_data_csv
import string

def initialize_system(path):
    '''
    Since this prototype is to test the scenario of aggregate private queries, 
    we are making the assumption that every column is private. 
    0. Initialize trusted and untrusted memory
    1. Create notion of schema in trusted memory - notion of privacy level is not yet implemented
    2. Create Bloom Filters for schema
    3. Get data
    4. Process data
        4.0. Register user in database (create private_userid and key) if necessary 
        4.1. Register data in Bloom Filter
        4.2. Encrypt data and store it in untrusted memory
    '''
    #initialize memories
    u = UntrustedMemory()
    t = TrustedMemory(u)

    #setup schema
    schema = {}
    _, user_columns = get_data_csv(path, 0, 1)
    schema["Users"] = user_columns
    
    #create Bloom Filters for Schema 
    n = 10 #number of bloom filters for int columns

    for i in range(n):
        t.create_bloom_filter(("Users", "user_id", "NUMERIC", i*1.0E9/n, (i+1)*1.0E9/n))
    
    for i in range(n):
        t.create_bloom_filter(("Users", "phone", "NUMERIC", i*1.0E10/n, (i+1)*1.0E10/n))

    for i in range(n):
        t.create_bloom_filter(("Users", "day", "NUMERIC", i*31/n, (i+1)*31/n))
    
    for i in range(n):
        t.create_bloom_filter(("Users", "month", "NUMERIC", i*12/n, (i+1)*12/n))
    
    for i in range(n):
        t.create_bloom_filter(("Users", "year", "NUMERIC", i*date.today().year/n, (i+1)*date.today().year/n))


    alphanum = string.ascii_letters + string.digits
    for i in range(len(alphanum)):
        t.create_bloom_filter(("Users", "first_name", "TEXT", "CONTAINS", alphanum[i]))
    
    for i in range(len(alphanum)):
        t.create_bloom_filter(("Users", "surname", "TEXT", "CONTAINS", alphanum[i]))
    
    for i in range(len(alphanum)):
        t.create_bloom_filter(("Users", "email", "TEXT", "CONTAINS", alphanum[i]))
    
    for i in range(len(alphanum)):
        t.create_bloom_filter(("Users", "gender", "TEXT", "CONTAINS", alphanum[i]))
    
    for i in range(len(alphanum)):
        t.create_bloom_filter(("Users", "location", "TEXT", "CONTAINS", alphanum[i]))

    return t, u

def process_data(path, start, end, t, u):
    user_data, _ = get_data_csv(path, start, end)
    int_columns = ["phone", "day", "month", "year"]
    text_columns = ["first_name", "surname", "email", "password", "gender", "location"]
    #Process data
    for user in user_data:
        userid = user["user_id"]
        t.create_private_userid(userid)
        t.create_key(userid)

        private_userid = t.get_private_userid(userid)
        u.setup_encrypted_data(private_userid)

        #register data in Bloom Filters
        for column_name in int_columns + text_columns:
            bloom_filters_for_c = []
            for key in t.bloom_filters.keys():
                if key[0] == "Users" and key[1] == column_name:
                    bloom_filters_for_c.append(key)
            for key in bloom_filters_for_c:
                if key[2] == "NUMERIC":
                    lower_limit = key[3]
                    upper_limit = key[4]
                    if  lower_limit <= user[column_name] <= upper_limit:
                        #add user to bloom filter
                        #use private_userid
                        t.get_bloom_filter(key).add(str(private_userid))
                if key[2] == "TEXT" and key[3] == "CONTAINS":
                    letter = key[4]
                    if letter in user[column_name]:
                        #add user to bloom filter
                        #use private_userid
                        t.get_bloom_filter(key).add(str(private_userid))
        
        #encrypt data and save it in untrusted memory
        secret_box = t.get_secret_box(private_userid)
        for column_name in ["month"]:#int_columns + text_columns:
            encrypted_data = secret_box.encrypt(str(user[column_name]).encode())
            #use private_id
            u.set_encrypted_data(private_userid, "Users", column_name, encrypted_data)

def main():
    t, u = initialize_system("private_1000.db")
    print("Function executed successfully!")

if __name__ == "__main__":
    main()