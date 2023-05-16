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

        ## record the file names to be input
        file = re.findall(r'\b\w+\.\w+\b', lines[0])
        in_stream = file[0]
        if not os.path.exists(in_stream):
            raise FileNotFoundError(f"'{in_stream}' does not exist.")

        start, end, out_stream = [], [], []
        for i in range(1,len(lines)):
            ## record the file names to be output
            file = re.findall(r'\b\w+\.\w+\b', lines[i])
            if len(file) == 0:
                out_stream.append([])
            else:
                out_stream.append(file[0])
            
            ## record the timestamps
            time = re.findall("[0-2][0-3]:[0-5][0-9]:[0-5][0-9]", lines[i])
            ## check whether timestamp make sense
            if time and len(time) == 2:
                start_obj, end_obj = datetime.strptime(time[0], '%H:%M:%S'), datetime.strptime(time[1], '%H:%M:%S')
                if start_obj <= end_obj:
                    start.append(time[0]), end.append(time[1])
                    print(f"Successfully read the timestamp on the {ordinal(i+1)} line.")
                else:
                    will = input(f"Warning! The start time of line {i+1} is later than the end time.\nStart:[{time[0]}] End:[{time[1]}]\nDo you want to swap them and continue?(y/n)")
                    if(will=="y"):
                        start.append(time[1]), end.append(time[0])
                        print("Swapping completed.")
                    else:
                        sys.exit()
            else:
                raise ValueError(f"Warning! Number of timestamp is incorrect in line {i+1}, please correct and try again.")

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
        if out_stream[i] == [] :
            output_file = f"output_{i+1}{os.path.splitext(in_stream)[1]}"
        else:
            output_file = out_stream[i]

        print(f"processing the {ordinal(i+1)} output file...")
        cmd = f"ffmpeg -i {in_stream} -ss {start[i]} -to {end[i]} -c:a copy -c:v copy {output_file}"
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(output_file):
            print(f"'{output_file}' created successfully!")
        else:
            raise FileNotFoundError(f"\nsome errors occurred while generating '{output_file}'!\n")
    except:
        print(f"\nsome errors occurred while generating '{output_file}'!\n")
