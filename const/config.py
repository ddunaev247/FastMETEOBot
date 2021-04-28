# finding the constants in the module

TOKEN = '1680539744:AAG0xvH_GXxB3njPnsBNomchzFQP9DSVvG0'
url_setwebhook = 'https://api.telegram.org/bot1680539744:AAG0xvH_GXxB3njPnsBNomchzFQP9DSVvG0/setwebhook?url=https://a8e71c704531.ngrok.io'
WEAHER_TOKEN = '4d119f7db2aec24c6a9e214968be8ac2'
WEAHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=4d119f7db2aec24c6a9e214968be8ac2&lang=ru'

class Configuration(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bot_db/botDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = 'super secret key'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'