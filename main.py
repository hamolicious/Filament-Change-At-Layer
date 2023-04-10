import sys
import os
import settings

cwd = os.getcwd()
this_dir = '/'.join(__file__.replace('\\', '/').split('/')[:-1:]) + '/'

def help():
	filename = os.path.basename(__file__)
	lines = [
		'',
		f'Usage: python {filename} <filename> <layer> <home>',
		'\t - `filename` the name of the GCODE file',
		'\t - `layer` the layer to perform the filament change on',
		'\t - `home` "true" if you want the printer to home after the change',
	]
	return '\n'.join(lines)

if len(sys.argv) < 3:
	print(help())
	quit()

file = sys.argv[1]
layer = sys.argv[2]
home = False
if len(sys.argv) == 4:
	home = sys.argv[3].lower() == 'true'

if not layer.isdigit():
	print(help())
	quit()

layer = int(layer)

with open(os.path.join(cwd, file), 'r') as f:
	file_data = f.read()

with open(os.path.join(this_dir, 'swap.gcode'), 'r') as f:
	inserted_gcode = f.read()

home_code = 'G28              ; Home printer' if home else ''
inserted_gcode = inserted_gcode.format(
	dump_fil_f=settings.DUMP_FILAMENT_F,
	purge_f=settings.PURGE_F,
	purge_len=settings.PURGE_LENGTH,
	dump_len=settings.DUMP_LENGTH,
	home=home_code,
)

index = file_data.index(f';LAYER:{layer}')

file_data = file_data[:index:] + inserted_gcode + file_data[index::]

new_filename = file.split('.')[0] + f'-filament-change-at-{layer}.' + file.split('.')[-1]
with open(os.path.join(cwd, new_filename), 'w') as f:
	f.write(file_data)

