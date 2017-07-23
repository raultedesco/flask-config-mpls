from netmiko import ConnectHandler
import io
from .get_commands import Commands

class call():
    
    def calling(self,ip_destino,mascara,next_hop):

        username='raul'
        ip='192.168.10.110'
        device_type='cisco_ios'
        password='cisco'
        secret='cisco'
        static_route={'command':'ip route'}
        #print(static_route['command'])

        cisco_7200 = {
                  'device_type':device_type,
                  'ip': ip,
                  'username': username,
                  'password': password,
                  'secret':secret}

        self.diccionario=cisco_7200
        try:
            net_connect = ConnectHandler(**cisco_7200)
            c = Commands()
            estatica = c.getXmlCommand('static-route')
            #estatica = 'ip route'
            space=' '
            #print(net_connect.enable())
            #print(net_connect.config_mode())
            net_connect.enable()
            #ip_destino=input('Ingrese IP Destino:')
            no='no '
            #ip_destino='10.0.66.0'
            #mascara='255.255.255.0'
            #next_hop='1.1.1.1'
            #no_command=no+space+estatica+space+ip_destino+space+mascara+space+next_hop
            command=estatica+space+ip_destino+space+mascara+space+next_hop
            config_commands = [command]
            command1=no+estatica+space+ip_destino+space+mascara+space+next_hop
            config_commands1 = [command1]
            print(config_commands1)
            print(net_connect.find_prompt())
            o2 = net_connect.send_config_set(config_commands)   
            print(o2)
            output = net_connect.find_prompt()
            print(output)
            o1 = net_connect.send_command('sh running-config')
            #print(o1)
            o3 = net_connect.send_config_set(config_commands1)
            print(o3)
            salida = []
            #with open('foobar.txt', 'r') as f:
                #lines = [line for line in f.split(',') if line]
                #lineas = [linea.split(",") for linea in f]

            #with open('foobar.txt', 'r') as f:
                #content = f.readlines()
            content=[o1]
                # you may also want to remove whitespace characters like `\n` at the end of each line
            #content = [x.strip() for x in content] 

            print(content)
            #for linea in lineas:
                #print(linea)
            for command in config_commands1:
                print(command)
            o9 = net_connect.send_config_set(content)
            #print(net_connect.config_mode())
            #output = net_connect.find_prompt()
            #file = open("foobar.txt", "w")
            #o4 = net_connect.send_config_from_file(config_file="foobar.txt")

            #print(o4)
            #file = open("foobar.txt", "w")
            #print(file)
            #print(output)
            #print(o2)
            #print(o1)
            #print(net_connect.disconnect())
            return o9
        except Exception as e1:
            self.error1  = e1
            #self.error2  = 'No ocurrio el segundo Error'
                
             
        return self.error1


#mycall = call()
#out1 = mycall.calling('192.168.31.0','255.255.255.0','1.1.1.1')
#print(out1)
#print(out2)
