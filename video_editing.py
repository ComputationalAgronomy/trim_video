from datetime import datetime
import subprocess
import argparse
import sys
import re
import os

## define function
def check_file(input_file):
    """
    This function checks if the file name meets the required format and if the input file exists.
    """
    if not input_file.endswith('.txt'):
        raise argparse.ArgumentTypeError("Input file must end with '.txt'")
    if not os.path.exists(input_file):
        raise argparse.ArgumentTypeError(f"'{input_file}' does not exist")
    
    return input_file

## used to generate ordinal numbers(taken from https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712)
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]) 
                                                                                     
def read_file(input_file):
    """
    This function will read the input_file text file that is passed in,and return the 
    {input stream name}, {output stream name list}, {start time list}, and {end time list}.
    """
    with open(input_file, 'r') as f:   
        lines = f.readlines()                                 

        ## record the file names to be input and output
        files = re.findall(r'\b\w+\.\w+\b', lines[0])
        in_stream, out_stream = files[0], files[1:]
        if not os.path.exists(in_stream):
            raise FileNotFoundError(f"'{in_stream}' does not exist.")

        ## store timestamp
        start, end = [], []
        for i in range(1,len(lines)):
            time = re.findall("[0-2][0-3]:[0-5][0-9]:[0-5][0-9]", lines[i])
            ## convert hh:mm:ss strings to seconds
            start_second, end_second = datetime.strptime(time[0], '%H:%M:%S'), datetime.strptime(time[1], '%H:%M:%S')
            ## Is there a start time and an end time, and the start time is earlier than the end time?
            if len(time) == 2 and start_second < end_second:
                start.append(time[0]), end.append(time[1])
                print(f"Successfully read the timestamp on the {ordinal(i+1)} line.")
            elif len(time)==2 and start_second >= end_second:
                will = input(f"Warning! The start time of line {i+1} is later than the end time.\nStart:[{time[0]}] End:[{time[1]}]\nDo you want to swap them and continue?(y/n)")
                if(will=="y"):
                    start.append(time[1]), end.append(time[0])
                    print("Swapping completed.")
                else:
                    sys.exit()
            else:raise ValueError(f"Number of time point(s) is incorrect in line {i+1}, please correct and try again.")

        ## compare the number of output files and the number of timestamps
        if(len(out_stream) == len(start)):
            print("The file has been read completely. Start processing files.....")
        elif(len(out_stream) < len(start)):
            will = input("Warning! The specified output files are less than the timestamp that has been read. \nAre you sure you want to continue?(y/n)")
            if(will=="y"):
                print("Start processing files.....")
            else:
                sys.exit()
        else:
            raise ValueError("The specified output files are more than the timestamp that has been read, please correct and try again.")

        return in_stream, out_stream, start, end

## execute(part1)
parser = argparse.ArgumentParser()
parser.add_argument("--file", type=check_file, help="path to input file, must end with .txt", required = True)
args = parser.parse_args()
in_stream, out_stream, start, end = read_file(args.file)

## execute(part2)
num_time = len(start)
num_out = len(out_stream)
for i in range(num_time):
    try:
        if i < num_out:
            output_file = out_stream[i]
        else:
            output_file = f"output_{i+1}{os.path.splitext(in_stream)[1]}"

        print(f"processing the {ordinal(i+1)} output file...")
        cmd = f"ffmpeg -y -i {in_stream} -ss {start[i]} -to {end[i]} {output_file}"
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(output_file):
            print(f"'{output_file}' created successfully!")
    except:
        
        print(f"\nsome errors occurred while generating '{output_file}'!\n")
