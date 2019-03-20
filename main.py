from flask import Flask,render_template,request
from mogo import connect as PyConnection
from flask_socketio import SocketIO
from flask_socketio import disconnect
import pymongo
import paramiko

from flask_mail import Mail, Message
from flask import flash
import os
import socket
import hashlib
import pyotp
global msg
global i
global this
global db
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


db_connect = pymongo.MongoClient('127.0.0.1', 27017)
database_name = ''
database = db_connect[database_name]
collection = database.xxxxx


@app.route("/")
def start():
   return render_template("index.html")
@app.route("/index.html")
def index():
   return render_template("index.html")
@app.route("/sign.html")
def second():
    return render_template("sign.html")
@app.route("/Register.html")
def third():
    return render_template("Register.html")
@app.route("/forgot.html")
def four():
    return render_template("forgot.html")
@app.route("/email.html")
def five():
    return render_template("email.html")
@app.route("/ip.html")
def six():
    return render_template("ip.html")

@app.route("/result.html")
def seven():
    return render_template("result.html")

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
	 Email = request.form['Email']
         password = request.form['password']
         Event = request.form['Event']
         Sponsor = request.form['Sponsor']
         facebook=request.form['facebook']
	 n=len(Email)
	 fe=len(Email.split('@')[0])
	 ss=str(Email+str(n)+str(fe))
	 result = hashlib.sha1(ss.encode())
	 re=result.hexdigest()
	 first= re[:8]
	 users =database.Register.insert({"ID":first,"Email":Email,"password":password,"Event":Event,"Sponsor":Sponsor,"facebook":facebook})
	 msg = Message('Hello', sender = 'delliganeshr@techfront.in', recipients = [Email])
	 msg.body = "THIS is Your User ID. Login with ID and password. ID= "+str(first)
	 mail.send(msg)
	 msgg = "Registered successfully"
         return render_template("result.html",msgg=msgg)
@app.route('/home', methods=['POST', 'GET'])
def home():
	if request.method=='POST':
		IDD= request.form['ID']
   		passwordd = request.form['password']
		document = db.Register.find({"ID":IDD,"password":passwordd}).count()
		if document==1:
		    return render_template("ip.html",IDD=IDD)
		else:
		    return "Login Failed"
@app.route('/emaili', methods=['POST', 'GET'])
def emaili():
	global num
	global mailid
	if request.method == 'POST':
		mailid=request.form['email']
		totp = pyotp.TOTP('base32secret3232')
		num=totp.now()
		msg = Message('****', sender = 'delliganeshr@techfront.in', recipients = [mailid])
		msg.body = str(num)
		
		mail.send(msg)
		return render_template("otp.html")
@app.route('/otpverify', methods=['POST', 'GET'])
def otpverify():
	if request.method=='POST':
		otpv=request.form['OTP']
		if otpv==num:
			return render_template("forgot.html")
		else:
			return "Invalid OTP"
@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
	global mailid
	if request.method=='POST':
		password =request.form['newpassword']
		repassword=request.form['password']
		n=len(mailid)
	 	fe=len(mailid.split('@')[0])
	 	ss=str(mailid+str(n)+str(fe))
		result = hashlib.sha1(ss.encode())
	 	re=result.hexdigest()
	 	first= re[:8]
		if password==repassword:
			db.Register.update({'Email':mailid},
                      {'$set': {'password': password}},
                       upsert=True,multi=True)
			return render_template("sign.html")
		else:
			return render_template("password not matching")
@app.route('/config', methods=['POST', 'GET'])
def config():
	#r = requests.get('http://localhost:5000/config')
	#print r.read()
	print (request.is_json)
    	content = request.get_json()
    	print (content)
	print("sucess")
	if request.method=='POST':
		IP = request.form['IP']
		s_username = request.form['s_username']
		s_password = request.form['s_password']
		s_event =request.form['s_Event']
		s_match = request.form['s_Match']
		s_v = request.form['s_Venue']
		s_vpath = request.form['s_Videopath']
		s_vresolution = request.form['s_Resolution']
		s_m = request.form['s_Model']
		s_gpu = request.form['s_Gpu']
		#s_deploy = request.form['s_Deploy']
		print(IP,s_username,s_password,s_event,s_match,s_v)
		print(s_vpath,s_vresolution,s_m,s_gpu)
		client = paramiko.SSHClient()
            	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            	client.connect(IP, username=s_username, password=s_password)
		print('Client Connected')
		stdin,stdout,stderr = client.exec_command('python /media/nanoyotta/Nano-Disk2/sample/test.py')
		line=stdout
		#return line=stdout
		return render_template("ip.html",line=stdout)
                client.close()
                print('Execution Finished')
               
@socketio.on('connect', namespace='/test')
def test_connect():
      print("connected")




@socketio.on('ButtonAction',namespace='/test')
def test_message(message):
    print(message['IP'])
    IP = message['IP']
    s_username = message['s_username']
    s_password = message['s_password']
    s_event =message['s_Event']
    s_match = message['s_Match']
    s_v = message['s_Venue']
    s_vpath = message['s_Videopath']
    s_vresolution = message['s_Resolution']
    s_m = message['s_Model']
    s_gpu = message['s_Gpu']
    print('Enter Exeution Part')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP, username=s_username, password=s_password)
    print('Client Connected')
    stdin,stdout,stderr = client.exec_command('python /home/nanoyotta/videotoframes.py',get_pty=True)
    for i in stdout:
        socketio.emit('someevent', {'number': i},namespace='/test')
        socketio.sleep(0)
        print(i)

   

    
    print('Execution Finished')
    
@socketio.on('disconnect', namespace='/test')
def on_disconnect_test():
    global disconnected
    disconnected = '/test'
    print('disconnected')   
   
    client.close()
		
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host="", port="5000")
