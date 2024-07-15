# config.py
class Config:
    MODEL_PATH = '/home/VGT/dictionary_search/db/poseformer_160.onnx'
    DATA_STORE = '/home/VGT/dictionary_search/db/out/'
    DB_PATH = '/home/VGT/dictionary_search/db/embeddings_pf_160/'
    DATABASE_URL='postgresql+psycopg2://admin:mirto@localhost:5432/amai'
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://admin:mirto@localhost:5432/amai'
    DB_FILE = '/home/VGT/dictionary_search/demo_webapp/db_entries.csv'
    MAX_ENTRIES = 1000

class ProductionConfig(Config):
    MODEL_PATH = '/home/VGT/dictionary_search/db/poseformer_160.onnx'
    DATA_STORE = '/home/VGT/dictionary_search/db/out/'
    DB_PATH = '/home/VGT/dictionary_search/db/embeddings_pf_160/'
    DATABASE_URL='postgresql+psycopg2://admin:mirto@localhost:5432/amai'
    DATABASE_URL='postgresql+psycopg2://admin:mirto@localhost:5432/amai'
    DB_FILE = '/home/VGT/dictionary_search/demo_webapp/db_entries.csv'

    MAX_ENTRIES = 1000
class DevelopmentConfig(Config):
    MODEL_PATH = '/home/VGT/dictionary_search/db/poseformer_160.onnx'
    DATA_STORE = '/home/VGT/dictionary_search/db/out/'
    DB_PATH = '/home/VGT/dictionary_search/db/embeddings_pf_160/'
    DATABASE_URL='postgresql+psycopg2://admin:mirto@localhost:5432/amai'
    DATABASE_URL='postgresql+psycopg2://admin:mirto@localhost:5432/amai'
    DB_FILE = '/home/VGT/dictionary_search/demo_webapp/db_entries.csv'

    MAX_ENTRIES = 1000
