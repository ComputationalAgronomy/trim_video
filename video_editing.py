from sys import argv
import numpy as np
import subprocess
import os

script, input_file, = argv

## part1
def rf(input_file):
    """This function will read the input_file text file that is passed in,and return the 
    {input stream name}, {output stream name list}, {start time list}, and {end time list}."""
    with open(input_file, 'r') as f:
        ## read file as a list   
        lines = f.readlines()                                 

        ## record the file names to be input and output
        in_stream, out_stream = lines[0].split("    ")
        out_stream = out_stream.strip().split(", ")

        ## create two zero-lists to store start and end times
        start = []
        end = []
        ## store time point 
        for line in lines[1:]:
            s, e = line.strip().split("    ")
            start.append(s)
            end.append(e)

        return in_stream, out_stream, start, end

## categorize elements from input_file
in_stream, out_stream, start, end = rf(input_file)

## part2
num_files = len(out_stream)
print(f"\nYou're going to trim '{in_stream}' into {num_files} part(s), right?")
input("if YES, press ENTER, rather press CTRL^C...\n")

for i in range(num_files):
    try:
        print(f"processing the {i+1}th output file...")

        ## construct the trimming command using ffmpeg
        cmd = f"ffmpeg -y -i {in_stream} -ss {start[i]} -to {end[i]} {out_stream[i]}"
        ## execute the command using subprocess.run
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ## check whether the output success
        if os.path.exists(out_stream[i]):
            print(f"'{out_stream[i]}' created successfully!\n")
    except:
        
        print(f"some errors occurred while generating '{out_stream[i]}'!\n")
		 

