import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dugsaiudfyagdui21h313t78qwduyhasuyd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgres://sejfhwnjsvwbwr:d5bd2225870276b9bb138013f7bf354ea9e0637475355daa07f80a22a11e453e@ec2-174-129-33-13.compute-1.amazonaws.com:5432/d7obpbv2epdb75'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
