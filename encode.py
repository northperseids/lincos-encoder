import numpy as np
import pyaudio
import wave
from PIL import Image

p = pyaudio.PyAudio()

# run file. use resize = 3 for images ~600x400.
# resize = 2 for most lincos images?
# duration = 20 for most files

volume = 0.5
rate = 44100
#interv = 0.0016 # hydrogen atom period times 10^13
#interv = 0.016 # hydrogen atom period times 1000000000000000 (10^14)
#duration = 0.1

#freq = 1420.405752 # hydrogen resonance frequency * 10^6

def resize_image(img, div):
    with Image.open(img) as image:
        grayscale = image.convert('L')
        img_width = grayscale.width
        img_height = grayscale.height
        resized = grayscale.resize((img_width//div,img_height//div))
        resized.save('resized.png')

def process_image(img):
    with Image.open(img) as image:
        pixels = list(image.getdata())
        return pixels
    
def make_audio(pix_list, filename, freq, interv, duration):

    audio_array = []

    if freq != 0:
        frequency = freq
    else:
        frequency = 1420.405752

    for i in range(len(pix_list)):
        note = frequency - (pix_list[i] * 2)
        samples = (np.sin(2 * np.pi * np.arange(rate * interv) * note / rate)).astype(np.float32)
        output_bytes = (volume * samples).tobytes()
        audio_array.append(output_bytes)
        if duration != 0:
            if i*interv > duration:
                break

    with wave.open(f'./audios/{filename}', 'w') as f:
        byte_list = b"".join(audio_array)
        f.setnchannels(1)
        f.setsampwidth(4)
        f.setframerate(rate)
        f.writeframes(byte_list)
        print('finished')

select = input('Which file? Input relative path. ./')

resize = input('Resize? (integer; 1 for no resize) ')

resized_image = resize_image(f'./{select}', int(resize))

interv = input('Interval? (in seconds - 0.016 = Ht*10^14 seems to get good results) ')

pixlist = process_image('resized.png')

print(len(pixlist))
print(len(pixlist) * float(interv))

dur = input('Duration? (0 for full duration.) ')

frequen = input('Base frequency? (0 for default 1420.4....) ')

name = input('File name? (Include format suffix.) ')

make_audio(pixlist, name, float(frequen), float(interv), int(dur))