from flask import Flask 
from flask_socketio import SocketIO, send
from pprint import pprint
from similarQuery import similar_query
from followups import followup
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


@socketio.on('message')
def handleMessage(msg):
	print("\n--------qry----------\n",msg)
	msg = similar_query(msg)
	print("\n---------resp---------\n",msg)
	resp = "".join(msg['resp'])
	
	if 'followup' in msg.keys():
		followup = msg['followup']
		t = "<br/><br/> <p> You might want to search for: <br/> <ol>"
		for x,y in followup.items():
			t += "<li><u><a onclick='document.getElementById(\"myMessage\").value = \""+y+"\"; document.getElementById(\"sendbutton\").click()' ></u>"+ x +"</a></li>"
		
		resp += t+"</ol>"

	send(resp)

if __name__ == '__main__':
	socketio.run(app)