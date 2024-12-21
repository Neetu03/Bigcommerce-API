from src.Repository.token_repository import TokenRepository
import os,requests
APP_ID = os.environ.get('APP_ID')
APP_SECRET_KEY= os.environ.get('APP_SECRET_KEY')

def get_token_from_db(bigcommerce_store_hash):
    print(f'Getting token from database for bigcommerce_store_hash: {bigcommerce_store_hash}')
    token_repo = TokenRepository().get_token_by_bigCommerce_store_hash(bigcommerce_store_hash)
    if token_repo != None:
        print(f'Serializing token')
        token = token_repo.serialize()['access_token']
        return token
    else:
        print(f'No token found for store: {bigcommerce_store_hash}')
        return None
    

def token_exist(bigcommerce_store_hash):
    print(f'Checking if token exists for store: {bigcommerce_store_hash}')
    if get_token_from_db(bigcommerce_store_hash) != None:
        print(f'Token exists for store: {bigcommerce_store_hash}')
        return True
    else:
        print(f'Token does not exist for bigcommerce store: {bigcommerce_store_hash}')
        return False
    
# def update_access_token(bigcommerce_store_hash):
#     token_repo = TokenRepository().get_token_by_bigCommerce_client_id(bigcommerce_store_hash)
#     print(f'Found token: {token_repo}')
#     if token_repo != None:
#         print(f'Serializing token')
#         print(f'APP id :{APP_ID}')
#         print(f'APP secret id :{APP_SECRET_KEY}')
#         refresh_token = token_repo.serialize()['store_hash']
#         print(f'Refresh token from the data base: {refresh_token}')
#         url=f"https://www.wix.com/oauth/access"
#         payload = {
#             "client_id": APP_ID,
#             "client_secret": APP_SECRET_KEY,
#             "grant_type": "refresh_token",
#             "refresh_token": refresh_token
#         }
#         try:
#             response = requests.post(url, json=payload)
#             print(f'Response status :{response.status_code}')
#             new_access_token=response.json()['access_token']
#             new_token=TokenRepository.update_token(bigcommerce_store_hash,new_access_token,refresh_token)
#             return "Updated"
#         except Exception as ex:
#             print(ex)
#             return None