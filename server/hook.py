#notify通知到后自动写入数据库的hook操作,只添加余额就行,连月都不用管
from .dao_pool import Database
def updateBalance(email,amount):
    ##通过传入用户email和回调中的金额修改balance
    with Database.get_connection() as conn:
        with conn.cursor() as cur:
            print("链接数据库成功")
            query = "SELECT balance FROM `v2_user` WHERE email = %(email)s"
            params = {'email': email}
            cur.execute(query, params)
            result = cur.fetchone()

            if result is not None:
                # 如果email已经存在于数据库中，那么从数据库中获取balance,让balance加上新充值的金额就行
                balance = result[0]
                balance +=float(amount)*100
                print(balance)
                query = "UPDATE `v2_user` SET balance = %(balance)s WHERE email = %(email)s"
                params = {'balance': str(balance), 'email': email}
                cur.execute(query, params)
                conn.commit()
            else:
                # 如果email不存在于数据库中，提示用户未注册(没必要，因为没法通知到app),所以不做处理
                pass
            print("数据库操作完成")




