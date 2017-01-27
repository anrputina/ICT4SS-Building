import sys
import time
import json
import paho.mqtt.client as mqtt
from datetime import date, datetime
from ShadingSystem import Shading_System_Controller
from configuration import *

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client()             	  
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)

	except:
		sys.exit('Broker Connection failed')

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

		# for room in building.rooms:
		# 	room.show()
		# 	for window in room.windows:
		# 		window.show()

		# building.sun.compute_elevation_azimuth()
		# building.sun.print_elevation_azimuth()

	except:
		sys.exit('System Core Initialization failed')


	#LOOP
	while(True):

		building.check_status()

		for room in building.rooms:
			client.publish(room.room_name+'/Shade', json.dumps(room.create_message()))

		time.sleep(5000)

if __name__ == "__main__":
	main()