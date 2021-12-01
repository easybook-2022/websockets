from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

local = False
server_url = "0.0.0.0"
local_url = "192.168.0.172"
apphost = server_url if local == False else local_url
clients = []

app = Flask(__name__)
socket = SocketIO(app, cors_allowed_origins="*")

@app.route("/socket")
def welcome():
	return { "msg": "This is EasygGO websocket" }
	
# business-side
# auth
@socket.on("socket/business/login")
def login(id):
	if "owner" + str(id) not in clients:
		clients.append("owner" + str(id))

	join_room("owner" + str(id))

@socket.on("socket/business/logout")
def logout(id):
	if "owner" + str(id) in clients:
		clients.remove("owner" + str(id))

	leave_room("owner" + str(id))

# main
@socket.on("socket/doneService")
def doneService(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

@socket.on("socket/canServeDiners")
def canServeDiners(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

@socket.on("socket/cancelRequest")
def cancelRequest(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

@socket.on("socket/business/acceptRequest")
def acceptRequest(data):
	receivers = data["receivers"]
	booker = receivers["booker"]
	users = receivers["users"]

	socket.emit("addToNotifications", data, to=booker)
	socket.emit("addToNotifications", data, to=users)

# booktime
@socket.on("socket/rescheduleAppointment")
def rescheduleAppointment(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

# cartorders
@socket.on("socket/orderReady")
def orderReady(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

@socket.on("socket/productPurchased")
def productPurchased(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

@socket.on("socket/receivePayment")
def receivePayment(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

# makereservation
@socket.on("socket/business/rescheduleReservation")
def makeReservation(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

# dinersorders
@socket.on("socket/deleteReservation")
def deleteReservation(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

# diningorders
@socket.on("socket/deliverRound")
def deliverRound(data):
	socket.emit("updateRounds", data, to=data["receiver"])










# user-side
# login
@socket.on("socket/user/login")
def login(id):
	if "user" + str(id) not in clients:
		clients.append("user" + str(id))

	join_room("user" + str(id))

@socket.on("socket/user/logout")
def logout(id):
	if "user" + str(id) in clients:
		clients.remove("user" + str(id))

	leave_room("user" + str(id))

# booktime
@socket.on("socket/requestAppointment")
def requestAppointment(data):
	socket.emit("updateRequests", data, to=data["receiver"])

# notifications
@socket.on("socket/acceptRequest")
def acceptRequest(data):
	receivers = data["receivers"]
	locations = receivers["locations"]
	users = receivers["users"]

	socket.emit("updateRequests", data, to=locations)
	socket.emit("addToNotifications", data, to=users)

@socket.on("socket/confirmRequest")
def confirmRequest(data):
	receivers = data["receivers"]

	if data["socketType"] == "restaurant":
		locations = receivers["locations"]
		users = receivers["users"]

		socket.emit("updateSchedules", data, to=locations)
		socket.emit("addToNotifications", data, to=users)
	else:
		socket.emit("updateSchedules", data, to=receivers)

@socket.on("socket/closeRequest")
def closeRequest(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

@socket.on("socket/cancelService")
def cancelService(data):
	socket.emit("updateRequests", data, to=data["receiver"])

@socket.on("socket/allowPayment")
def allowPayment(data):
	socket.emit("updateSchedules", data, to=data["receiver"])

@socket.on("socket/sendDiningPayment")
def sendDiningPayment(data):
	socket.emit("sendDiningPayment", data, to=data["receiver"])

@socket.on("socket/acceptReservationJoining")
def acceptReservationJoining(data):
	socket.emit("updateDiners", data, to=data["receiver"])

@socket.on("socket/cancelCartOrder")
def cancelCartOrder(data):
	socket.emit("updateOrderers", data, to=data["receiver"])

@socket.on("socket/confirmCartOrder")
def confirmCartOrder(data):
	socket.emit("updateOrderers", data, to=data["receiver"])

# cart
@socket.on("socket/updateCallfor")
def updateCallfor(receiver):
	socket.emit("addToNotifications", data, to=data["receiver"])
	socket.emit("updateNumNotifications", data, to=data["receiver"])

@socket.on("socket/removeCallfor")
def removeCallfor(receiver):
	socket.emit("updateNumNotifications", data, to=data["receiver"])

@socket.on("socket/checkoutCart")
def checkoutCart(data):
	socket.emit("updateOrders", data, to=data["receiver"])

# makereservation
@socket.on("socket/makeReservation")
def makeReservation(data):
	locations = data["receivingLocations"]
	users = data["receivingUsers"]

	socket.emit("updateRequests", data, to=locations)
	socket.emit("addToNotifications", data, to=users)
	socket.emit("updateNumNotifications", data, to=users)

# order
@socket.on("socket/sendOrders")
def sendOrders(data):
	locations = data["receiverLocations"]
	diners = data["receiverDiners"]

	socket.emit("updateCustomerOrders", data, to=locations)
	socket.emit("updateRounds", data, to=diners)
	socket.emit("updateRounds", data, to=locations)

@socket.on("socket/addDiners")
def addDiners(data):
	socket.emit("addToNotifications", data, to=data["receiver"])
	socket.emit("updateNumNotifications", data, to=data["receiver"])

@socket.on("socket/addItemtoorder")
def addItemtoorder(data):
	socket.emit("addToNotifications", data, to=data["receiver"])
	socket.emit("updateNumNotifications", data, to=data["receiver"])

@socket.on("socket/cancelDiningorder")
def cancelDiningorder(data):
	socket.emit("updateRounds", data, to=data["receiver"])

@socket.on("socket/confirmDiningOrder")
def confirmDiningOrder(data):
	socket.emit("updateRounds", data, to=data["receiver"])

@socket.on("socket/deleteOrder")
def deleteOrder(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

# itemprofile
@socket.on("socket/addItemtocart")
def addItemtocart(data):
	socket.emit("addToNotifications", data, to=data["receiver"])
	socket.emit("updateNumNotifications", data, to=data["receiver"])

# dinersorders
@socket.on("socket/getDinersPayments")
def getDinersPayments(data):
	socket.emit("addToNotifications", data, to=data["receiver"])

if __name__ == "__main__":
	socket.run(app, host=apphost, port=5001, use_reloader=True)
