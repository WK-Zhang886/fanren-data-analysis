import pandas as pd
import pymysql

df = pd.read_csv(
    r"/数据分析-项目/bilibili_danmaku.csv"
)

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='我的密码',
    database='fanren',
    charset='utf8mb4'
)

cursor = conn.cursor()

sql = """
INSERT INTO danmu
(time_sec,mode,font_size,color,send_time,content,ep_id,bvid,title)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

for _, row in df.iterrows():

    cursor.execute(sql, (
        row['time_sec'],
        row['mode'],
        row['font_size'],
        row['color'],
        row['send_time'],
        row['text'],      # CSV里的列名
        row['ep_id'],
        row['bvid'],
        row['title']
    ))

conn.commit()

print("导入完成")

cursor.close()
conn.close()
