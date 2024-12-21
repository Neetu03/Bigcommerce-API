from src.interactor.Database.sql_alchemy import sqlalchemy_db as db
from src.Models.token import Token
from sqlalchemy.exc import SQLAlchemyError

class TokenRepository:
    @staticmethod
    def initialize_database(app):
        with app.app_context():
            # Create all tables if they don't exist
            db.create_all()
            
            # Check if tokens already exist within the app context
            if not Token.query.first():  # This query now happens within the context
                initial_credentials = Token(
                    Client_Id='jhcz6cbcobf2664tyvuz8xiu5uu3tf0',
                    access_token='rcrntva3yg1rd39nrzgcawwi0us8jgj',
                    store_hash='9ldckktazi',
                    Client_Secret='4661be843a1fe059388fca55fe51ff79640d9a56618b3c70e870b99d242abc01'
                )
                db.session.add(initial_credentials)
                db.session.commit()
                print("Initial credentials added to the database.")
            else:
                print("Credentials already exist in the database.")


    
    @staticmethod
    def create_token(Client_Id, Client_Secret, access_token, store_hash):
        try:
            new_token = Token(
                Client_Id=Client_Id,
                Client_Secret=Client_Secret, 
                access_token=access_token,
                store_hash=store_hash
            )
            db.session.add(new_token)
            db.session.commit()
            return new_token
        except SQLAlchemyError as e:
            db.session.rollback()
            raise


    @staticmethod
    def get_token_by_bigCommerce_store_hash(store_hash):
        try:
            var=Token.query.filter_by(store_hash=store_hash).first()
            print(var.access_token)
            return Token.query.filter_by(store_hash=store_hash).first()
        except SQLAlchemyError as e:
                raise

    @staticmethod
    def get_all_tokens():
        try:
            return Token.query.all()
        except SQLAlchemyError as e:
            raise

    # @staticmethod
    # def update_token(Client_Id,access_token,store_hash):
    #     try:
    #         token = Token.query.filter_by(Client_Id=Client_Id).first()
    #         if token:
    #             token.Client_Id =Client_Id
    #             token.access_token = access_token
    #             token.store_hash=store_hash
    #             db.session.commit()
    #             return token
    #         return None
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         raise

    # @staticmethod
    # def delete_token(token_id):
    #     try:
    #         token = Token.query.get(token_id)
    #         if token:
    #             db.session.delete(token)
    #             db.session.commit()
    #             return True
    #         return False
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         raise