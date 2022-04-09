import secrets
from bloom_filter import BloomFilter
from singleton import singleton
from hyperparameters import *
import nacl.secret
import nacl.utils

@singleton
class TrustedMemory(object):
    '''
    Class manager for trusted memory.
    '''
    def __init__(self, u):
        #Mapping Condition Descriptor -> Bloom Filter
        #Condition Descriptor is a tuple. Examples: 
        #1. ("TABLE", "COLUMN", "NUMERIC", 0, 100)
        #2.  ("TABLE", "COLUMN", "CATEGORICAL", "FEMALE")
        #3. ("TABLE", "COLUMN", "TEXT", "STARTS_WITH", "A")
        self.bloom_filters = {}
        #Mapping user_id -> private_userid
        self.private_userids = {}
        #Mapping user_id -> AES encryption/decryption key
        self.keys = {}
        self.secret_boxes = {}
        self.schema = {}
        self.u = u

        #TODO: write a  global eliminate user from system 
        self.userids = []
        self.conditions = []

    def create_bloom_filter(self, condition, items_count = ITEMS_COUNT, fp_prob = FP_PROB):
        if condition not in self.bloom_filters:
            id = secrets.token_bytes(BLOOM_FILTER_ID_SIZE)
            self.bloom_filters[condition] = BloomFilter(id, self.u, items_count, fp_prob)
            self.conditions.append(condition)
        else:
            raise Exception("Bloom Filter can't be created, it already exists.")

    def delete_bloom_filter(self, condition):
        if condition in self.bloom_filters:
            del self.bloom_filters[condition]
        else:
            raise Exception("Bloom Filter can't be deleted, it doesn't exist.")
    
    def get_bloom_filter(self, condition):
        if condition in self.bloom_filters:
            return self.bloom_filters[condition]
        else:
            raise Exception("Can't get Bloom Filter {} because it doesn't exist", str(condition))
    
    def has_bloom_filter(self, condition):
        return condition in self.bloom_filters
    
    def create_private_userid(self, userid):
        if userid not in self.private_userids:
            private_userid = secrets.token_bytes(PRIVATE_ID_SIZE)
            # start of safeguard 
            if private_userid in self.private_userids.values():
                self.create_private_userid(userid)
            # end of safeguard
            else:
                self.private_userids[userid] = private_userid
                self.userids.append(userid)
        else:
            raise Exception("Private User ID can't be created, it already exists one for user {}.".format(userid))

    def delete_private_userid(self, userid):
        if userid in self.private_userids:
            del self.private_userids[userid]
        else:
            raise Exception("Private User ID can't be deleted, it doesn't exist for user {}.".format(userid))

    def get_private_userid(self, userid):
        if userid in self.private_userids:
            return self.private_userids[userid]
        else:
            raise Exception("Can't get private userid for user {} because it doesn't exist".format(userid))

    def create_key(self, userid):
        if userid not in self.keys:
            new_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
            #start safeguard
            if new_key in self.keys.values():
                self.create_key(userid)
            #end safeguard
            else:
                key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
                private_userid = self.get_private_userid(userid)
                self.keys[private_userid] = key
                self.secret_boxes[private_userid] =  nacl.secret.SecretBox(key)
        else:
            raise Exception("Can't create key for user {} because it already exists one".format(userid))

    def delete_key(self, userid):
        if userid in self.keys:
            del self.keys[userid]
            del self.secret_boxes[userid]
        else:
            raise Exception("Can't delete key for user {} because it has not been created.".format(userid))

    def get_key(self, userid):
        if userid in self.keys:
            return self.keys[userid]
        else:
            raise Exception("Can'get key for user {} because it doesn't exist.".format(userid)) 

    def get_secret_box(self, userid):
        if userid in self.secret_boxes:
            return self.secret_boxes[userid]
        else:
            raise Exception("Can'get secret box for user {} because it doesn't exist.".format(userid)) 
    
    #------------------------------------ PROTOTYPE HELPERS -------------------------------------------
    def set_schema(self, schema):
        '''schema is of the form 
        {'table_name': [column_name, ...], ...}'''
        if self.schema == {}:
            self.schema = schema
        else:
            assert("Can't override previous schema for protytpe")  