import redis
import MySQLdb
import json

def process_item():
    #创建redis数据库链接
    rediscli = redis.Redis(host="49.233.21.252",port=6379,db=0)
    #创建mysql数据库链接
    conn = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="24301234",db="foodmate",charset='utf8')

    offset = 0
    while True:
        #获取数据,将数据从redisz中pop出来
        source,data = rediscli.blpop("foodmatespider_redis:items")
        item = json.loads(data)
        #创建mysql操作游标对象，可以执行sql语句
        cursor = conn.cursor()
        cursor.execute("insert into news_table (title,source_detail,source_url,introduce,content) VALUES ('%s','%s','%s','%s','%s')" %(item['title'],item['source_detail'],item['source_url'],item['introduce'],item['content']))
        conn.commit()
        cursor.close()
        offset+=1
        print (offset)

if __name__=="__main__":
    process_item()