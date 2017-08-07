from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, IPAddress, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
    username = StringField('Username', validators=[InputRequired('debe ingresar un valor'), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class DevicesConfigStaticRoute(FlaskForm):
     id= StringField('ID')
     ip_destino = StringField('IP Destino', validators=[IPAddress(ipv4=True, ipv6=False, message='IP Destino: IP invalida')])
     mascara = StringField('Mascara', validators=[DataRequired(message='Si o Si debe ingresar un numero de AS'),Length(min=7, max=15,message='Mascara: debe tener un minimo de 5 y un maximo de 15 caracteres')])
     next_hop = StringField('Next Hop', validators=[InputRequired(message='Ingrese IP correcta!')])

class DevicesConfigBGP(FlaskForm):
     id= StringField('ID')
     bgp_process = StringField('Proceso BGP', validators=[InputRequired(message='Ingrese Proceso BGP')]) 
     bgp_as = StringField('BGP AS', validators=[InputRequired(message='Ingrese AS')]) 
     bgp_neighbor = StringField('BGP Neighbor', validators=[InputRequired(message='Ingrese IP Neighbor')]) 
     bgp_network = StringField('BGP Network', validators=[InputRequired(message='Ingrese Network')]) 
     bgp_mascara = StringField('BGP Network Mask', validators=[InputRequired(message='Ingrese Network Mask')]) 

class DevicesConfigEIGRP(FlaskForm):
     id= StringField('ID')
     eigrp_process = StringField('EIGRP Process', validators=[InputRequired(message='Ingrese Proceso EIGRP')]) 
     eigrp_network = StringField('EIGRP Network', validators=[InputRequired(message='Ingrese Proceso EIGRP')]) 
     eigrp_mascara = StringField('EIGRP Wilcard bits', validators=[InputRequired(message='Ingrese Proceso EIGRP')]) 

class DevicesConfigOSPF(FlaskForm):
     id= StringField('ID')
     ospf_process = StringField('OSPF Process', validators=[InputRequired(message='Ingrese Proceso OSPF')]) 
     ospf_network = StringField('OSPF Network', validators=[InputRequired(message='Ingrese Proceso OSPF')]) 
     ospf_area = StringField('OSPF Area', validators=[InputRequired(message='Ingrese Proceso OSPF')]) 

class DeviceConfigInterfaces(FlaskForm):
     id= StringField('ID')
     interface = StringField('Interface', validators=[DataRequired(message='debe ingresar una interface')])
     interface_ip = StringField('Interface IP', validators=[IPAddress(ipv4=True, ipv6=False, message='IP Destino: IP invalida')])
     interface_mascara = StringField('Interface Mascara', validators=[DataRequired(message='Si o Si debe ingresar un numero de AS'),Length(min=7, max=15,message='Mascara: debe tener un minimo de 5 y un maximo de 15 caracteres')])

    

class DeviceBD(FlaskForm):
    device_id=StringField('Id',validators=[InputRequired()])
    device_name=StringField('Nombre',validators=[InputRequired()])
    device_rol=StringField('Tipo-Rol',validators=[InputRequired()])
    device_so=StringField('SO',validators=[InputRequired()])
    device_ssh=StringField('SSH Version',validators=[InputRequired()])

class ModalFormViewConfig(FlaskForm):
    id=StringField('Id')
    #dconfig = StringField('Device Config')
    dconfig = TextAreaField(u'Device Config')

class ModalFormEdit(FlaskForm):
    id = StringField('Id from wtf')
    devicename = StringField('Device Name')
    devicerol_edit = SelectField(u'Device Rol', choices=[('P', 'P'), ('PE', 'PE'), ('CPE', 'CPE')])
    deviceso  = StringField('Device S.O.')
    devicesshv2 = StringField('Device SSHv2')
    deviceip = StringField('Device IP')
    deviceuserlogin = StringField('User Login')
    deviceuserpassword = PasswordField('User Password') 
    deviceenapassword = PasswordField('User Ena Password')
    devicesnmp=StringField('Snmp')

class ModalFormAdd(FlaskForm):
    devicename = StringField('Device Name', validators=[DataRequired()])
    devicerol = StringField('Device Rol')
    devicerol = SelectField(u'Device Rol', choices=[('P', 'P'), ('PE', 'PE'), ('CPE', 'CPE')])
    deviceso  = StringField('Device S.O.')
    devicesshv2 = StringField('Device SSHv2')
    deviceip = StringField('Device IP')
    deviceuserlogin = StringField('User Login')
    deviceuserpassword = PasswordField('User Password') 
    deviceenapassword = PasswordField('User Ena Password')
    devicesnmp=StringField('Snmp')




