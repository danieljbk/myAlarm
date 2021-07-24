# import all modules that come with python
import os
import time
import glob

# auto-import modules that require additional installation
try:
    import osascript
except ImportError:
    print("Installing the osascript module...\n")
    os.system('python -m pip3 install osascript')
    os.system('python -m pip install osascript')

try:
    import simpleaudio as sa
except ImportError:
    print("Installing the simpleaudio module...\n")
    os.system('python -m pip3 install simpleaudio')
    os.system('python -m pip install simpleaudio')

import osascript
import simpleaudio as sa

indent = "    * "


def max_volume():
    osascript.osascript("set volume output volume 100")


def play_audio(file_paths=list, minutes_repeated_for=int): # play audio files in list
    global indent

    print("–––")
    print()
    print("Let's Get It Started!")
    print()
    
    max_volume()
    for file_path in file_paths:
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        file_name = file_path[int('-'+str(list(reversed(list(file_path))).index('/'))):]
        
        now_playing = "Now Playing"
        if minutes_repeated_for != 0:
            now_playing += f" for {minutes_repeated_for} Minute"
        if minutes_repeated_for > 1:
            now_playing += 's'
        print(now_playing + ':')
        print(file_name)
        wave_obj.play().wait_done() # play the audio file & wait until it fully plays
        print(indent + "Played 1 time...", end="\r")
        
        if minutes_repeated_for != 0:
            start = time.time()
            play_count = 1
            while time.time() - start < 60*minutes_repeated_for:
                max_volume()
                wave_obj.play().wait_done()
                play_count += 1
                print(indent + "Played", play_count, "times...", end="\r")
        
        print()
        print()
    print("Launch sequence complete.")
    print()


def setup_time(): # when running the script, the user sets the audio to play after a certain time.
    global indent
    
    print('\n'+('*'*75+'\n')*3)
    print("Set Alarm to Play In:")
    hours = input(indent + "Hours: ")
    if not hours:
        hours = '0'
    hours = int(hours)
    minutes = input(indent + "Minutes: ")
    if not minutes:
        minutes = '0'
    minutes = list(minutes)
    if '.' in minutes: # if the minutes input is not an integer
        minutes = float(''.join(minutes))
    else:
        minutes = int(''.join(minutes))
    total_seconds = 60*60*hours + round(60*minutes)
    print()
    print("Repeat Each Audio File for How Many Minutes?:")
    times_to_repeat = input(indent)
    if not times_to_repeat:
        times_to_repeat = '0'
    times_to_repeat = int(times_to_repeat)
    print()
    print(f"Alarm will play in {hours} hours, {int(minutes)} minutes, and {total_seconds % 60} seconds.")
    print()
    
    for x in range(0, total_seconds+1):
        b = str(total_seconds - x) + " seconds left..."
        print(b, end='\r')
        time.sleep(1)
    print()
    print()
    
    return times_to_repeat


# replace '\' because Terminal adds the backslash character before spacing when retrieving file paths
folder_location = input("Drag the folder with audio files into the Terminal.\n").strip().replace('\\', '')
extension = "/*.wav"
morningcalls = list(reversed(glob.glob( # reversed because glob reads 3-2-1 and not 1-2-3
    folder_location+extension)))

if morningcalls:
    times_to_repeat = setup_time()
    while True:
        play_audio(morningcalls, times_to_repeat)
else:
    print(f"No files with the extension '.wav' were found inside {folder_location}.")
    exit()
