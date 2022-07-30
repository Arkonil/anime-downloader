import subprocess

def ts_to_mp4(*input_files, output_file):

    inputs = []
    for file in input_files:
        inputs.extend(['-i', file])

    subprocess.run([
        'ffmpeg', 
        *inputs, 
        '-c:v', 'copy', 
        '-c:a', 'aac', 
        '-loglevel', 'quiet',
        '-stats',
        output_file])
