import sys
import time
import json
import datetime
import paho.mqtt.client as mqtt
from ShadingSystem import Shading_System_Controller
from shade_core_configuration import configuration
from broker_configuration import broker_configuration

#SYSTEM CORE INITIALITAZION#
try:

	building = Shading_System_Controller(configuration['Building'],
										configuration['Season'],
										configuration['Location'][0]['latitude'],
										configuration['Location'][0]['longitude'])

	for i in range(len(configuration['Rooms'])):
		building.add_room(configuration['Rooms'][i]['name'],
						 configuration['Rooms'][i]['area'],
						 configuration['Rooms'][i]['length'],
						 configuration['Rooms'][i]['width'],
						 configuration['Rooms'][i]['height'])
		for window in configuration['Rooms'][i]['windows']:
			building.rooms[i].add_window(window['name'],window['azimuth'], window['height'],
			  window['length'], window['device_number'], window['device_width'])

	#PRINT SYSTEM STATUS
	print ('-----SYSTEM STATUS-----')
	for room in building.rooms:
		room.show()
		for window in room.windows:
			window.show()

	print ('-----END SYSTEM STATUS-----')

except:
	sys.exit('System Core Initialization failed')


def shade_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	response = building.parse_shade_message(mes)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client('core_shade')             	  
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)

		client.on_connect = on_connect
		client.message_callback_add('+/Shade', shade_callback)
		client.loop_start()

	except:
		sys.exit('Broker Connection failed')

	print ('-----RUNNING-----')
	
	#LOOP
	while(True):

		for hour in range(0, 24, 1):

			timestamp = datetime.datetime(2016, 6, 21, hour, 0, 0)
			# timestamp = datetime.date().now()
			print ('Simulating: ' + str(timestamp))

			building.check_status(timestamp)

			for room in building.rooms:
				client.publish(room.room_name+'/Shade', json.dumps(room.create_shade_message(str(timestamp))))

			time.sleep(5)

if __name__ == "__main__":
	main()