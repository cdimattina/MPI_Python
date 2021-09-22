import add_numbers as anum
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

numInputsPerRank  = 2
numOutputsPerRank = 1
numProcessors     = 4

data = None

# Manager node contains the bounds for the sum
if rank==0:	 
	data = np.array([1, 25, 26, 50, 51, 75, 76, 100],dtype = 'd')

recvbuf_nodes = np.empty(numInputsPerRank,dtype = 'd')
parsum_nodes  = np.empty(numOutputsPerRank,dtype = 'd')
comm.Scatter(data,recvbuf_nodes, root=0)
parsum_nodes  = np.array(anum.compute_sum(int(recvbuf_nodes[0]),int(recvbuf_nodes[1])),dtype = 'd')

print("Processor " + str(rank) + " adds up numbers from " + str(int(recvbuf_nodes[0])) + " to " + str(int(recvbuf_nodes[1])) + " to obtain: " + str(parsum_nodes))

# Gather the partial sums from the processors to get the total sum
recvbuf_root = np.empty(numProcessors,dtype='d')
comm.Gather(parsum_nodes,recvbuf_root, root=0)

if rank==0:	
	total_sum = np.sum(recvbuf_root)
	print("Processor 0 has gathered the partial sums to obtain the total sum of : " + str(int(total_sum)))
	

