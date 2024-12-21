from flask_sqlalchemy import SQLAlchemy


sqlalchemy_db = SQLAlchemy()

class SQLAlchemyAdapter:

    def __init__(self, app):

        if app.config['SQLALCHEMY_DATABASE_URI'] is not None:
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
            sqlalchemy_db.init_app(app)
        else:
            raise Exception("SQLALCHEMY_DATABASE_URI not set")


def setup_sqlalchemy(app, throw_exception_if_not_set=True):

    try:
        SQLAlchemyAdapter(app)
        print("SQLAlchemy setup complete")
        
    except Exception as e:
        if throw_exception_if_not_set:
            raise e

    return app