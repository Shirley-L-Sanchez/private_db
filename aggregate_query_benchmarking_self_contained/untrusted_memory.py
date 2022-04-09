from singleton import singleton
from bitarray import bitarray

@singleton
class UntrustedMemory(object):
    '''
    Class manager for untrusted memory.
    '''
    def __init__(self):
        #Mapping Bloom Filer ID -> bloom filter's bitarray
        self.bitarrays = {}
        self.encrypted_data = {}

    def create_bitarray(self, id, size):
        if id not in self.bitarrays:
            self.bitarrays[id] = bitarray(size)
            return self.bitarrays[id]
        else:
            raise("Bitarray with id {} already exists.".format(id))

    def delete_bitarray(self, id):
        if id in self.bitarrays:
            del self.bitarrays[id]
        else:
            raise("There exists no bitarray corresponding to id {}".format(id))

    def has_bit_array(self, id):
        return id in self.bitarrays

    def setup_encrypted_data(self, userid):
        if userid not in self.encrypted_data:
            self.encrypted_data[userid] = {}
        else:
            raise ("User {} has already been assigned a storage for encrypted data.".format(userid))

    def get_encrypted_data(self, userid):
        if userid in self.encrypted_data:
            return self.encrypted_data[userid]
        else:
            raise("User {} doesn't have encrypted data - no storage, no setup".format(userid))

    def has_encrypted_data(self, userid):
        return userid in self.encrypted_data

    def del_encrypted_data(self, userid):
        if userid in self.encrypted_data:
            del self.encrypted_data[userid]
        else:
            raise("Can't delete encrypted data of user {} because it doesn't exist".format(userid))

    def set_encrypted_data(self, userid, encrypted_data):
        '''Encrypted data must be a dictionary of the form 
        {(table_name, column_name): encrypted_data, ...}.
        DO NOT DEFAULT TO USING THIS FUNCTION to set encrypted data.
        Use set_encrypted_data(self, userid, table_name, column_name, encrypted_data) instead '''
        if userid in self.encrypted_data:
            self.encrypted_data[userid] = encrypted_data
        else:
            raise("Can't set encrypted data for user {} because the user has not been set up.".format(userid))

    def set_encrypted_data(self, userid, table_name, column_name, encrypted_data):
        if userid in self.encrypted_data:
            self.encrypted_data[userid][(table_name, column_name)] = encrypted_data
        else:
            raise("Can't set encrypted data for user {} because the user has not been set up.".format(userid))

    def has_encrypted_data(self, userid, table_name, column_name):
        if userid in self.encrypted_data:
            return (table_name, column_name) in self.encrypted_data[userid]
        else:
            raise("User {} does not have encrypted data storage set up".format(userid))

    def del_encrypted_data(self, userid, table_name, column_name):
        if userid in self.encrypted_data:
            if (table_name, column_name) in self.encrypted_data[userid]:
                del self.encrypted_data[userid][(table_name, column_name)]
            else:
                raise("User {} does nort have encrypted data corresponding to table {} and column {}".format(table_name, column_name))
        else:
            raise("Can't delete encyrpted data for user {} because it has not been setup - no information available on user".format(userid)) 