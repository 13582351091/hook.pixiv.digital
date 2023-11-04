import json
from typing import *
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from .hook import *

router = APIRouter()

@router.route('/', methods=['POST','GET'])
async def webhookData(request: Request):
    #获取afdian 通知的订单信息
    order_info_bytes = await request.body()
    order_info = order_info_bytes.decode()  # 将字节对象转换为字符串
    print(order_info)
    ##因为这个通知对于别人是不可见的，也无法手动查询，只好先返回收到然后写入数据库了
    resp = {'ec': 200}
    email,amount = getCustomId(order_info)
    if email and amount:
        #如果都email amount存在才会执行updataBalance
        updateBalance(email, amount)
    return JSONResponse(resp)

def getCustomId(order_info:str)-> Tuple[str, str]:
    ##从notify收到的信息中获取CustomId也就是mail以及金额
    ##获取后改变v2_user表中对应email的balance就行
    order_info_json = json.loads(order_info)
    if order_info_json['ec']==200:
        data = order_info_json['data']
        # email = data["order"]["custom_order_id"]
        # amount = data["order"]["total_amount"]
        order = data.get("order")
        email = order.get("custom_order_id") if order else None
        amount = order.get("total_amount") if order else None#这样写是为了第一次保存回调地址可以正常返回
        return email,amount
    else:
        return None,None
