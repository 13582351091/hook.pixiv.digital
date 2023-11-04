import mysql.connector
from mysql.connector import pooling
from .utils import config
class Database:
    __connection_pool = None
    @classmethod
    def init(cls):
        try:
            cls.__connection_pool = pooling.MySQLConnectionPool(
                pool_name="v2boardPool",
                pool_size=5,
                host=config["host"],
                database=config["databaseName"],
                user=config["databaseUser"],
                password=config["password"]
            )
        except mysql.connector.Error as e:
            print("Error initializing connection pool: {}".format(str(e)))

    @classmethod
    def get_connection(cls):
        if cls.__connection_pool is None:
            cls.init()
        conn = cls.__connection_pool.get_connection()
        return conn

    @classmethod
    def release_connection(cls, connection):
        connection.close()

    @classmethod
    def close_all_connections(cls):
        cls.__connection_pool.close()

    @classmethod
    def status(cls):
        # 获取使用了的连接状态
        if cls.__connection_pool is None:
            cls.init()
        return cls.__connection_pool.get_pool_size()

if __name__ == '__main__':
    email = 'hanryr.dios482992030@gmail.com'
    with Database.get_connection() as conn:
        with conn.cursor() as cur:
            print("链接数据库成功")
            query = "SELECT balance FROM `v2_user` WHERE email = %(email)s"
            params = {'email': email}
            cur.execute(query, params)
            result = cur.fetchone()

            if result is not None:
                # 如果email已经存在于数据库中，那么从数据库中获取balance
                balance = result[0]
                print(balance)
            else:
                # 如果email不存在于数据库中，提示用户未注册(没必要，因为没法通知到app),所以不做处理
                pass
            print("数据库操作完成")
