# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_cors import CORS
import json
import os
import mysql.connector
import logging
import logging.handlers
import common

app = Flask(__name__)
CORS(app)

LOG_FILE = 'error.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger = logging.getLogger('tst')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

mysqlConfig = {
    'host': '127.0.0.1',  # 默认127.0.0.1
    'user': 'root',
    'password': 'ygj000',
    'port': 3306,  # 默认即为3306
    'database': 'test'  # ,
    # 'charset': 'utf8'  # 默认即为utf8
}

orders = [
    {
        "orderNO": 1,
        "status": 1,
        "count": 1,
        "amount": 99,
        "address": "河南省濮阳市黄河路与丽都路崛起时代C座5楼",
        "buyer": "尹国杰",
        "phone": "18888888888",
        "products": [
            {
                "name": "【特惠】正山堂茶业 元正特级正山小种红茶茶叶50g*3武夷桐木原产",
                "price": 99,
                "count": 1,
                "img": "https://gw.alicdn.com/bao/uploaded/i2/TB1dNF9QVXXXXaCXFXXXXXXXXXX_!!0-item_pic.jpg_120x120q50s150.jpg"
            }
        ]
    },
    {
        "orderNO": 2,
        "status": 2,
        "count": 1,
        "amount": 8,
        "address": "河南省濮阳市黄河路与丽都路崛起时代C座5楼",
        "buyer": "尹国杰",
        "phone": "18888888888",
        "products": [
            {
                "name": "汽车移车临时停车牌挪车电话号码牌卡夜光贴车内用品超市创意个性",
                "price": 8,
                "count": 1,
                "img": "https://gw.alicdn.com/bao/uploaded/i4/2158146650/TB2.t5CXxvzQeBjSZFgXXcvfVXa_!!2158146650.jpg_120x120q50s150.jpg"
            }
        ]
    },
    {
        "orderNO": 3,
        "status": 3,
        "count": 1,
        "amount": 8,
        "address": "河南省濮阳市黄河路与丽都路崛起时代C座5楼",
        "buyer": "尹国杰",
        "phone": "18888888888",
        "products": [
            {
                "name": "百易特加厚真空压缩袋送电泵包邮棉被衣物真空袋收纳袋特大号",
                "price": 51,
                "count": 1,
                "img": "https://gw.alicdn.com/bao/uploaded/i3/TB1KdA4QpXXXXbBaXXXXXXXXXXX_!!0-item_pic.jpg_120x120q50s150.jpg"
            }
        ]
    },
    {
        "orderNO": 4,
        "status": 4,
        "count": 2,
        "amount": 485,
        "address": "河南省濮阳市黄河路与丽都路崛起时代C座5楼",
        "buyer": "尹国杰",
        "phone": "18888888888",
        "products": [
            {
                "name": "亿力原装 高压清洗机水枪配件 高效去污旋转喷水毛刷P165C",
                "price": 62.16,
                "count": 1,
                "img": "https://gw.alicdn.com/bao/uploaded/i2/TB1XjGyNVXXXXabXFXXXXXXXXXX_!!0-item_pic.jpg_120x120q50s150.jpg"
            },
            {
                "name": "亿力手拎式高压洗车机家用220V洗车神器便携横款洗车泵刷车水枪",
                "price": 422.84,
                "count": 1,
                "img": "https://gw.alicdn.com/bao/uploaded/i1/1723681966/TB2YQvJkypnpuFjSZFkXXc4ZpXa_!!1723681966.jpg_120x120q50s150.jpg"
            }
        ]
    }
]


@app.route('/order/listdata', methods=['GET', 'POST'])
@app.route('/order/listdata/<int:status>', methods=['GET', 'POST'])
def getOrders(status=0):
    uid = request.form.get('uid', type=str)
    if uid is None:
        return json.dumps({'status': 2})

    return json.dumps({'status': 1, 'message': orders})


@app.route('/order/scramble', methods=['POST'])
def orderScramble():
    orderNo = request.form.get('orderNO', type=str)
    uid = request.form.get('uid', type=str)
    pass


@app.route('/order/send', methods=['POST'])
def sendOrder():
    orderNumber = request.form.get('no', type=int, default=0)
    uid = request.form.get('uid', type=str)
    if uid is None:
        return json.dumps({'status': 2})
    elif orderNumber == 0:
        return json.dumps({'status': 0, 'message': '订单编号无效'})
    else:
        return json.dumps({'status': 1})


@app.route('/order/info', methods=['POST'])
def getOrderInfo():
    uid = request.form.get('uid', type=str, default=None)
    if uid is None or len(uid) == 0:
        return json.dumps({'status': 2})
    orderNO = request.form.get('orderNO', type=str, default=None)
    if orderNO is None or len(orderNO) == 0:
        return json.dumps({'status': 0, 'message': '订单编号为空'})
    order = [o for o in orders if str(o.get('orderNO')) == orderNO]
    if len(order) > 0:
        order = order[0]
    return json.dumps({'status': 1, 'message': order})


@app.route('/postman/listdata', methods=['POST', 'GET'])
def getPostman():
    uid = request.form.get('uid', type=str)
    pageSize = request.form.get('pageSize', type=int, default=10)
    pageIndex = request.form.get('pageIndex', type=int, default=1)

    startIndex = pageSize * (pageIndex - 1)
    if uid is None:
        return json.dumps({'status': 2})

    try:  # -- ORDER BY orderCount DESC

        sql = '''SELECT id,name,phone,img,orderCount,status 
                 FROM postman 
                 WHERE status = 0 
                 LIMIT {0},10'''.format(
            startIndex)
        conn = mysql.connector.connect(**mysqlConfig)
        cur = conn.cursor()
        cur.execute(sql)
        postmans = []
        for (id, name, phone, img, orderCount, status) in cur:
            postmans.append({
                'id': id,
                'name': name,
                'phone': phone,
                'img': img,
                'orderCount': orderCount,
                'status': status
            })
        cur.close()
        conn.close()
        return json.dumps({'status': 1, 'message': postmans})
    except Exception as e:
        logger.error('获取派送员数据失败', e)
        return json.dumps({'status': 0, 'message': '获取派送员数据失败'})


@app.route('/postman/delete', methods=['POST'])
def postmanDelete():
    uid = request.form.get('uid', type=str)
    if uid is None:
        return json.dumps({'status': 2})
    id = request.form.get('id', type=str)
    if id is None:
        return json.dumps({'status': 0, 'message': '派送员ID为空，无法删除'})
    try:
        sql = 'UPDATE postman SET status = 2 WHERE id = {0}'.format(id)
        conn = mysql.connector.connect(**mysqlConfig)
        cur = conn.cursor()
        cur.execute(sql)
        result = conn.commit()
        if cur.rowcount > 0:
            return json.dumps({'status': 1})
        else:
            return json.dumps({'status': 0})
        cur.close()
        conn.close()
    except Exception as e:
        logger.error('删除派送员失败', e)
        return json.dumps({'status': 0})


@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname', type=str)
    if uname is None or len(uname) == 0:
        return json.dumps({'status': 0, 'message': '用户名不能为空'})
    pwd = request.form.get('pwd', type=str)
    if pwd is None or len(pwd) == 0:
        return json.dumps({'status': 0, 'message': '密码不能为空'})
    return json.dumps({'status': 1, 'message': 1})


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=9000, host='192.168.0.136')
