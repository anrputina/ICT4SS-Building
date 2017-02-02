import datetime
import random

random.seed(10000007)

configuration = {'traces':{

		datetime.datetime(2017, 1, 1, 0, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 1, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 2, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 3, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 4, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 5, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 6, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 7, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 8, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 9, 0, 0):  10 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 10, 0, 0): 10 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 11, 0, 0): 40 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 12, 0, 0): 60 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 13, 0, 0): 80 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 14, 0, 0): 100 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 15, 0, 0): 100 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 16, 0, 0): 80 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 17, 0, 0): 70 + random.randint(-20, 20),
		datetime.datetime(2017, 1, 1, 18, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 19, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 20, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 21, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 22, 0, 0): 0,
		datetime.datetime(2017, 1, 1, 23, 0, 0): 0
		
		}
}