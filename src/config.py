class AWSConfig:
    AWS_ACCESS_KEY_ID = 'aws-access-key-for-dev'
    AWS_SECERT_ACCESS_KEY = 'aws-secret-access-key-for-dev'
    AWS_S3_BUCKET_NAME = 'aws-s3-bucket-name-for-dev'


class DEVConfig:
    HOST = 'fnf-eai-dev-db.ch4iazthcd1k.ap-northeast-2.rds.amazonaws.com'
    DB = 'eaimon'
    USER = 'eaimon'
    PASSWORD = 'eaimon'
    PORT = '5432'


class PRDConfig:
    HOST = 'HOST'
    DB = 'DB'
    USER = 'USER'
    PASSWORD = 'PASSWORD'
    PORT = 'PORT'