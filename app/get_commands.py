import xml.etree.ElementTree as ET
import os
from app import app
class Commands():
    
    def getXmlCommand(self,valor):
    	#se agrega el app root de la app Flask para que llegue al archivo xml , ejecucion fuera de flask no es necesario el app.root_path
        tree = ET.parse(app.root_path+'/commands.xml')
        root = tree.getroot()
        for command in root.iter(valor):
            c = command.find('value').text
      
        #retorna el comando en el fichero xml
        return c
#l = Commands()
#out = l.getXmlCommand('static-route')
#print(out)
