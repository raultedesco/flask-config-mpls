from app import celery, db
from models import *
from ping import *
from snmpcall import *


@celery.task(name='calery_bg_task_check_device')
def bg_task(id):
    # Chequeo Asyncrono para que no interrumpa las solicitudes http get o post
    up = ''

    device = Device.query.get(id)
    if ping(device.deviceip):
        print('Levanto!', device.deviceip)
        up = 'Up'
    else:
        print('Down!', device.deviceip)
        up = 'Down'

    print('device status:', up)

    s = snmpcall()
    i = s.interfaces()
    lista_inter = ''
    for inter in i:
        lista_inter += inter + ' '

    #result = jsonify(status=up,interfaces_snmp=lista_inter)
    return up, lista_inter
