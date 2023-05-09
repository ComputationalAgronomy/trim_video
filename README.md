# Introduction
This project is for batch processing video files that allows users to quickly split a longer video file into multiple shorter parts, and the start and end time of each part are specified by a text file.

# Usage Instructions
This project is designed to be used in conjunction with a text file. Therefore, the format of the text will be explained below:

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

Part1 of the code defines a function called "rf" which reads the data from a text file and categorizes it into a string and three lists: "input stream name", [output stream name list], [start time list], and [end time list]. The function opens the input file, reads its contents as a list of lines, extracts the input and output file names, and creates two lists to store the start and end times. 

Part2 of the code uses the ffmpeg tool to split a video file into multiple parts. It uses the data returned by the "rf" function and a for loop to go through all the parts of the video that need to be outputted and uses subprocess to run ffmpeg commands. If the cutting is successful, the program will output a success message. Otherwise, the program will output an error message.

# Technical Details
[FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)

[Subprocess](https://docs.python.org/3/library/subprocess.html)

[Argparse](https://docs.python.org/3/library/argparse.html)

[Reg Expression](https://www.w3schools.com/python/python_regex.asp)
