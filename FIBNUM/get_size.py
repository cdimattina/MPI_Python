from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() # get the rank of each node in the communicator
size = comm.Get_size() # get the size of the communicator

if rank==0:
     print('Communicator Size: ', size)
     print('Manager Node Rank: ', rank)



