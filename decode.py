import numpy as np
from PIL import Image
import crepe # type: ignore
import os
import pandas as pd

width = int(input('Width? '))
height = int(input('Height? '))

freq = 1420.405752 # hydrogen resonance frequency * 10^6

regen = input('Regenerate frequency list? y/n ')

if regen == 'y':
    fileinput = input('Which file? (WAV file - include suffix) ')
    file = os.path.join(os.path.dirname(__file__), f'audios/{fileinput}')
    step_input = input('Step size? (in Seconds) ')
    step = float(step_input) * 1000
    crepe.process_file(file, model_capacity='medium', step_size=step, output='./audios')

def divide_chunks(array, chunk_size):
    arr = []
    for i in range(0, len(array), chunk_size):
            x = i
            arr.append(array[x:x+chunk_size])
    return arr

def make_image(file_path):

    image = Image.new('L', (width, height))

    with open(file_path, 'r') as file:
        data = np.genfromtxt(file, delimiter=',')

        frequencies = data[:,1]

        freq_list = list(divide_chunks(frequencies, width))

    minimum = list(map(min, *freq_list))[1]
    maximum = list(map(max, *freq_list))[1]

    for y in range(1, height-1):
        for x in range(1, width-1):
            #num = row[x]
            mapped = round(np.interp(freq_list[y][x], [minimum, maximum], [0,255]))
            #mapped = round(freq - num)
            image.putpixel((x,y), mapped)

    filename = input('Save file name? (Include .jpg at end)')

    image.save(f'./images/decoded_and_originals/{filename}')

csv_file = input('CSV path? ./audios/')

make_image(f'./audios/{csv_file}')