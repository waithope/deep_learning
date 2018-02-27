# -*- coding: utf-8 -*-
from aip import AipNlp
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
from ylib import ylog
from requests.exceptions import ConnectionError, ChunkedEncodingError
from snownlp import SnowNLP

# """ 你的 APPID AK SK """
APP_ID = '10850025'
API_KEY = 'eYAUNnDTmO7qTsSYRlvfnAqh'
SECRET_KEY = 'ZQXDsGb03HpXXawLcLIiZn1MfSkYquVN'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
engine = create_engine(
    'mysql+mysqlconnector://datatec:0.618@[172.16.103.103]:3306/JYDB',
    echo=False)

# # Create MetaData instance
# metadata = MetaData(engine, reflect=True)

# # Get Table
# ex_table = metadata.tables['C_RR_ResearchReport']
# print(ex_table)
df_analysis = pd.DataFrame()
df_research = pd.read_sql(
    "SELECT * FROM JYDB.C_RR_ResearchReport order by InfoPublDate desc limit 1;",
    engine)
for item in df_research.iterrows():
    print(item[0])
    #  print(item[1]['Conclusion'])
    title = item[1]['Title']

    text = item[1]['Conclusion']
    res = client.lexer(text)
    tag = client.commentTag(text)
    # 文章标签
    keyword = client.keyword(title, text)
    # 文本分类
    topic = client.topic(title, text)
    # 情感倾向分析
    sentiment = client.sentimentClassify(text)
