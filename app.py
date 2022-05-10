from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

test = True

server_url = "0.0.0.0"
local_url = "192.168.0.172"
apphost = server_url if test == False else local_url

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")

@app.route("/socket")
def welcome():
	return { "msg": "This is EasygGO websocket" }
	
# business-side
# auth
@socket.on("socket/business/login")
def login(id):
	join_room("owner" + str(id))

@socket.on("socket/business/logout")
def logout(id):
	leave_room("owner" + str(id))

# main
@socket.on("socket/doneService")
def doneService(data):
	socket.emit("updateNotifications", data, to=data["receiver"])

@socket.on("socket/business/cancelSchedule")
def cancelSchedule(data):
	socket.emit("updateNotifications", data, to=data["receiver"])

@socket.on("socket/business/cancelAppointment")
def cancelAppointment(data):
	socket.emit("updateNotifications", data, to=data['receiver'])


# booktime
@socket.on("socket/rescheduleAppointment")
def rescheduleAppointment(data):
	socket.emit("updateNotifications", data, to=data["receiver"])

# cartorders
@socket.on("socket/orderDone")
def orderDone(data):
	socket.emit("updateNotifications", data, to=data["receiver"])
	socket.emit("updateSeeorders", data, to=data["receiver"])

@socket.on("socket/setWaitTime")
def setWaitTime(data):
	socket.emit("updateNotifications", data, to=data["receiver"])

# user-side
# login
@socket.on("socket/user/login")
def login(id):
	join_room("user" + str(id))

@socket.on("socket/user/logout")
def logout(id):
	leave_room("user" + str(id))

# booktime
@socket.on("socket/makeAppointment")
def makeAppointment(data):
	socket.emit("updateSchedules", data, to=data["receiver"])

@socket.on("socket/salonChangeAppointment")
def salonChangeAppointment(data):
	socket.emit("updateNotifications", data, to=data["receiver"])

# notifications
@socket.on("socket/closeSchedule")
def closeSchedule(data):
	socket.emit("updateNotifications", data, to=data["receiver"])

@socket.on("socket/cancelRequest")
def cancelRequest(data):
	if data["locationType"] == "restaurant":
		socket.emit("updateRequests", data, to=data["receivers"]["owners"])
		socket.emit("updateNotifications", data, to=data["receivers"]["users"])
	else:
		socket.emit("updateSchedules", data, to=data["receivers"]["owners"])

@socket.on("socket/cancelCartOrder")
def cancelCartOrder(data):
	socket.emit("updateOrderers", data, to=data["receiver"])

@socket.on("socket/confirmCartOrder")
def confirmCartOrder(data):
	socket.emit("updateOrderers", data, to=data["receiver"])

# cart
@socket.on("socket/checkoutCart")
def checkoutCart(data):
	socket.emit("updateOrders", data, to=data["receiver"])

# itemprofile
@socket.on("socket/addItemtocart")
def addItemtocart(data):
	socket.emit("updateNotifications", data, to=data["receiver"])
	socket.emit("updateNumNotifications", data, to=data["receiver"])

if __name__ == "__main__":
	socket.run(app, host=apphost, port=5002, use_reloader=True)
