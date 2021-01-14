import pymongo

# remember to alter the ip access on Mongodb atlas
def connect_mongodb(url, db_name="mydatabase", collection_name="mycollection"):
    myclient = pymongo.MongoClient(url)
    try:
        myclient.server_info()
    except Exception as e:
        raise e("Cannot connect to db!")
    # create database and collection
    mydb = myclient[db_name]
    mycol = mydb[collection_name]

    return mycol

def register_card(mongo_url, card_id, user_name):
    if not mongo_url or not isinstance(mongo_url, str):
        return { 'status': False, 'messsage': f"Invalid mongo url {card_id}! Expected url <str>.", 'id': "" }
    elif not card_id or not isinstance(card_id, str):
        return { 'status': False, 'messsage': f"Invalid card ID {card_id}! Expected card ID <str>.", 'id': "" }
    elif not user_name or not isinstance(user_name, str):
        return { 'status': False, 'messsage': f"Invalid user name {user_name}! Expected user name <str>.", 'id': "" }

    mongo_col = connect_mongodb(mongo_url)

    data = {
        "card_id": card_id,
        "name": user_name
    }

    card = mongo_col.count_documents({ "card_id": card_id })
    if card != 0:
        return { 'status': False, 'message': f"Card id already exists!.", 'id': card_id }

    result = mongo_col.insert_one(data)
    if not result.inserted_id:
        return { 'status': False, 'message': "Error occurred while inserting card into database.", 'id': "" }
    
    return { 'status': True, 'message': "Success", 'id': result.inserted_id }
    
def query_card(mongo_url, card_id):
    if not mongo_url or not isinstance(mongo_url, str):
        return { 'status': False, 'messsage': f"Invalid mongo url {card_id}! Expected url <str>.", 'id': "" }
    elif not card_id or not isinstance(card_id, str):
        return { 'status': False, 'message': "Warning: invalid card id! Expected <str>." }
    
    mongo_col = connect_mongodb(mongo_url)

    if mongo_col.count_documents({ "card_id": card_id }) == 0:
        return { 'status': False, 'message': "Card not found!" }
    elif mongo_col.count_documents({ "card_id": card_id }) == 1:
        return { 'status': True, 'message': f"Card found! User: {mongo_col.find({ 'card_id': card_id })[0]['name']}." } # choose the only one user
    else:
        return { 'status': False, 'message': "Warning: multiple cards found. Make sure your code is correct." }

def delete_all_card(mongo_url):
    if not mongo_url or not isinstance(mongo_url, str):
        return { 'status': False, 'messsage': f"Invalid mongo url {card_id}! Expected url <str>.", 'id': "" }
    
    try:
        mongo_col = connect_mongodb(mongo_url)
        result = mongo_col.delete_many({})
    except Exception as e:
        return { 'status': False, 'message': f"Error occurred! {e}."}
    
    return { 'status': True, 'message': f"Success. {result.deleted_count} documents deleted!" }
    


