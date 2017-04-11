import sys

val_order = []
math_operators = ['+', '-', '/', '*']
db_operations = ["read", "write", "output"]


def print_val(val_data):
	for val in val_order:
		print(val, str(val_data[val]), end='')
		if val_order.index(val) != len(val_order) - 1:
			print(" ", end='')
	print()

def get_val(data):
	val_data = {}
	data = data.strip().split()
	for index in range(0, len(data), 2):
		val_order.append(data[index])
		val_data[data[index]] = int(data[index + 1])
	return val_data

def math_operate(core_element, element1, element2, operator, swap_mem):
	if element1.isdigit():
		element1 = int(element1)
	else:
		element1 = swap_mem[element1]
	if element2.isdigit():
		element2 = int(element2)
	else:
		element2 = swap_mem[element2]
	if operator == '+':
		swap_mem[core_element] = element1 + element2
	elif operator == '-':
		swap_mem[core_element] = element1 - element2
	elif operator == "*":
		swap_mem[core_element] = element1 * element2
	else:
		try:
			swap_mem[core_element] = element1 / element2
		except:
			print("Operation Error")
			sys.exit(0)

	return swap_mem

def db_operate(params, operation, swap_mem, val_data, transaction_id):
	'''
	read(element, variable to be stored in)
	write(element, variable to read from)
	output(commit element)
	'''
	params = params.strip()
	delimit = ","
	if delimit in params:
		param1, param2 = params.split(",")
		param1 = param1.strip()
		param2 = param2.strip()

	if operation == "read":
		swap_mem[param2] = val_data[param1]
	elif operation == "write":
		print("<" + transaction_id + ", " + param1 + ", " + str(val_data[param1]) + ">")
		val_data[param1] = swap_mem[param2]
		print_val(val_data)
	return swap_mem, val_data

def execute(command, swap_mem, val_data, transaction_id):
	db_flag = False

	for operation in db_operations:
		if operation in command:
			swap_mem, val_data = db_operate(command.strip().split("(")[1].strip().split(")")[0], operation, swap_mem, val_data, transaction_id)
			db_flag = True


	if not db_flag:
		command = command.strip().split(":=")
		op = command[0].strip()
		for operator in math_operators:
			if operator in command[1]:
				op1, op2 = command[1].strip().split(operator)
				swap_mem = math_operate(op, op1, op2, operator, swap_mem)

	return swap_mem


def undo_log(fileName, cycle):
	f = open(fileName)
	data = f.readlines()
	f.close()

	line_num = 0
	val_data = get_val(data[line_num])
	line_num = 1
	commands = {}
	# because dictionary keys aren't sorted therefore storing transaction order
	trans_order = []

	
	while line_num < len(data):
		if data[line_num].strip() != "":
			transaction_id, num_commands = data[line_num].strip().split()
			
			if transaction_id not in trans_order:
				trans_order.append(transaction_id)
				commands[transaction_id] = []
			else:
				print("Duplicate Transactions")
				sys.exit(0)

			num_commands = int(num_commands)
			while num_commands > 0:
				line_num += 1
				commands[transaction_id].append(data[line_num][:-1])
				num_commands -= 1
		line_num += 1

	register = {}
	swap_mem = {}
	shut_flg = {}
	for tr in commands:
		register[tr] = (0, min(cycle, len(commands[tr])))
		swap_mem[tr] = {}
		shut_flg[tr] = False
	
	while True:
		terminate = True 
		for tr in trans_order:
			total_cmds = len(commands[tr])
			
			if not shut_flg[tr]:
				if register[tr][0] == 0:
					print("<" + tr + ", start>")
					print_val(val_data)

				for command_no in range(register[tr][0], register[tr][1]):
					swap_mem[tr] = execute(commands[tr][command_no], swap_mem[tr], val_data, tr)
	
				register[tr] = (register[tr][0] + cycle, register[tr][1] + cycle)
				
				if register[tr][0] > total_cmds - 1:
					print("<" + tr + ", commit>")
					print_val(val_data)
					shut_flg[tr] = True
				if register[tr][1] > total_cmds:
					register[tr] = (register[tr][0], total_cmds)
			terminate = terminate & shut_flg[tr]
		if terminate:
			break



if __name__ == '__main__':
	undo_log(sys.argv[1], int(sys.argv[2]))
