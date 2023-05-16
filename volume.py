from datetime import timedelta
import matplotlib.pyplot as plt
import moviepy.editor as mp
import librosa.display
import soundfile as sf
import numpy as np
import subprocess
import argparse
import os

## define function
def extract_volume(input_file, extension):
    if extension in ['.wav', '.aiff', '.mp3', '.wma', '.flac', '.aac', '.m4a', '.shn', '.ape', '.wv', '.tta', '.spx', 'audio']:
        audio_data, sample_rate = sf.read(input_file)
    elif extension in ['.avi', '.wmv', '.mov', '.qt', '.flv', '.swf', '.mp4', 'm4v', '.m4p', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', 'video']:
        video = mp.VideoFileClip(input_file)
        audio = video.audio
        audio_data, sample_rate = audio.to_soundarray(fps=audio.fps), audio.fps
    else:
        extension = input("Unable to recognize the file type. Is it an audio file or a video file?(audio/video)")
        return extract_volume(input_file, extension)

    db = librosa.amplitude_to_db(audio_data, ref=np.max(audio_data))

    avg_db_per_second = []
    for i in range(0, len(db), sample_rate):
        db_window = db[i:i+sample_rate]
        avg_db = np.mean(db_window)
        avg_db_per_second.append(avg_db)

    return avg_db_per_second

def record_segments(db, threshold, min_silence_duration):
    segments = []
    segment_start = None
    segment_end = None
    
    for i in range(len(db)):
        if db[i] > threshold:
            if segment_start is None :
                segment_start = i
            elif segment_end is not None:
                if i - segment_end >= min_silence_duration:
                    start, end = str(timedelta(seconds = segment_start)), str(timedelta(seconds = segment_end))
                    segments.append((start, end))
                    segment_start, segment_end = i, None
                else:
                    segment_end = None
            else:pass
        else:
            if segment_end is None and segment_start is not None:
                segment_end = i
    
    if segment_end is not None:
        start, end = str(timedelta(seconds = segment_start)), str(timedelta(seconds = segment_end))
    else:
        start, end = str(timedelta(seconds = segment_start)), str(timedelta(seconds = len(db)))
    segments.append((start, end))

    return segments             

def audiograph(db_per_second):
    y = np.array(db_per_second)
    librosa.display.waveshow(y, sr=1, axis='time')
    plt.ylim(np.min(y), np.max(y))
    plt.xlabel('Time(s)')
    plt.ylabel('Vloume(dB)')
    plt.show()

## execute
if __name__ == '__main__':
    ## (part1)
    parser = argparse.ArgumentParser(description='Record silence segments')
    parser.add_argument('--f', type=str, help='input audio file name', required = True)
    #parser.add_argument('--threshold', type=float, help='dB threshold', required = True)
    #parser.add_argument('--duration', type=int, help='minimum silence duration', required = True)

    args = parser.parse_args()
    
    input_file = args.f
    if not os.path.exists(input_file):
        raise argparse.ArgumentTypeError(f"'{input_file}' does not exist")
    _, extension = os.path.splitext(input_file)
    db_per_second = extract_volume(input_file, extension)
    audiograph(db_per_second)
    threshold = int(input("dB Threshold?"))
    duration = int(input("Minimum Silence Duration?"))
    segments = record_segments(db_per_second, threshold, duration)

    ## (part2)
    parts = len(segments)
    for i in range(parts):
        start, end, output_file = segments[i][0], segments[i][1], f"clip{i+1}{extension}"
        cmd = f"ffmpeg -i {input_file} -ss {start} -to {end} -c:a copy -c:v copy {output_file}"
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(output_file):
            print(f"'{output_file}' created successfully!")
        else:
            raise FileNotFoundError(f"\nsome errors occurred while generating '{output_file}'!\n")

