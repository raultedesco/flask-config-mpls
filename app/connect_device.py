from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


class ConnectDevice():
  def connecting(self,username,ip,password,secret):
    self.username=username
    self.ip=ip
    self.device_type='cisco_ios'
    self.password=password
    self.secret=secret
    self.profile=self.CreateProfile(self.device_type,self.ip,self.username,self.password,self.secret)
    self.error_desc=''
    try:
      self.net_connect = ConnectHandler(**self.profile)
      return self.net_connect
      
    
    except (NetMikoTimeoutException, NetMikoAuthenticationException)as e:
        self.error  = e
        self.error_desc = 'Error de Autenticacion'            
        print(self.error_desc)
    return self.error_desc

  def CreateProfile(self,device_type,ip,username,password,secret):
    cisco_device = {
                  'device_type':device_type,
                  'ip': ip,
                  'username': username,
                  'password': password,
                  'secret':secret}

    return cisco_device
    
  def disconnect(self):
        self.net_connect.disconnect()