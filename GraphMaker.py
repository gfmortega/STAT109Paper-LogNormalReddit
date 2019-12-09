from scipy import stats
import numpy
from math import log, sqrt, floor, exp
from matplotlib import pyplot as plt

types = ['len','getsizeof']
for t in types:
	reader = open('data/data_'+t+'.txt','r')
	data_to_analyze = reader.read().split()
	for i in range(0,len(data_to_analyze),6):
		if data_to_analyze[i]=='r/all':
			plt.clf()
			plt.figure(figsize=(5,8))
			log_data = [log(int(x)) for x in data_to_analyze[i+1].split(',')]
			plt.hist(log_data,100)
			plt.xlim([0,10])
			plt.xticks(range(0,10,2))
			plt.ylim([0,550])
			plt.yticks(range(0,550,100))
			plt.suptitle('Histogram of the natural log of the length of\n'+data_to_analyze[i]+' comments, measured\n'+('by character count' if t=='len' else 'in number of bytes'), wrap=True)
		else:
			plt.clf()
			fig, axes = plt.subplots(1,3,sharey=True,figsize=(5*3,8))
			for j in range(3):
				log_data = [log(int(x)) for x in data_to_analyze[i+2*j+1].split(',')]
				axes.flat[j].hist(log_data,100)
				axes.flat[j].set_xlim([0,10])
				axes.flat[j].set_xticks(range(0,10,2))
				axes.flat[j].set_ylim([0,550])
				axes.flat[j].set_yticks(range(0,550,100))
				axes.flat[j].set_title('Histogram of the natural log of the length of\n'+data_to_analyze[i+2*j]+' comments, measured\n'+('by character count' if t=='len' else 'in number of bytes'), wrap=True)
		plt.savefig('graph_'+t+'/'+str(i//6)+'.png')
	
	reader.close()
	