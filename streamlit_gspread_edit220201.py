#!/usr/bin/env python
# coding: utf-8

# In[16]:


import streamlit as st

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from operator import itemgetter


import pandas as pd

#st.write("DB username:", st.secrets["db_username"])


# 設定
json_path = st.secrets.json_path.json_path

gss_key = "1KUUf73iGU9Ggw1CnYgfenNNDNtGbjzg3PQz_d_lo_28"
## GoogleスプレッドシートとGoogleドライブのURL（ここは共通）
api = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# 認証処理
cred = ServiceAccountCredentials.from_json_keyfile_name(json_path, api)
gs_auth = gspread.authorize(cred)

# Work Sheet取得
lang_ws = gs_auth.open_by_key(gss_key).sheet1

# データの読み込み（pandas データフレーム）
lang_list_read = lang_ws.get_all_values()
for lang in lang_list_read:
    #print(lang)       
    df = pd.DataFrame(lang)
    #print(df)

# 日付列の取得
tesCol = lang_ws.col_values(3)
#print(tesCol)

#ワークシートの値の全てを多次元配列に格納する
cell_list = lang_ws.get_all_values()

#ヘッダ行2行を削除
cell_list.pop(0)
cell_list.pop(0)

          
#仮全体リスト（配列）ssList をつくる
ssList = []

for i in range(len(cell_list)):
    del cell_list[i][0:2]
    del cell_list[i][7:10]
    del cell_list[i][-32:]

    if cell_list[i][0]  != '':
        ssList.append(cell_list[i])
        #print(cell_list[i])
        
    else:        
        #print("bbb")
        continue

#print(ssList)

#今日の日付を取得
from datetime import datetime, date, timedelta

today = datetime.today()
print(datetime.strftime(today, '%Y/%m/%d'))

#向こう45日間のリストscListをつくる

scList = []

for i in range(45):
    nDay = today + timedelta(days=i)
    #print(nDay.strftime('%Y/%m/%d'))

    for j in range(len(ssList)):
        if ssList[j][0]  ==  nDay.strftime('%Y/%m/%d') :
            scList.append(ssList[j])
            #print(ssList[j])
        
    else:        
        #print("bbb")
        continue

print(len(scList))

print (itemgetter(0,1,2,3,4,5,6,7,8)(scList[0])) 

ccList = []
for k in range(len(scList)):
    item = list(itemgetter(0,1,2,3,4,5,6,7,8)(scList[k]))
    ccList.append(item)

print(ccList)


df = pd.DataFrame(ccList,
                   #index=['row1', 'row2'],
                  columns=['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9'])

st.dataframe(df)

    

# ワークシートの値の全てを辞書型のリストに格納する
# [第1引数]empty2zero - 空のセルをゼロに変換するかどうかを指定する
# [第2引数]head - スプレッドシートの数値に従って1から始まるキーとして使用する行を決定する
# [第3引数]default_blank - 空のセルを空の文字列またはゼロ以外の何かに変換するかどうかを指定する
cell_dict = lang_ws.get_all_records(empty2zero=False ,head=2, default_blank='')
#print(cell_dict)


#選択したワークシートの行数を取得
rowCount = lang_ws.row_count
#print(rowCount)



# In[ ]:




