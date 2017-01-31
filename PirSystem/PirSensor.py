import datetime

class Pir_Sensor():

	def __init__(self, name):
		self.room_name = name

	def add_simulation_trace(self, trace):
		self.trace = trace

	def get_person_number(self, msg):

		if (msg['type'] == 'PIR-REQUEST'):

			dict = {
				'persons': self.trace[datetime.datetime.strptime(\
									msg['timestamp'], '%Y-%m-%d %H:%M:%S')],
				'date': msg['timestamp'],
				'name': self.room_name,
				'type': 'PIR-RESPONSE'
			}

			return dict

		else:
			return None