import sys
import os

cwd = os.getcwd()
this_dir = '/'.join(__file__.replace('\\', '/').split('/')[:-1:]) + '/'

def help():
	filename = os.path.basename(__file__)
	lines = [
		'',
		f'Usage: python {filename} <filename> <layer>',
		'\t - `filename` the name of the GCODE file',
		'\t - `layer` the layer to perform the filament change on',
	]
	return '\n'.join(lines)

if len(sys.argv) != 3:
	print(help())
	quit()

file = sys.argv[1]
layer = sys.argv[2]

if not layer.isdigit():
	print(help())
	quit()

layer = int(layer)

with open(os.path.join(cwd, file), 'r') as f:
	file_data = f.read()

with open(os.path.join(this_dir, 'swap.gcode'), 'r') as f:
	inserted_gcode = f.read()

index = file_data.index(f';LAYER:{layer}')

file_data = file_data[:index:] + inserted_gcode + file_data[index::]

new_filename = file.split('.')[0] + f'-filament-change-at-{layer}.' + file.split('.')[-1]
with open(os.path.join(cwd, new_filename), 'w') as f:
	f.write(file_data)

