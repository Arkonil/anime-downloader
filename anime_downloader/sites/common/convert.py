import os
import subprocess


def run_ffmpeg(*args, output_file):
    command = ['ffmpeg', ' '.join(args), '-loglevel', 'quiet', '-stats', f'"{output_file}"']
    command = ' '.join(command)
    subprocess.run(command, shell=True)


def ts_to_mp4(input_files, output_file):
    current_directory = os.getcwd()
    files_directory = [os.path.dirname(p) for p in input_files.values()]

    if len(set(files_directory)) != 1:
        raise ValueError(f"All files are not in the same directory:\n{input_files}")
    
    os.chdir(files_directory[0])

    if video := input_files.get('video'):
        video = os.path.basename(video)

    if audio := input_files.get('audio'):
        audio = os.path.basename(audio)
    
    if subtitle := input_files.get('subtitle'):
        subtitle = os.path.basename(subtitle)

    """
    video audio subtitle        commands  
      ✅    ✅     ✅            -vf subtitles=subtitle.srt
      ✅    ❌     ✅            -vf subtitles=subtitle.srt
      ✅    ✅     ❌            -c:v copy -c:a aac
      ✅    ❌     ❌            -c:v copy -c:a aac
    """

    if subtitle:
        if audio:
            run_ffmpeg('-i', video, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', output_file=video)

        run_ffmpeg('-i', f'"{video}"', '-vf', f'subtitles="{subtitle}"', output_file=output_file)
    else:
        if audio:
            run_ffmpeg('-i', video, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', output_file=output_file)
        else:
            run_ffmpeg('-i', video, '-c:v', 'copy', '-c:a', 'aac', output_file=output_file)

    os.chdir(current_directory)


if __name__ == '__main__':
    ts_to_mp4({
        'video': 'E:/Anime/video.ts',
        'subtitle': 'E:/Anime/subtitle.vtt'
    }, "E:/Anime/video.mp4")
