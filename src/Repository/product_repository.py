import bigcommerce

class ProductRepository:
    def __init__(self, client_id, access_token, store_hash):
        try:
            print(f"Initializing ProductRepository with client_id: {client_id}, store_hash: {store_hash}")
            self.api = bigcommerce.api.BigcommerceApi(client_id=client_id, access_token=access_token, store_hash=store_hash)
        except Exception as e:
            print("Error initializing BigcommerceApi:", e)
