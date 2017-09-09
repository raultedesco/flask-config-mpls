from flask import render_template, jsonify, request
from app import app, db
from forms import *
from models import *
from send_comands import *
from snmpcall import *
from ping import *
from flask_wtf import FlaskForm
from tasks_list import *


@app.route('/show_result_static_route', methods=['GET', 'POST'])
def show_result_static_route():
    group = 'Static Route'
    form = DevicesConfigStaticRoute()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        id_c = form.id.data
        device = Device.query.get(id_c)
        user = User.query.get(id_c)
        print('device ip:', device.deviceip)
        print('ip validada:', form.ip_destino.data)
        if ping(device.deviceip):
            # ip=form.ip_destino.data
            # mask=form.mascara.data
            # n_hop=form.next_hop.data
            # space=' '
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               'cisco', 'cisco'))
            userlogin = device.deviceuserlogin
            deviceip = device.deviceip
            devicepassword = device.devicepassword
            devicepasswordena = device.devicepasswordena

            print(userlogin, deviceip, devicepassword, devicepasswordena)
            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output , running_config = c.static_route(form.ip_destino.data, form.mascara.data, form.next_hop.data)
                # output= c.net_connect.find_prompt()
                task = bg_save_executed_cm.delay(form.id.data,output,running_config,group)
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            
            return jsonify(data=format(output))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.ip_destino.errors, error2=form.mascara.errors, error3=form.next_hop.errors)

    return jsonify(data='Error en la validacion de los datos!')




@app.route('/show_result_interface', methods=['GET', 'POST'])
def show_result_interface():
    form = DeviceConfigInterfaces()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            interface = form.interface.data
            interface_ip = form.interface_ip.data
            interface_mascara = form.interface_mascara.data

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))

            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.interfaces(form.interface.data, form.interface_ip.data,
                                      form.interface_mascara.data, 'Up')
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            return jsonify(data=format(output))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.interface.errors, error2=form.interface_ip.errors, error3=form.interface_mascara.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_interface_mpls', methods=['GET', 'POST'])
def show_result_interface_mpls():
    form = DeviceConfigInterfaces_mpls()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            interface = form.interface.data
            interface_ip = form.interface_ip.data
            interface_mascara = form.interface_mascara.data

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))

            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.interfaces_mpls_ip(form.interface.data, form.interface_ip.data,
                                              form.interface_mascara.data, 'Up')
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            return jsonify(data=format(output))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.interface.errors, error2=form.interface_ip.errors, error3=form.interface_mascara.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_interface_vrf', methods=['GET', 'POST'])
def show_result_interface_vrf():
    form = DeviceConfigInterfaces_vrf()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            interface = form.interface.data
            interface_ip = form.interface_ip.data
            interface_mascara = form.interface_mascara.data

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))

            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.interfaces_vrf(form.interface.data, form.interface_vrf.data, form.interface_ip.data,
                                          form.interface_mascara.data, 'Up')
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            return jsonify(data=format(output))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.interface.errors, error2=form.interface_ip.errors, error3=form.interface_mascara.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_bgp', methods=['GET', 'POST'])
def show_result_bgp():
    form = DevicesConfigBGP()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            # falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))
            userlogin = device.deviceuserlogin
            deviceip = device.deviceip
            devicepassword = device.devicepassword
            devicepasswordena = device.devicepasswordena

            print(userlogin, deviceip, devicepassword, devicepasswordena)
            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.bgp(form.bgp_process.data, form. bgp_neighbor.data,
                               form.bgp_as.data, form.bgp_network.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.bgp_process.errors, error2=form.bgp_as.errors, error3=form.bgp_neighbor.errors, erro4=form.bgp_network, error5=form.bgp_mascara)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_ibgp_mpls', methods=['GET', 'POST'])
def show_result_ibgp_mpls():
    form = ibgp_mpls_form()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            # falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))
            userlogin = device.deviceuserlogin
            deviceip = device.deviceip
            devicepassword = device.devicepassword
            devicepasswordena = device.devicepasswordena

            print(userlogin, deviceip, devicepassword, devicepasswordena)
            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.iBGP_mpls(form.bgp_process.data, form.bgp_as.data,
                                     form. bgp_neighbor.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.bgp_process.errors, error2=form.bgp_as.errors, error3=form.bgp_neighbor.errors, erro4=form.bgp_network, error5=form.bgp_mascara)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_ibgp_ec', methods=['GET', 'POST'])
def show_result_ibgp_ec():
    form = ibgp_ec_form()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            # falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))
            userlogin = device.deviceuserlogin
            deviceip = device.deviceip
            devicepassword = device.devicepassword
            devicepasswordena = device.devicepasswordena

            print(userlogin, deviceip, devicepassword, devicepasswordena)
            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.iBGP_extended_community(form.bgp_process.data, form. bgp_neighbor.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.bgp_process.errors, error2=form.bgp_as.errors, error3=form.bgp_neighbor.errors, erro4=form.bgp_network, error5=form.bgp_mascara)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_ebgp_vrf', methods=['GET', 'POST'])
def show_result_ebgp_vrf():
    form = ebgp_vrf_form()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            # falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))
            userlogin = device.deviceuserlogin
            deviceip = device.deviceip
            devicepassword = device.devicepassword
            devicepasswordena = device.devicepasswordena

            print(userlogin, deviceip, devicepassword, devicepasswordena)
            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.eBGP_vrf(form.bgp_process.data, form.bgp_as.data,
                                    form. bgp_neighbor.data, form.bgp_vrf.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.bgp_process.errors, error2=form.bgp_as.errors, error3=form.bgp_neighbor.errors, erro4=form.bgp_network, error5=form.bgp_mascara)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_eigrp', methods=['GET', 'POST'])
def show_result_eigrp():
    form = DevicesConfigEIGRP()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):
            eigrp_process = form.eigrp_process.data
            eigrp_network = form.eigrp_network.data
            eigrp_mascara = form.eigrp_mascara.data
            print(eigrp_process, eigrp_process, eigrp_mascara)
            # falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))
            userlogin = device.deviceuserlogin

            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.eigrp(form.eigrp_process.data,
                                 form.eigrp_network.data, form.eigrp_mascara.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.eigrp_process.errors, error2=form.eigrp_network.errors, error3=form.eigrp_mascara.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_ospf', methods=['GET', 'POST'])
def show_result_ospf():
    form = DevicesConfigOSPF()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))
            userlogin = device.deviceuserlogin

            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.ospf(form.ospf_process.data, form.ospf_network.data, form.ospf_area.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.ospf_process.errors, error2=form.ospf_network.errors, error3=form.ospf_area.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_vrf', methods=['GET', 'POST'])
def show_result_vrf():
    form = Vrf()
    # print('static route id',form.id.data)
    if form.validate_on_submit():
        device = Device.query.get(form.id.data)
        if ping(device.deviceip):

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin, device.deviceip,
                               device.devicepassword, device.devicepasswordena))

            # c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                # print(c.net_connect.find_prompt())
                output = c.vrf(form.vrf_name.data, form.vrf_rd.data, form.vrf_rt.data)
                # output= c.net_connect.find_prompt()
            else:
                output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()
            return jsonify(data=format(output))

            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')
    else:
        # flash_errors(form)
        # return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.ospf_process.errors, error2=form.ospf_network.errors, error3=form.ospf_area.errors)

    return jsonify(data='Error en la validacion de los datos!')