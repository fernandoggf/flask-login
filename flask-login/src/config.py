
class Config:
    SECRET_KEY = "asfWF$sfg_w22%"

class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}