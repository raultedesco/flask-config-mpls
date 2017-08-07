from flask import render_template, redirect, url_for, jsonify, request, g, flash
import json
from app import app, db, lm, admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from forms import *
from models import *
from datatables import BaseDataTables
#from .conectRouter import call
from send_comands import *
#from .connect_device import *
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
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, registered_on=datetime.utcnow(),admin=False)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    else:
        flash_errors(form)

    return render_template('signup.html', form=form)


@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    form=ModalFormEdit()
    form1=ModalFormAdd()
    return render_template('dashboard.html', name=current_user.username, columnas=columns,form=form,form1=form1)
    #**locals(),


@app.route('/configs_backup', methods=['GET','POST'])
@login_required
def configs_backup():
    form = ModalFormViewConfig()
    return render_template('configs_backup.html',name=current_user.username, columnas=config_columns, form=form )

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

@app.route('/<command>/<device>' , methods=['GET', 'POST'])
def command(command, device):
    

    if command == 'bgp':
        form = DevicesConfigBGP()
        return render_template('bgp.html',form=form,device=device)
    if command == 'interfaces':
        form = DeviceConfigInterfaces()
        #chequear posibles errores en la llamada snmp asi como si no esta configurada la comunidad en la db y viene null
        #device= Device.query.get(device)
        #s = snmpcall()
        
        #i = s.interfaces()

        #if  i:
            #lista = [(y,y) for y in i]
            #print(lista)
            # form.interface.choices=[('i1',i[0]),('i2',i[1]),('i3',i[2])]
            #form.interface.choices=lista
            #return render_template('interfaces.html',form=form,device=device)
        #else:
            #form.interface.choices=[('message', 'fastethernet or ethernet...') ]
        return render_template('interfaces.html',form=form,device=device)
    if command =='eigrp':
        form = DevicesConfigEIGRP()
        return render_template('eigrp.html',form=form,device=device)

    if command =='ospf':
        form = DevicesConfigOSPF()
        return render_template('ospf.html',form=form,device=device)


        
        
    return 'Error de Validacion'+command+device

@app.route('/static_route')
def static_route():
        
    form = DevicesConfigStaticRoute()
    return render_template('devices.html', form=form)


@app.route('/show_result_static_route', methods=['GET', 'POST'])
def show_result_static_route():
    form = DevicesConfigStaticRoute()
    #print('static route id',form.id.data)
    if form.validate_on_submit():
        id_c=form.id.data
        device= Device.query.get(id_c)
        user=User.query.get(id_c)
        print('device ip:',device.deviceip)
        print('ip validada:',form.ip_destino.data)
        if ping(device.deviceip):
            #ip=form.ip_destino.data
            #mask=form.mascara.data
            #n_hop=form.next_hop.data
            #space=' '
            #mycall = call()
            #out = mycall.calling(ip,mask,n_hop)
            #print(out)


            c = SendCommands()
            print(c.connecting(device.deviceuserlogin,device.deviceip,device.devicepassword,device.devicepasswordena))
            userlogin=device.deviceuserlogin
            deviceip=device.deviceip
            devicepassword=device.devicepassword
            devicepasswordena=device.devicepasswordena
            
            print(userlogin,deviceip,devicepassword,devicepasswordena)
            #c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                #print(c.net_connect.find_prompt())
                output=c.static_route(form.ip_destino.data,form.mascara.data,form.next_hop.data)
                #output= c.net_connect.find_prompt()
            else:
                output='Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            #new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            #new_device_config.device= device
            #db.session.add(new_device_config)
            #db.session.commit()
            return jsonify(data=format(output))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')    
    else:
        #flash_errors(form)
        #return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.ip_destino.errors, error2=form.mascara.errors, error3=form.next_hop.errors)

    return jsonify(data='Error en la validacion de los datos!')



@app.route('/show_result_interface',methods=['GET', 'POST'])
def show_result_interface():
    form = DeviceConfigInterfaces()
    #print('static route id',form.id.data)
    if form.validate_on_submit():
        device= Device.query.get(form.id.data)
        if ping(device.deviceip):
            interface=form.interface.data
            interface_ip=form.interface_ip.data
            interface_mascara=form.interface_mascara.data

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin,device.deviceip,device.devicepassword,device.devicepasswordena))

            
            #c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                #print(c.net_connect.find_prompt())
                output=c.interfaces(form.interface.data,form.interface_ip.data,form.interface_mascara.data,'Up')
                #output= c.net_connect.find_prompt()
            else:
                output='Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            #new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            #new_device_config.device= device
            #db.session.add(new_device_config)
            #db.session.commit()

            return jsonify(data=format(output))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')    
    else:
        #flash_errors(form)
        #return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.interface.errors, error2=form.interface_ip.errors, error3=form.interface_mascara.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_bgp',methods=['GET', 'POST'])
def show_result_bgp():
    form = DevicesConfigBGP()
    #print('static route id',form.id.data)
    if form.validate_on_submit():
        device= Device.query.get(form.id.data)
        if ping(device.deviceip):
            #falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()


            c = SendCommands()
            print(c.connecting(device.deviceuserlogin,device.deviceip,device.devicepassword,device.devicepasswordena))
            userlogin=device.deviceuserlogin
            deviceip=device.deviceip
            devicepassword=device.devicepassword
            devicepasswordena=device.devicepasswordena
            
            print(userlogin,deviceip,devicepassword,devicepasswordena)
            #c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                #print(c.net_connect.find_prompt())
                output=c.bgp(form.bgp_process.data,form. bgp_neighbor.data,form.bgp_as.data,form.bgp_network.data)
                #output= c.net_connect.find_prompt()
            else:
                output='Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            #new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            #new_device_config.device= device
            #db.session.add(new_device_config)
            #db.session.commit()
            return jsonify(data=format(output))


            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')    
    else:
        #flash_errors(form)
        #return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.bgp_process.errors, error2=form.bgp_as.errors, error3=form.bgp_neighbor.errors,erro4=form.bgp_network,error5=form.bgp_mascara)

    return jsonify(data='Error en la validacion de los datos!')



@app.route('/show_result_eigrp',methods=['GET', 'POST'])
def show_result_eigrp():
    form = DevicesConfigEIGRP()
    #print('static route id',form.id.data)
    if form.validate_on_submit():
        device= Device.query.get(form.id.data)
        if ping(device.deviceip):
            eigrp_process=form.eigrp_process.data
            eigrp_network=form.eigrp_network.data
            eigrp_mascara=form.eigrp_mascara.data
            print(eigrp_process,eigrp_process,eigrp_mascara)
            #falta terminar de configurar
            # mycall = call()
            # out = mycall.calling(ip,mask,n_hop)
            # print(out)

            # new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            # new_device_config.device= device
            # db.session.add(new_device_config)
            # db.session.commit()

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin,device.deviceip,device.devicepassword,device.devicepasswordena))
            userlogin=device.deviceuserlogin
            

            #c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                #print(c.net_connect.find_prompt())
                output=c.eigrp(form.eigrp_process.data,form.eigrp_network.data,form.eigrp_mascara.data)
                #output= c.net_connect.find_prompt()
            else:
                output='Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            #new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            #new_device_config.device= device
            #db.session.add(new_device_config)
            #db.session.commit()
            return jsonify(data=format(output))


            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')    
    else:
        #flash_errors(form)
        #return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.eigrp_process.errors, error2=form.eigrp_network.errors, error3=form.eigrp_mascara.errors)

    return jsonify(data='Error en la validacion de los datos!')


@app.route('/show_result_ospf',methods=['GET', 'POST'])
def show_result_ospf():
    form = DevicesConfigOSPF()
    #print('static route id',form.id.data)
    if form.validate_on_submit():
        device= Device.query.get(form.id.data)
        if ping(device.deviceip):

            c = SendCommands()
            print(c.connecting(device.deviceuserlogin,device.deviceip,device.devicepassword,device.devicepasswordena))
            userlogin=device.deviceuserlogin
            

            #c.connecting('raul','192.168.10.110','cisco','cisco')
            if not c.error_desc == 'Error de Autenticacion':
                #print(c.net_connect.find_prompt())
                output=c.ospf(form.ospf_process.data,form.ospf_network.data,form.ospf_area.data)
                #output= c.net_connect.find_prompt()
            else:
                output='Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            #new_device_config = DeviceConfig(deviceconfig=device.devicename+'-'+str(datetime.utcnow()),devicecurrentconfig=out)
            #new_device_config.device= device
            #db.session.add(new_device_config)
            #db.session.commit()
            return jsonify(data=format(output))


            return jsonify(data=format(out))
        else:
            return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')    
    else:
        #flash_errors(form)
        #return jsonify(ip_destino=form.ip_destino.errors, mascara=form.mascara.errors, next_hop=form.next_hop.errors)
        return jsonify(error1=form.ospf_process.errors, error2=form.ospf_network.errors, error3=form.ospf_area.errors)

    return jsonify(data='Error en la validacion de los datos!')



@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username
@app.route('/bgp/<device>',methods=['GET', 'POST'])
def bgp(device):
    form = DevicesConfigBGP()
    if form.validate_on_submit():
        return '<h1>OK</h1>'
        
    return render_template('bgp.html', form=form, device=device)

@app.route('/monitor/<device>',methods=['GET', 'POST'])
def monitor(device):

       
    return render_template('monitor.html', device=device)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = ModalFormEdit()
    if form.validate_on_submit():
        print('id pasado:',form.id.data)
        print('username pasado:', form.devicename.data)
        actualdevice=Device.query.get(form.id.data)
        print(actualdevice.id)
        changed_device = actualdevice
        changed_device.devicename = form.devicename.data
        print('rol:',form.devicerol_edit.data)
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
        #return 'Form Successfully Submitted!'+'con el id:'+form.id.data+' el username:'+form.username.data+' y el mail:'+form.mail.data
        return jsonify(data=format('Device Editado Correctamente'))
    return 'no valido'

@app.route('/add', methods=['GET','POST'])
def add():
    form1 = ModalFormAdd()
    print(form1.devicename.data, form1.devicerol.data, form1.deviceso.data, form1.devicesshv2.data)
    print(form1.deviceip.data, form1.deviceuserlogin.data, form1.deviceuserpassword.data,form1.deviceenapassword.data)
    print(g.user.id)

    if form1.validate_on_submit():
        
        new_device = Device(devicename=form1.devicename.data, devicerol=form1.devicerol.data, deviceso=form1.deviceso.data, devicesshv2=form1.devicesshv2.data, deviceip=form1.deviceip.data, deviceuserlogin=form1.deviceuserlogin.data, devicepassword=form1.deviceuserpassword.data,devicepasswordena=form1.deviceenapassword.data,devicesnmp=form1.devicesnmp.data)
        new_device.user= g.user
        db.session.add(new_device)
        db.session.commit()
        #return '<h1>New user has been created!</h1>'
        return jsonify(data=format('Device Creado Correctamente'))

    return jsonify(data=format('Device no guardado'))



@app.route('/eliminar', methods=['GET','POST'])
def eliminar():
    content = request.json
    print('valor json', content)
    print('id pasado para eliminar',content['id'])
    device = Device.query.get(content['id'])
    print('id traido db', device.id)
    db.session.delete(device)
    db.session.commit()

    return jsonify(data=format('Usuario Eliminado Correctamente'))


@app.route('/config')
def config():
    return 'pagina de configuracion'

columns = ['ID', 'Image','Device Name', 'ROL', 'SO', 'SSHv2','IP','Device User login']
config_columns = ['ID','Device Configuration', 'Saved On', 'Device Id']

@app.route('/_server_data')
def _server_data():
    #print('es admin:',g.user.admin, ' y su nombre es:', g.user.username)
    if g.user.admin==1:
        all = Device.query.all()
    else:
        all = Device.query.filter_by(user_id = g.user.id).all()

    #all = Device.query.all()
    collection=[]
    for i in range(len(all)):
        if all[i].devicerol=='CPE':
            device_image_rol='<img src=static\images\cpe48.png>'
        if all[i].devicerol=='PE':
            device_image_rol='<img src=static\images\pe48.png>'
        if all[i].devicerol=='P':
            device_image_rol='<img src=static\images\p48.png>'
        collection.append(dict(zip(columns, [all[i].id,device_image_rol,all[i].devicename, all[i].devicerol,all[i].deviceso,all[i].devicesshv2,all[i].deviceip,all[i].deviceuserlogin])))

    results = BaseDataTables(request, columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)


@app.route('/_server_data_config')
def _server_data_config():
   
    #consulta todos los registros de la base deviceconfig
    all = DeviceConfig.query.all()

    

  
    collection=[]
    for i in range(len(all)):
        collection.append(dict(zip(config_columns, [all[i].id,all[i].devicecurrentconfig , all[i].deviceconfig,all[i].device_id])))

    results = BaseDataTables(request, config_columns, collection).output_result()

    # return the results as a string for the datatable
    return json.dumps(results)

@app.route('/load_device', methods=['GET','POST'])
def load_device():   
    up=''
    #print('request json',request.json)
    device= Device.query.get(request.json)
    if ping(device.deviceip):
        up='Up'
    else:
        up='Down'
    
    s = snmpcall()
    i = s.interfaces()
    lista_inter = ''
    for inter in i:
        lista_inter += inter + ' ' 

    #print('device data:',device.devicename,device.deviceip,device.devicerol)
    return jsonify(devicename=device.devicename,devicerol=device.devicerol,deviceip=device.deviceip, status=up, devicesnmp=device.devicesnmp, interfaces_snmp=lista_inter)


@app.route('/check_device', methods=['GET','POST'])
def check_device(): 
    id = request.json 
    print('id:',id)
    task = bg_task.delay(id)

    while True:
        if task.state=='SUCCESS':
            result =task.get()
            print (result[0])
            print (result[1])
            return jsonify(status=result[0],interfaces_snmp=result[1])

@app.route('/load_ip_brief_and_routes',methods=['GET','POST'])  
def load_ip_brief_and_routes():
    id = request.json
    device= Device.query.get(id)
    if ping(device.deviceip):

        c = SendCommands()
        print(c.connecting(device.deviceuserlogin,device.deviceip,device.devicepassword,device.devicepasswordena))
                       
        
        if not c.error_desc == 'Error de Autenticacion':
            print('passwords correctos')
     
            check_ip_brief,check_ip_route = c.ip_brief_and_routes()
            return jsonify(check_ip_brief=format(check_ip_brief), check_ip_route=format(check_ip_route))


        else:
            output='Verifique que los Passwords de Acceso tanto para login como modo ENABLE sean correctos'
            return jsonify(data=output)
        return jsonify(data='algo fallo')

            
    else:
        return jsonify(data='El estado del dispositivo es Down! verifique conectividad IP...')   
  

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/back',methods=['GET','POST'])
def back_route():
    return redirect(redirect_url())

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

admin.add_view(ModelView(User, db.session))