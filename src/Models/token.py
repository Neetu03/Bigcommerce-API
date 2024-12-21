from src.interactor.Database.sql_alchemy import sqlalchemy_db as db

class Token(db.Model):
    __tablename__ = 'token'

    Id = db.Column(db.Integer, primary_key=True)
    Client_Id = db.Column(db.String(255), unique=True, nullable=False)
    Client_Secret = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    store_hash = db.Column(db.String(255), nullable=False)
    
    def serialize(self):
        # Convert the model attributes into a JSON-serializable format
        return {
            'Id': self.Id,
            'Client_Id': self.Client_Id,
            'Client_Secret': self.Client_Secret,
            'access_token': self.access_token,
            'store_hash': self.store_hash
        }
    


# ACCESS TOKEN: rcrntva3yg1rd39nrzgcawwi0us8jgj
# CLIENT NAME: Example
# CLIENT ID: jhcz6cbcobf2664tyvuz8xiu5uu3tf0
# CLIENT SECRET: 4661be843a1fe059388fca55fe51ff79640d9a56618b3c70e870b99d242abc01
# NAME: Example
# API PATH: https://api.bigcommerce.com/stores/9ldckktazi/v3/



# Newpassword@3