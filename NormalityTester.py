from scipy import stats
import numpy
from math import log, sqrt, floor, exp
from matplotlib import pyplot as plt

def output(s,writer,ender=False):
	print(s)
	writer.write(s+'\n')
	if ender==True: 
		print('----------------------------------------------------------------')
		writer.write('----------------------------------------------------------------\n')
	writer.flush()
	
types = ['len','getsizeof']
for t in types:
	reader = open('data/data_'+t+'.txt','r')
	data_to_analyze = reader.read().split()
	writer = open('data/results_'+t+'.txt','w+')
	for i in range(0,len(data_to_analyze),2):
		
		output(data_to_analyze[i],writer)
		output('',writer)
		
		log_data = [log(int(x)) for x in data_to_analyze[i+1].split(',')]
		
		mu = numpy.mean(log_data)
		var = numpy.var(log_data,ddof=1)
		stdev = sqrt(var)
		
		output('mu='+str(mu),writer)
		output('stdev='+str(stdev),writer)
		output('W,p='+str(stats.shapiro(log_data)),writer,True)
	
	reader.close()
	writer.close()
	