#flask-config-mpls

Steps to Install and Run the App
---------------------------------------------------------------------------------------------------------------------------------------

#install python3 
youruser@debian:~$ sudo apt-get install python3

#install pip3 
youruser@debian:~$ sudo apt-get instal python3-pip

#install git
youruser@debian:~$ sudo apt-get install git

#install rabbitmq-server
youruser@debian:~$ sudo apt-get install rabbitmq-server 

#create a folder for our proyect
youruser@debian:~$ mkdir mpls_networks

#go to a folder mpls_networks
youruser@debian:~$ cd mpls_networks

#clone code from Github using git
youruser@debian:~$ git clone https://github.com/raultedesco/flask-config-mpls.git

#go to a folder flask-config-mpls
youruser@debian:~$ cd flask-config-mpls

#install dependencies
youruser@debian:~$ pip3 install -r requirements.txt

#run mpls_networks/flask-config-mpls/app/app.py
and mpls_networks/flask-config-mpls/app/server_celery_manager.sh in diferents terminals

Terminal 1
youruser@debian:~$ cd mpls_networks/flask-config-mpls/app/
youruser@debian:~$ python3 app.py

Terminal 2
youruser@debian:~$ cd mpls_networks/flask-config-mpls/app/
youruser@debian:~$ sudo ./server_celery_manager.sh

#in a web browser go to http://localhost:12346/
#enjoy!


Creditos

https://prettyprinted.com/ (Tutoriales sobre Flask )

http://markcell.github.io/jquery-tabledit/ (Libreria Jquery - in line edit table)

https://github.com/ktbyers/netmiko (Libreria para automatizar comandos cisco via SSH)

http://getbootstrap.com/ (Framwork para Desarrollo Web)

http://flask.pocoo.org/ (Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions)

http://wtforms.readthedocs.io/en/latest/ ( Generador de Formularios Web)

https://pythonhosted.org/Flask-Bootstrap/forms.html

http://www.bootply.com/128062 (CSS Animate Loading Icon Button)

http://gns3.com/ (Emulador de Hardware cisco)

https://www.cisco.com/ (Web Fabricante de Routers)

https://editor.datatables.net/examples/styling/bootstrap.html ( Datatables Editables)
