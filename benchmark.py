
from time import time, sleep
from threading import Thread
from multiprocessing import Process, Pipe




def basic_test(number_to_calculate_to):
	all_numbers = 0
	for num in range(number_to_calculate_to):
		all_numbers += 1


def test_processor(processes_to_create, number_to_calculate_to):

	processes = []
	for _ in range(processes_to_create):
		processes.append( Process(target=basic_test, args=(number_to_calculate_to,)) )
		
	start = time()

	for process in processes:
		process.start()
		
	for process in processes:
		process.join()
		
	end = time()

	return end - start
	
	
	

TIMES_TO_REPEAT_NUMBER_TEST = 2
DESIRED_TIME = 0.5
ERROR_MARGIN = 1 * (0.01)
STARTING_NUMBER = 100


TIMES_TO_REPEAT_MULTIPROCESS_TEST = 5
RUN_UNTIL_PERFORMANCE_DROP = 60



overall_number = 0
for _ in range(TIMES_TO_REPEAT_NUMBER_TEST):
	number = STARTING_NUMBER
	while 1:
		
		time_taken = test_processor(1, int(number))
		print(f"Temporary test result: {time_taken} @ {number}")
		
		if DESIRED_TIME * (1-ERROR_MARGIN) <= time_taken <= DESIRED_TIME * (1+ERROR_MARGIN):
			number = int(number)
			break
		
		number *= DESIRED_TIME / time_taken
	overall_number += number
number = overall_number / TIMES_TO_REPEAT_NUMBER_TEST

number_to_calculate_to = int(number)
original_time = time_taken
print(f"Using benchmark: {number}")


performance_drops = []

base_performance = None
processes = 1
while 1:
	
	overall_time = 0
	for _ in range(TIMES_TO_REPEAT_MULTIPROCESS_TEST):
		time_taken = test_processor(processes, number_to_calculate_to)
		overall_time += time_taken
	overall_time /= TIMES_TO_REPEAT_MULTIPROCESS_TEST
		
	if base_performance == None:
		base_performance = overall_time
	performance_drop = 100 * ( 1 - ( (base_performance) / overall_time) )
	performance_drops.append( performance_drop )
	print(f"%3d processes: %f%% performance drop, %f seconds overall"%(processes, performance_drop, overall_time))
	
	if performance_drop > RUN_UNTIL_PERFORMANCE_DROP:
		break
	processes += 1


for ind in range(len(performance_drops)-1):
	last = performance_drops[ind]
	new = performance_drops[ind+1]
	
	print("%3d to %3d processes: %f%% more performance loss" %(ind+1, ind+2, new - last) )
