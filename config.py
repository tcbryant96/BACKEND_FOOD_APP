import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "random_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgres://ztdsskdvvnhnji:63fef8fc79d1f0c1b31848ec3b307f9efb0c624699c50bbfedfd53837297429f@ec2-3-214-2-141.compute-1.amazonaws.com:5432/d3r4a2t8cs27ie' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False