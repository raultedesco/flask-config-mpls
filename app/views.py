from flask import render_template, redirect, url_for, jsonify, request, g, flash
import json
from app import app, db, lm, admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from forms import *
from models import *
from api_restful import *
from datatables import BaseDataTables
# from .conectRouter import call
from send_comands import *
# from .connect_device import *
from snmpcall import *
from ping import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, IPAddress, DataRequired
from flask_admin.contrib.sqla import ModelView


from tasks_list import *


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, registered_on=datetime.utcnow(), admin=False)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    else:
        flash_errors(form)

    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ModalFormEdit()
    form1 = ModalFormAdd()
    return render_template('dashboard.html', name=current_user.username, columnas=columns, form=form, form1=form1)
    #**locals(),


@app.route('/configs_backup', methods=['GET', 'POST'])
@login_required
def configs_backup():
    form = ModalFormViewConfig()
    return render_template('configs_backup.html', name=current_user.username, columnas=config_columns, form=form)



list_user_columns = ['ID','Usuario', 'Email','Registered_on','Is Admin']
list_devices_columns  = ['ID', 'Device Name', 'ROL', 'SO', 'SSHv2', 'IP']
list_devices_users_columns = ['ID', 'Device Name', 'ROL', 'SO', 'SSHv2', 'IP', 'Device User login']
list_devices_rol_columns = ['ID', 'Image', 'Device Na me', 'ROL', 'SO', 'SSHv2', 'IP', 'Device User login']
list_config_group_columns = ['ID', 'Config Send', 'Saved On', 'Device']


@app.route('/reporting', methods=['GET', 'POST'])
@login_required
def reporting():
    return render_template('reporting.html', name=current_user.username, columnas_user=list_user_columns, columnas_devices=list_devices_columns, columnas_devices_user=list_devices_users_columns, columnas_devices_rol=list_devices_rol_columns, columnas_config_group=list_config_group_columns)

@app.route('/configs_log', methods=['GET', 'POST'])
@login_required
def configs_log():
    form = ModalFormViewConfigLog()
    return render_template('configs_log.html', name=current_user.username, columnas=config_log_columns, form=form)



@app.route('/device_p/<device>')
def devices_p(device):

    form = DevicesConfigStaticRoute()
    return render_template('device_p.html', form=form, device=device)


@app.route('/device_pe/<device>')
def devices_pe(device):

    form = DevicesConfigStaticRoute()
    return render_template('device_pe.html', form=form, device=device)


@app.route('/device_cpe/<device>')
def devices_cpe(device):

    form = DevicesConfigStaticRoute()
    return render_template('device_cpe.html', form=form, device=device)


@app.route('/<command>/<device>', methods=['GET', 'POST'])
def command(command, device):

    if command == 'bgp':
        form = DevicesConfigBGP()
        return render_template('bgp.html', form=form, device=device)
    if command == 'interfaces':
        form = DeviceConfigInterfaces()
        return render_template('interfaces.html', form=form, device=device)
    if command == 'eigrp':
        form = DevicesConfigEIGRP()
        return render_template('eigrp.html', form=form, device=device)
    if command == 'ospf':
        form = DevicesConfigOSPF()
        return render_template('ospf.html', form=form, device=device)
    if command == 'interfaces_vrf':
        form = DeviceConfigInterfaces_vrf()
        return render_template('interfaces_vrf.html', form=form, device=device)
    if command == 'interfaces_mpls':
        form = DeviceConfigInterfaces_mpls()
        return render_template('interfaces_mpls.html', form=form, device=device)
    return 'Error de Validacion' + command + device


@app.route('/static_route')
def static_route():

    form = DevicesConfigStaticRoute()
    return render_template('devices.html', form=form)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/bgp/<device>', methods=['GET', 'POST'])
def bgp(device):
    form = DevicesConfigBGP()
    if form.validate_on_submit():
        return '<h1>OK</h1>'

    return render_template('bgp.html', form=form, device=device)


@app.route('/ibgp_mpls/<device>', methods=['GET', 'POST'])
def ibgp_mpls(device):
    form = ibgp_mpls_form()
    return render_template('ibgp_mpls.html', form=form, device=device)


@app.route('/ibgp_ec/<device>', methods=['GET', 'POST'])
def ibgp_ec(device):
    form = ibgp_ec_form()
    return render_template('ibgp_extended_community.html', form=form, device=device)


@app.route('/ebgp_vrf/<device>', methods=['GET', 'POST'])
def ebgp_vrf(device):
    form = ebgp_vrf_form()
    return render_template('ebgp_vrf.html', form=form, device=device)


@app.route('/monitor/<device>', methods=['GET', 'POST'])
def monitor(device):

    return render_template('monitor.html', device=device)


@app.route('/vrf/<device>', methods=['GET', 'POST'])
def vrf(device):
    form = Vrf()
    return render_template('vrf.html', form=form, device=device)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = ModalFormEdit()
    if form.validate_on_submit():
        print('id pasado:', form.id.data)
        print('username pasado:', form.devicename.data)
        actualdevice = Device.query.get(form.id.data)
        print(actualdevice.id)
        changed_device = actualdevice
        changed_device.devicename = form.devicename.data
        print('rol:', form.devicerol_edit.data)
        changed_device.devicerol = form.devicerol_edit.data
        changed_device.deviceso = form.deviceso.data
        changed_device.devicesshv2 = form.devicesshv2.data
        changed_device.deviceip = form.deviceip.data
        changed_device.deviceuserlogin = form.deviceuserlogin.data
        changed_device.devicepassword = form.deviceuserpassword.data
        changed_device.devicepasswordena = form.deviceenapassword.data
        changed_device.devicesnmp = form.devicesnmp.data
        db.session.add(changed_device)
        db.session.commit()
        # return 'Form Successfully Submitted!'+'con el id:'+form.id.data+' el username:'+form.username.data+' y el mail:'+form.mail.data
        return jsonify(data=format('Device Editado Correctamente'))
    return 'no valido'

@app.route('/add', methods=['GET', 'POST'])
def add():
    form1 = ModalFormAdd()
    print(form1.devicename.data, form1.devicerol.data, form1.deviceso.data, form1.devicesshv2.data)
    print(form1.deviceip.data, form1.deviceuserlogin.data,
          form1.deviceuserpassword.data, form1.deviceenapassword.data)
    print(g.user.id)

    if form1.validate_on_submit():
        new_device = Device(devicename=form1.devicename.data, devicerol=form1.devicerol.data, deviceso=form1.deviceso.data, devicesshv2=form1.devicesshv2.data, deviceip=form1.deviceip.data,
                            deviceuserlogin=form1.deviceuserlogin.data, devicepassword=form1.deviceuserpassword.data, devicepasswordena=form1.deviceenapassword.data, devicesnmp=form1.devicesnmp.data)
        new_device.user = g.user
        db.session.add(new_device)
        db.session.commit()
        # return '<h1>New user has been created!</h1>'
        return jsonify(data=format('Device Creado Correctamente'))

    return jsonify(data=format('Device no guardado'))


@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    content = request.json
    print('valor json', content)
    print('id pasado para eliminar', content['id'])
    device = Device.query.get(content['id'])
    print('id traido db', device.id)
    db.session.delete(device)
    db.session.commit()

    return jsonify(data=format('Usuario Eliminado Correctamente'))


@app.route('/delete_device', methods=['GET', 'POST'])
def delete_device():
    content = request.json
    print('valor json', content)
    print('id pasado para eliminar', content['id'])
    device_config = DeviceConfig.query.get(content['id'])
    print('id traido db', device_config.id)
    db.session.delete(device_config)
    db.session.commit()

    return jsonify(data=format('Device Eliminado Correctamente'))


@app.route('/config')
def config():
    return 'pagina de configuracion'


columns = ['ID', 'Image', 'Device Name', 'ROL', 'SO', 'SSHv2', 'IP', 'Device User login']
config_columns = ['ID', 'Device Configuration', 'Saved On', 'Device Id']
config_log_columns = ['ID', 'Config Send', 'Device']


@app.route('/_server_data')
def _server_data():
    # print('es admin:',g.user.admin, ' y su nombre es:', g.user.username)
    if g.user.admin == 1:
        all = Device.query.all()
    else:
        all = Device.query.filter_by(user_id=g.user.id).all()

    # all = Device.query.all()
    collection = []
    for i in range(len(all)):
        if all[i].devicerol == 'CPE':
            device_image_rol = '<img src=static\images\cpe48.png>'
        if all[i].devicerol == 'PE':
            device_image_rol = '<img src=static\images\pe48.png>'
        if all[i].devicerol == 'P':
            device_image_rol = '<img src=static\images\p48.png>'
        collection.append(dict(zip(columns, [all[i].id, device_image_rol, all[i].devicename, all[i].devicerol,
                                             all[i].deviceso, all[i].devicesshv2, all[i].deviceip, all[i].deviceuserlogin])))

    results = BaseDataTables(request, columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)


@app.route('/_server_data_config')
def _server_data_config():

    # consulta todos los registros de la base deviceconfig
    all = DeviceConfig.query.all()

    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(config_columns, [all[i].id, all[i].devicecurrentconfig, all[i].saved_on, all[i].device_id])))

    results = BaseDataTables(request, config_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)


@app.route('/_server_data_config_log')
def _server_data_config_log():

    # consulta todos los registros de la base deviceconfig
    all = DeviceConfig.query.all()

    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(config_log_columns, [all[i].id, all[i].deviceconfig, all[i].device_id])))

    results = BaseDataTables(request, config_log_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)


@app.route('/_server_data_list_users')
def _server_data_list_users():

    # consulta todos los registros de la base deviceconfig
    all = User.query.all()

    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(list_user_columns, [all[i].id, all[i].username, all[i].email,all[i].registered_on, all[i].admin])))

    results = BaseDataTables(request, list_user_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)

list_devices_columns  = ['ID', 'Device Name', 'ROL', 'SO', 'SSHv2', 'IP']
@app.route('/_server_data_list_devices')
def _server_data_list_devices():

    # consulta todos los registros de la base deviceconfig
    all = Device.query.all()

    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(list_devices_columns, [all[i].id, all[i].devicename, all[i].devicerol,all[i].deviceso, all[i].devicesshv2, all[i].deviceip])))

    results = BaseDataTables(request, list_devices_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)


list_devices_users_columns = ['ID', 'Device Name', 'ROL', 'SO', 'SSHv2', 'IP', 'Device User login']
@app.route('/_server_data_list_devices_user/<user_id>')
def _server_data_list_devices_user(user_id):

    # consulta todos los registros de la base deviceconfig
    all = Device.query.filter_by(user_id=user_id).all()
    print("valor de user_id",user_id)
    print("consulta", all[0].devicename)
    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(list_devices_users_columns, [all[i].id, all[i].devicename, all[i].devicerol,all[i].deviceso, all[i].devicesshv2, all[i].deviceip, all[i].deviceuserlogin])))

    results = BaseDataTables(request, list_devices_users_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)


list_devices_rol_columns = ['ID', 'Device Na me', 'ROL', 'SO', 'SSHv2', 'IP', 'Device User login']

@app.route('/_server_data_list_devices_rol/<device_rol>')
def _server_data_list_devices_rol(device_rol):

    # consulta todos los registros de la base deviceconfig
    all = Device.query.filter_by(devicerol=device_rol).all()
    print("valor de user_id",device_rol)
    print("consulta", all[0].devicename)
    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(list_devices_users_columns, [all[i].id, all[i].devicename, all[i].devicerol,all[i].deviceso, all[i].devicesshv2, all[i].deviceip, all[i].deviceuserlogin])))

    results = BaseDataTables(request, list_devices_users_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)



list_config_group_columns = ['ID', 'Config Send', 'Saved On', 'Device']

@app.route('/_server_data_list_config_group/<config_group>')
def _server_data_list_config_group(config_group):

    # consulta todos los registros de la base deviceconfig
    all = DeviceConfig.query.filter_by(deviceconfig_group=config_group).all()
    collection = []
    for i in range(len(all)):
        collection.append(dict(
            zip(list_config_group_columns, [all[i].id, all[i].deviceconfig, all[i].saved_on,all[i].device_id])))

    results = BaseDataTables(request, list_config_group_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)



@app.route('/load_device', methods=['GET', 'POST'])
def load_device():
    up = ''
    # print('request json',request.json)
    device = Device.query.get(request.json)
    if ping(device.deviceip):
        up = 'Up'
    else:
        up = 'Down'

    s = snmpcall()
    i = s.interfaces(device.devicesnmp,device.deviceip)
    lista_inter = ''
    for inter in i:
        lista_inter += inter + ' '

    # print('device data:',device.devicename,device.deviceip,device.devicerol)
    return jsonify(devicename=device.devicename, devicerol=device.devicerol, deviceip=device.deviceip, status=up, devicesnmp=device.devicesnmp, interfaces_snmp=lista_inter)


@app.route('/check_device', methods=['GET', 'POST'])
def check_device():
    id = request.json
    print('id:', id)
    task = bg_task.delay(id)

    while True:
        if task.state == 'SUCCESS':
            result = task.get()
            print(result[0])
            print(result[1])
            return jsonify(status=result[0], interfaces_snmp=result[1])

    return jsonify(status="pending", interfaces_snmp="no results yet")

@app.route('/load_ip_brief_and_routes', methods=['GET', 'POST'])
def load_ip_brief_and_routes():
    id = request.json
    device = Device.query.get(id)
    if ping(device.deviceip):

        c = SendCommands()
        print(c.connecting(device.deviceuserlogin, device.deviceip,
                           device.devicepassword, device.devicepasswordena))

        if not c.error_desc == 'Error de Autenticacion':
            print('passwords correctos')

            check_ip_brief, check_ip_route = c.ip_brief_and_routes()
            return jsonify(check_ip_brief=format(check_ip_brief), check_ip_route=format(check_ip_route))

        else:
            output = 'Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            return jsonify(data=output)
        return jsonify(data='algo fallo')

    else:
        return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')


@app.route('/get_device_data', methods=['GET', 'POST'])
def get_device_data():
    id = request.json
    print('id json:', id)
    device = Device.query.get(id)
    password = device.devicepassword
    password_ena = device.devicepasswordena
    snmp = device.devicesnmp
    return jsonify(password= password, password_ena = password_ena, snmp=snmp)

@app.route('/save_config', methods=['GET', 'POST'])
def save_config():
    id = request.json
    print('id:', id)
    task = bg_save_config.delay(id)
    return jsonify(data='Proccess to save config trigger!')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/back', methods=['GET', 'POST'])
def back_route():
    return redirect(redirect_url())


def redirect_url():
    return request.args.get('next') or \
        request.referrer or \
        url_for('index')


admin.add_view(ModelView(User, db.session))



