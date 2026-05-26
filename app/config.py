import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

    DB_USER = os.getenv("MYSQL_USER", "expense_user")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "expense_pass")
    DB_HOST = os.getenv("MYSQL_HOST", "db")
    DB_NAME = os.getenv("MYSQL_DATABASE", "expense_db")
    DB_PORT = os.getenv("MYSQL_PORT", "3306")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODEL_PATH = os.getenv("MODEL_PATH", "ml/overspending_model.pkl")