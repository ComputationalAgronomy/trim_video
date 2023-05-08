import subprocess
import argparse
import sys
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, help="path to input file, must end with .txt", required = True)
args = parser.parse_args()

if args.file.endswith('.txt'):
    if os.path.exists(args.file): pass
    else:
        print(f"Warning! '{args.file}' does not exist.")    
        sys.exit()
else:
    print("Input file must end with '.txt'.")
    sys.exit()

## part1
def rf(input_file):
    """This function will read the input_file text file that is passed in,and return the 
    {input stream name}, {output stream name list}, {start time list}, and {end time list}."""
    with open(input_file, 'r') as f:   
        lines = f.readlines()                                 

        ## record the file names to be input and output
        files = re.findall(r'\b\w+\.\w+\b', lines[0])
        in_stream, out_stream = files[0], files[1:]

        ## store time point 
        start, end = [], []
        for i in range(1,len(lines)):
            time = re.findall("[0-2][0-3]:[0-5][0-9]:[0-5][0-9]", lines[i])
            if(len(time)==2):
                start.append(time[0])
                end.append(time[1])
                print(f"Successfully read the timestamp in line {i+1}.")
            else:
                input(f"Warning! Number of time point(s) is incorrect in line {i+1}, please correct and try again.")
                sys.exit() 

        if(len(out_stream) == len(start)):
            print("The file has been read completely. Start processing files.....")
        elif(len(out_stream) < len(start)):
            will = input("Warning! The specified output files are less than the timestamp that has been read. \nAre you sure you want to continue?(y/n)")
            if(will=="y"):print("Start processing files.....")
            else:sys.exit()
        else:
            print("Warning! The specified output files are more than the timestamp that has been read, please correct and try again.")
            sys.exit()

        return in_stream, out_stream, start, end

## categorize elements from input_file
in_stream, out_stream, start, end = rf(args.file)

## part2
num_time = len(start)
for i in range(num_time):
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
		 

