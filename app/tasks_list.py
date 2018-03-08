from app import celery, db
from models import *
from ping import *
from snmpcall import *
from send_comands import *
import datetime

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
    i = s.interfaces(device.devicesnmp,device.deviceip)
    lista_inter = ''
    for inter in i:
        lista_inter += inter + ' '

    #result = jsonify(status=up,interfaces_snmp=lista_inter)
    return up, lista_inter

@celery.task(name='calery_bg_save_config')
def bg_save_config(id):
    # task Asyncrono para que no interrumpa las solicitudes http get o post
    message=''
    device = Device.query.get(id)
    print('user login:',device.deviceuserlogin)
    print('ip:',device.deviceip)
    print('user password:',device.devicepassword)
    print('user password ena:',device.devicepasswordena)


    c = SendCommands()
    print(c.connecting(device.deviceuserlogin, device.deviceip,device.devicepassword,devicepasswordena))
    if not c.error_desc == 'Error de Autenticacion':
        output = c.save_config()
        hora = datetime.datetime.now()
        print(hora)
        new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+'Configuracion Guardada:'+str(datetime.datetime.now()),devicecurrentconfig=output)
        new_device_config.device= device
        db.session.add(new_device_config)
        db.session.commit()
        message='se salvo la configuracion!'
    else:
        output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'

    return message


@celery.task(name='calery_bg_save_executed_cmd')
def bg_save_executed_cm(id,cmds,running_config,group):
    # task Asyncrono para que no interrumpa las solicitudes http get o post
    message=''
    device = Device.query.get(id)
    print('user login:',device.deviceuserlogin)
    print('ip:',device.deviceip)
    print('user password:',device.devicepassword)
    print('user password ena:',device.devicepasswordena)
    print('group',group)
    new_device_config = DeviceConfig(deviceconfig=cmds,devicecurrentconfig=running_config,deviceconfig_group=group)
    new_device_config.device= device
    db.session.add(new_device_config)
    db.session.commit()
    message='se salvo la configuracion!'
    return message