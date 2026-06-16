# 创建数据库
CREATE DATABASE fanren;
# 创建数据表
CREATE TABLE danmu(
    time_sec DOUBLE,
    MODE INT,
    font_size INT,
    color BIGINT,
    send_time BIGINT,
    content TEXT,
    ep_id BIGINT,
    bvid VARCHAR(30),
    title VARCHAR(30)
);
# 导入数据
# 见Python

# 数据清洗
DELETE FROM danmu WHERE content IS NULL OR content='';

# 添加新数据
ALTER TABLE danmu ADD COLUMN MINUTE INT;
UPDATE danmu SET MINUTE=CEIL(time_sec/60); # 发的弹幕在第几分钟
ALTER TABLE danmu ADD COLUMN send_datetime DATETIME;
UPDATE danmu SET send_datetime=FROM_UNIXTIME(send_time); # 弹幕发出时间

# 查询哪个情节弹幕多（慕兰之战01）
SELECT
    MINUTE,
    COUNT(*) AS '弹幕数'
FROM danmu
WHERE title = '慕兰之战01'
GROUP BY MINUTE
ORDER BY MINUTE;

# 查询哪个情节弹幕多（慕兰之战02）
SELECT
    MINUTE,
    COUNT(*) AS '弹幕数'
FROM danmu
WHERE title = '慕兰之战02'
GROUP BY MINUTE
ORDER BY MINUTE;

# 查询每一集的弹幕数最多出现在第几分钟
SELECT title,MINUTE,COUNT(1) AS '弹幕数' FROM danmu GROUP BY title,MINUTE ORDER BY title,MINUTE;

SELECT t1.title,t1.minute,t1.弹幕数 AS '最大弹幕数'
FROM 
(SELECT title,MINUTE,COUNT(1) AS '弹幕数' FROM danmu GROUP BY title,MINUTE ORDER BY title,MINUTE) t1
JOIN
(SELECT title, MAX(弹幕数) AS 最大弹幕数 FROM (SELECT title, MINUTE, COUNT(1) AS 弹幕数 FROM danmu GROUP BY title, MINUTE) t 
GROUP BY title) t2
ON t1.title=t2.title AND t1.弹幕数=t2.最大弹幕数
ORDER BY title;