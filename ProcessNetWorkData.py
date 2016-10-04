# -*- coding:utf-8 -*-

import socket
import threading
import _thread
import time
import os
import _struct
import re
import psutil

net_data = {
    'process_speed': 0,
    'total_speed': 0
}
d_net_info = {}
lock = threading.Lock()

process_id = 0
process_name = 'BaiduYunGuanJia'
process_connections = []


def print_data():
    while True:
        lock.acquire()
        print("{0}流量为：{1}\n".format(process_name, net_data['process_speed']))
        print("总流量为：{0}\n".format(net_data['total_speed']))
        print('***********************************************\n')
        lock.release()
        time.sleep(5)


def get_net_info():
    net_info_lines = os.popen('netstat -nbo').readlines()

    # 忽略前四行无用数据
    if net_info_lines is not None:
        net_info_lines = net_info_lines[4:]
    index = 0
    for line in net_info_lines:
        index += 1
        arr = line.split()
        if (index % 2) == 0 or len(arr) < 4:
            continue
        pid = arr[4]

        if str(process_id) != pid:
            continue

        local = arr[1]
        remote = arr[2]
        key = '{0}-{1}'.format(local, remote)

        # conn = [con for con in process_connections if con['key'] == key]
        if key not in process_connections:
            process_connections.append(key)

            # process_connections.append({
            #     'key': '{0}-{1}'.format(arr[1], arr[2]),
            #     'local': arr[1],
            #     'remote': arr[2]
            # })

            # if len(arr) > 2:
            #     if arr[4] != str(process_id):
            #         continue
            #     key = "%s %s" % (arr[1], arr[2])
            #     key2 = "%s %s" % (arr[2], arr[1])
            # else:
            #     if key != '' and key not in d_net_info:
            #         d_net_info[key] = arr[0]
            #         d_net_info[key2] = arr[0]


def get_packet():
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((host, 0))

    # 设置Socket
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # net_data["unknow"] = 0

    while True:
        buffer = s.recvfrom(65565)  # 从Socket中获取数据，不过包含自己信息
        port = _struct.unpack('HH', buffer[0][20:24])

        # 从Buffer数据中获取网络IP和端口信息
        src_ip = "%d.%d.%d.%d" % _struct.unpack('BBBB', buffer[0][12:16])
        dest_ip = "%d.%d.%d.%d" % _struct.unpack('BBBB', buffer[0][16:20])
        src_port = socket.htons(port[0])
        dest_port = socket.htons(port[1])

        data_len = len(buffer[0])
        key = "%s:%d-%s:%d" % (src_ip, src_port, dest_ip, dest_port)

        net_data['process_speed'] = 0
        net_data['total_speed'] = 0

        if key in process_connections:
            net_data['process_speed'] += data_len
        net_data['total_speed'] += data_len

        # if key not in process_connections:
        #     get_net_info()
        #
        # if key in d_net_info:
        #     key2 = "%s %s" % (key, d_net_info[key])
        #     if key2 in net_data:
        #         net_data[key2] = net_data[key2] + data_len
        #     else:
        #         net_data[key2] = data_len  # _thread.start_new_thread(print_data, ())


# get_packet()


def get_process_id(process_name):
    """
    根据进程名获取进程ID
    :param process_name:
    :return:
    """
    process_list = psutil.process_iter()
    regx = re.compile(process_name, re.I)
    for process_info in process_list:
        if regx.search(process_info.name()):
            return process_info.pid
    return None


if __name__ == '__main__':
    process_id = get_process_id(process_name)
    print('【{0}】的进程ID是{1}'.format('百度云管家', process_id))

    get_net_info()
    get_packet()
    _thread.start_new_thread(print_data, ())

