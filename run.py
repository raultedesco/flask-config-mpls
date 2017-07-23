
from app import app
#from OpenSSL import SSL


#context = (app.root_path+'/bob.crt', app.root_path+'/bob.key')
#app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True, ssl_context=context, threaded=True) 
app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True) 

