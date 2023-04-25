# Introduction
This project is for batch processing video files that allows users to quickly split a longer video file into multiple shorter parts, and the start and end time of each part are specified by a text file.

# Usage Instructions
This project is designed to be used in conjunction with a text file. Therefore, the format of the text will be explained below:

1. The first line of the text file should record the input file name and output file name(s), separated by a tab, where multiple output file names are separated by a comma and a space (", "). 
2. Starting from the second line, each line records the start and end time of an output file, separated by a tab. All times should be in the format of hh:mm:ss. (PS: the number of output files and starting/ending time points must be match)

Here is a sample text file:
```txt
input_flie.mp4    output_file1.mp4, output_file2.mp4
00:00:00    00:02:05
00:01:23    00:03:21
```

When you have completed your text file, you can use the program on the terminal according to the following code:

```cmd
python vedio_editing.py XXXXX.txt
```

# How It Work
For code, please click *video_editing.py*.

Part1 of the code defines a function called "rf" which reads the data from a text file and categorizes it into a string and three lists: "input stream name", [output stream name list], [start time list], and [end time list]. The function opens the input file, reads its contents as a list of lines, extracts the input and output file names, and creates two lists to store the start and end times. 

Part2 of the code uses the ffmpeg tool to split a video file into multiple parts. It uses the data returned by the "rf" function and a for loop to go through all the parts of the video that need to be outputted and uses subprocess to run ffmpeg commands. If the cutting is successful, the program will output a success message. Otherwise, the program will output an error message.

# Technical Details
[FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)

[Subprocess](https://docs.python.org/3/library/subprocess.html)
