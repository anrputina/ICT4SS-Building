import sys
import time
import json
import paho.mqtt.client as mqtt
from client_configuration import *
from configuration import broker_configuration
from Room import Room

#Client INITIALITAZION#
try:

	room = Room(configuration['name'],
				configuration['area'],
				configuration['length'],
				configuration['width'],
				configuration['height'])

	for window in configuration['windows']:
		room.add_window(window['name'],window['azimuth'], window['height'],
		  window['length'], window['device_number'], window['device_width'])

	# for window in room.windows:
	# 	window.show()

except:
	sys.exit('System Core Initialization failed')

def shade_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	room.read_message(mes)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client()             	 
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)
		client.on_connect = on_connect

		client.message_callback_add(room.room_name+'/Shade', shade_callback)
		client.loop_forever()
	except:
		sys.exit('Broker Connection failed')

if __name__ == "__main__":
	main()