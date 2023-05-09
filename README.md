# Introduction
This project is for batch processing video files that allows users to quickly split a longer video file into multiple shorter parts, and the start and end time of each part are specified by a text file.

# Usage Instructions
This project is designed to be used in conjunction with a text file. Therefore, the format of the text file will be explained below:

The first line indicates the name of the input file, which should be in the format of **{filename.filetype}**. Starting from the second line, each line contains information about a time interval, including the start time, end time, and the output file name(optional). The time is specified in the format of **{hh:mm:ss}**. The output file name is optional, which should also be in the format of {filename.filetype}. If no output file name is specified, the default name will be **{output_{ith}.{input_filetype}**. The order of the time intervals and output file names will not affect the reading of the file, and the order of start and end can be corrected during program runtime even if it is inverted.

Here is a sample text file:
```txt
input_flie.mp4
00:00:00    00:02:05    output1.mp4
00:01:23    00:03:21    output2.mp4
```

When you have completed your text file, you can use the program on the terminal according to the following code:

```cmd
python video_editing.py --file XXXX.txt
```

# How It Work
For code, please click [video_editing.py](https://github.com/ComputationalAgronomy/trim_video/blob/main/video_editing.py).

The code can be divided into three parts:

The first part defines two functions, check_file(input_file) and read_file(input_file). The check_file function checks if the file name meets the requirements and if the file exists. The read_file function reads the text file inputted by the user and extracts information such as the media file to be processed, start and end time, and output media file name. If there are issues with the timestamps, a prompt will be given and the program will terminate.

The second part uses the argparse module to handle the arguments inputted by the user from the command line. The arguments are then passed to the read_file() function, and the results returned by the function are stored in variables.

The third part is the main processing procedure, which uses a for loop to process each media file to be outputted, and uses the ffmpeg library for trimming and outputting. After the trimming is complete, the program checks if the output file exists. If it exists, a  message is displayed, otherwise an error message is displayed.

# Technical Details
[FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)

[Subprocess](https://docs.python.org/3/library/subprocess.html)

[Argparse](https://docs.python.org/3/library/argparse.html)

[Reg Expression](https://www.w3schools.com/python/python_regex.asp)
