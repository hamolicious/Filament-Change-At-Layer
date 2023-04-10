# Filament Change At Layer
A simple python script that will allow you to insert some GCODE for manual colour changing, useful for prints with text at the top layer that you may want printed in a different colour.

## Usage
I am 90% sure this will only work for Cura slicer and so once you have sliced your model, figure out what layer you want to change filament at (this can be done using the layer slider in preview mode).

![layer-slider](https://i.ibb.co/wKjpR2K/image.png)

Once you have a desired layer, say 10 for example, you will then simply say:
```bash
python main.py my_sliced_model.gcode 10
```
This will give you a file that will be named `my_sliced_model-filament-change-at-10.gcode`. The printer will then continuously print until the layer you specified when it will move over, expel the currently loaded filament and pause the print indefinitely, you are then able to load in the new filament and click continue and the printer will purge the old filament out and resume your print now with a new colour.

## Caveats and Things to think about
1. This is **not** a multi-coloured printing solution per se, instead, you can only change filament at a given layer meaning that you cannot print multi colour models (unless the multiple colours are all set out between separate layers)
2. Your printer *may* disable steppers if it has been sat around for a while, this can mean that you are able to accidentally knock the Z carnage out of alignment and your entire print is unsalvageable.

