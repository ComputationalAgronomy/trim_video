from datetime import datetime
import subprocess
import argparse
import sys
import re
import os

## define function
def check_file(input_file):
    """This function checks if the file name meets the required format and if the input file exists."""
    if not input_file.endswith('.txt'): # if not meet the required format
        print("Warning! Input file must end with '.txt'.")
        sys.exit()
    
    if not os.path.exists(input_file): # if not exist
        print(f"Warning! '{input_file}' does not exist.")    
        sys.exit()

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

def rf(input_file):
    """This function will read the input_file text file that is passed in,and return the 
    {input stream name}, {output stream name list}, {start time list}, and {end time list}."""
    with open(input_file, 'r') as f:   
        lines = f.readlines()                                 

        ## record the file names to be input and output
        files = re.findall(r'\b\w+\.\w+\b', lines[0])
        in_stream, out_stream = files[0], files[1:]
        if not os.path.exists(in_stream):
            print(f"Warning! '{in_stream}' does not exist.")
            sys.exit()

        ## store timestamp
        start, end = [], []
        for i in range(1,len(lines)):
            time = re.findall("[0-2][0-3]:[0-5][0-9]:[0-5][0-9]", lines[i])
            start_obj, end_obj = datetime.strptime(time[0], '%H:%M:%S'), datetime.strptime(time[1], '%H:%M:%S')
            if len(time)==2 and start_obj<end_obj:
                start.append(time[0])
                end.append(time[1])
                print(f"Successfully read the timestamp on the {ordinal(i+1)} line.")
            elif len(time)==2 and start_obj>=end_obj:
                will = input(f"Warning! The start time of line {i+1} is greater than the end time.\nStart:[{time[0]}] End:[{time[1]}]\nDo you want to swap them and continue?(y/n)") 
                if(will=="y"):
                    start.append(time[1])
                    end.append(time[0])
                    print("Swapping completed.")
                else:sys.exit()
            else:
                print(f"Warning! Number of time point(s) is incorrect in line {i+1}, please correct and try again.")
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

## execute(part1)
parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, help="path to input file, must end with .txt", required = True)
args = parser.parse_args()
check_file(args.file)
in_stream, out_stream, start, end = rf(args.file)

## execute(part2)
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
            print(f"'{out_stream[i]}' created successfully!")
    except:
        
        print(f"\nsome errors occurred while generating '{out_stream[i]}'!\n")
		 

