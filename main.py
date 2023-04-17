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

index = file_data.index(f';LAYER:{layer}')

# Backtrack until you find G1 command with E steps (I know its ugly, bite me)
i = index
while True:
	i -= 1
	if file_data[i:i+2].startswith('G1'):
		command = ''
		j = 0
		while True:
			if file_data[i+j] == '\n':
				break
			command += file_data[i+j]
			j += 1

		if 'e' not in command.lower():
			continue
		e_steps = command[command.lower().index('e')+1::].split(' ')[0]

		if not ('.' in e_steps and e_steps.replace('.', '').isdigit()):
			print(f'[ERROR] Shoot, something went wrong, "{e_steps}" is not a valid value for E steps')

		break

path = os.path.join(this_dir, 'notif_bleep.gcode')
if os.path.exists(path):
	with open(path, 'r') as f:
		notif_tune = f.read()
else:
	notif_tune = ''

home_code = 'G28              ; Home printer' if home else ''
inserted_gcode = inserted_gcode.format(
	dump_fil_f=settings.DUMP_FILAMENT_F,
	purge_f=settings.PURGE_F,
	purge_len=settings.PURGE_LENGTH,
	dump_len=settings.DUMP_LENGTH,
	home=home_code,
	old_e_steps=e_steps,
	notif_tune=notif_tune,
)

file_data = file_data[:index:] + inserted_gcode + file_data[index::]

new_filename = file.split('.')[0] + f'-filament-change-at-{layer}.' + file.split('.')[-1]
with open(os.path.join(cwd, new_filename), 'w') as f:
	f.write(file_data)

