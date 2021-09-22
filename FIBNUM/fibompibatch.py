"""
fibompibatch.py

Description: This computes the fibonacci sequence for multiple inputs
	     using a parallel process (4 cores at a time)
	     
	     Basic fibonacci sequence calculation
		base case: 		
		f(1) = 1	
		f(2) = 1
		recursion: 
		f(n) = f(n-1) + f(n-2) , n > 2 

Usage: 	     mpirun -n 4 python3 fibompibatch.py <num_fib> 

"""

import sys
import time
import fibomod as fb
from mpi4py import MPI
import numpy as np

num_args = len(sys.argv)
args     = sys.argv
num_cpu  = 4

def check_valid(inlist):
	is_valid = 1
	for i in range(1,len(inlist)):
		if(int(inlist[i])<1):
			is_valid = 0
	return is_valid

# Make sure there were 2 arguments to the program
if(num_args == 2):

	is_valid = check_valid(args) 
	# For all the inputs, sequentially compute the requested Fibonacci number
	if(is_valid):

		comm = MPI.COMM_WORLD
		size = comm.Get_size()
		rank = comm.Get_rank()

		numDataPerRank = 1
		data = None

		fibo_list   = np.arange(int(args[1])) + 1
		num_batches = int(len(fibo_list)/num_cpu)

		if rank==0:		
			print("...valid inputs...")
			print("...number of batches: " + str(num_batches))

		for i in range(num_batches):

			if rank==0:
				t0   = time.time()
				data = np.array(fibo_list[(i*num_cpu):((i+1)*num_cpu)],dtype='d')
				print("...batch: ", i + 1);

			recvbuf_nodes = np.empty(numDataPerRank,dtype='d')
			comm.Scatter(data,recvbuf_nodes, root=0)
			recvbuf_nodes = np.array(float(fb.calc_fibo(int(recvbuf_nodes)))) # for each input, compute the output

			recvbuf_root = np.empty(4,dtype='d')
			comm.Gather(recvbuf_nodes,recvbuf_root, root=0) 	

			if rank==0:
				for i in range(4):
					outStr = "The " + str(int(data[i])) + "-th Fibonacci number is: " + str(int(recvbuf_root[i]))
					print(outStr)
		
				t1 = time.time()
				wt = t1-t0                
				timeStr = "Wall time = " + str("{:.4}".format(wt))  + " seconds"
				print(timeStr)
				
	
	else:
		print("...ERROR! Usage: fibompibatch <num_fib>, integer > 0")	
else:
	print("...ERROR! Usage: fibompibatch <num_fib>, integer > 0")

	

