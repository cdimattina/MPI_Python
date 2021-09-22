import sys

num_args = len(sys.argv)
args     = sys.argv

def compute_sum(st,sp):
	sum_total = 0
	for i in range(st,sp + 1):
		sum_total += i

	return sum_total

if (num_args > 1):

	if (num_args != 3):
		print('ERROR! Wrong number of arguments!')
	else:
		start_num = int(args[1])
		stop_num  = int(args[2])
	
		sum_total = compute_sum(start_num,stop_num)

		print("The sum of all numbers from ", start_num ," to ", stop_num  ," is: ", sum_total) 

	

	


