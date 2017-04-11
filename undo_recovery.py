import sys

def print_val(val_data):
	val_order = sorted(val_data)
	for val in val_order:
		print(val, str(val_data[val]), end='')
		if val_order.index(val) != len(val_order) - 1:
			print(" ", end='')
	print()

def get_val(data):
	val_data = {}
	data = data.strip().split()
	for index in range(0, len(data), 2):
		val_data[data[index]] = int(data[index + 1])
	return val_data

def undo_recover(fileName):
	f = open(fileName)
	data = f.readlines()
	f.close()

	val_data = get_val(data[0])
	data = list(reversed(data[1:]))
	ignore_tr = []

	flag = False
	for line in data:
		line = line[:-1].strip()
		if line != "":
			if len(line.split(",")) == 3:
				tr, element, val = line.split(",")
				tr = tr.split("<")[1].strip()
				element = element.strip()
				val = int(val.split(">")[0].strip())
				if not tr in ignore_tr:
					val_data[element] = val
			elif "commit" in line:
				line = line.split(",")
				ignore_tr.append(line[0].split("<")[1])
			elif line == "<end ckpt>":
				flag = True
			elif "<start ckpt" in line:
				break

	print_val(val_data)

if __name__ == '__main__':
	undo_recover(sys.argv[1])