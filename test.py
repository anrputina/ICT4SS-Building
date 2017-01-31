import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math

mu = 1
variance = 1
# sigma = math.sqrt(variance)
sigma = 1
x = 1
#plt.plot(x,mlab.normpdf(x, mu, sigma))

print (mlab.normpdf(x, mu, sigma))