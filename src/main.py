import glob
from datetime import datetime
import psycopg2
import config
import pandas as pd
import boto3
import botocore.exceptions

# postgresql 접속
con_db = psycopg2.connect(host=config.DEVConfig.HOST, dbname=config.DEVConfig.DB, user=config.DEVConfig.USER,
                          password=config.DEVConfig.PASSWORD, port=config.DEVConfig.PORT)

#SQL Query
query1 = (f"select * from public.eai_trans_log where proc_date = to_char(now()::date-1, 'YYYYMMDD') order by proc_date desc limit 5")
query2 = (f"select * from public.if_master limit 5")
#query3 = (f"select * from public.error_code limit 5")

#날짜
now = datetime.now()
date = now.strftime('%Y%m%d')


#Query 조회 함수
def data_select():

    try:
        cur1 = con_db.cursor()
        cur1.execute(query1)
        cur2 = con_db.cursor()
        cur2.execute(query2)
        cur3 = con_db.cursor()
        #cur3.execute(query3)

        mon_data_list = (cur1.fetchall())
        if_master_list = (cur2.fetchall())

        return mon_data_list, if_master_list
    except Exception as e:
        print(e)
        return None


#csv 파일 생성 함수
def csv_create():
    csv1 = pd.read_sql_query(query1, con_db)
    csv1_name = 'eai_trans_mon_'+date+'.csv'
    csv1.to_csv(csv1_name, sep='^', index=False) #결측값, 인코딩, 경로

    csv2 = pd.read_sql_query(query2, con_db)
    csv2_name = 'if_master_' + date + '.csv'
    csv2.to_csv(csv2_name, sep='^', index=False)

    # csv3 = pd.read_sql_query(query3, con_db)
    #csv3_name = 'error_code_' + date + '.csv'
    # csv3.to_csv(csv3_name, sep='^', index=False)

    return csv1_name, csv2_name

def bucket_upload(bucket_name):
    s3 = boto3.client(
        's3',  # 사용할 서비스 이름, ec2이면 'ec2', s3이면 's3', dynamodb이면 'dynamodb'
        aws_access_key_id=config.AWSConfig.AWS_ACCESS_KEY_ID,         # 액세스 ID
        aws_secret_access_key=config.AWSConfig.AWS_SECERT_ACCESS_KEY)    # 비밀 엑세스 키
    try:
        files = glob.glob('*.csv')

        #버킷에 파일 업로드
        for file, name in range(files, files):
            s3.upload_file(file, config.AWSConfig.AWS_S3_BUCKET_NAME, name)

    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    print('조회 결과 :', data_select())
    csv_create()
    print(csv_create(), '이 생성되었습니다')
    files = glob.glob('*.csv')
    print(files)