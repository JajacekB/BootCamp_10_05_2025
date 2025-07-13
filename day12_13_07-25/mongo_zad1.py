# baza nosgl - none all SQL

import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017")

my_db = my_client['mysatabase']
my_col = my_db['customers']

print(my_db.list_collection_names())


