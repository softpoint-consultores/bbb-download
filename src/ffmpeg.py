__author__ = 'CreateWebinar.com, softpoint.es'
__email__ = 'support@createwebinar.com, info@softpoint.es'

# Python wrapper around the ffmpeg utility
import os
import shutil

# FFMPEG = 'ffmpeg'
FFMPEG = '/opt/ffmpeg/ffmpeg'
# FFMPEG = '/root/bin/ffmpeg'
VID_ENCODER = 'libx264'


def set_logfile(file):
    global logfile
    logfile = file


def mux_slideshow_audio(video_file, audio_file, out_file):
    command = '%s -i %s -i %s -map 0 -map 1 -codec copy -shortest %s 2>> %s' % (
        FFMPEG, video_file, audio_file, out_file, logfile)
    os.system(command)


def extract_audio_from_video(video_file, out_file):
    command = '%s -i %s -ab 160k -ac 2 -ar 44100 -vn %s 2>> %s' % (FFMPEG, video_file, out_file, logfile)
    os.system(command)


def create_video_from_image(image, duration, out_file):
    print('*'*15 + 'create_video_from_image' + '*'*15)
    print(image, duration, out_file, sep='\n')
    command = '%s -loop 1 -r 5 -f image2 -i %s -c:v %s -t %s -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" %s 2>> %s' % (
        FFMPEG, image, VID_ENCODER, duration, out_file, logfile)
    os.system(command)


def concat_videos(video_list, out_file):
    command = '%s -f concat -safe 0 -i %s -c copy %s 2>> %s' % (FFMPEG, video_list, out_file, logfile)
    os.system(command)


def mp4_to_ts(input, output):
    command = '%s -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s 2>> %s' % (FFMPEG, input, output, logfile)
    os.system(command)


def concat_ts_videos(input, output):
    command = '%s -i %s -c copy -bsf:a aac_adtstoasc %s 2>> %s' % (FFMPEG, input, output, logfile)
    os.system(command)


def rescale_image(image, height, width, out_file):
    if height < width:
        command = '%s -i %s -vf pad=%s:%s:0:oh/2-ih/2 %s -y 2>> %s' % (FFMPEG, image, width, height, out_file, logfile)
    else:
        command = '%s -i %s -vf pad=%s:%s:0:ow/2-iw/2 %s -y 2>> %s' % (FFMPEG, image, width, height, out_file, logfile)

    os.system(command)


def trim_video(video_file, start, end, out_file):
    command = '%s -ss %d -t %d -i %s -vcodec copy -acodec copy %s 2>> %s' % (
        FFMPEG, start, end, video_file, out_file, logfile)
    os.system(command)


def trim_video_by_seconds(video_file, start, end, out_file):
    command = '%s -ss %s -i %s -c copy -t %s %s 2>> %s' % (FFMPEG, start, video_file, end, out_file, logfile)
    os.system(command)


def trim_audio(audio_file, start, end, out_file):
    temp_file = 'temp.mp3'

    command = '%s -ss %d -t %d -i %s %s 2>> %s' % (FFMPEG, start, end, audio_file, temp_file, logfile)

    os.system(command)
    mp3_to_aac(temp_file, out_file)
    os.remove(temp_file)


def trim_audio_start(dictionary, length, full_audio, audio_trimmed):
    times = list(dictionary.keys())
    times.sort()
    trim_audio(full_audio, int(round(times[0])), int(length), audio_trimmed)


def trim_video_start(dictionary, length, full_vid, video_trimmed):
    times = list(dictionary.keys())
    times.sort()
    trim_video(full_vid, int(round(times[2])), int(length), video_trimmed)


def mp3_to_aac(mp3_file, aac_file):
    command = '%s -i %s -c:a libfdk_aac %s 2>> %s' % (FFMPEG, mp3_file, aac_file, logfile)
    os.system(command)


def webm_to_mp4(webm_file, mp4_file):
    command = '%s -i %s -qscale 0 %s 2>> %s' % (FFMPEG, webm_file, mp4_file, logfile)
    os.system(command)


def audio_to_video(audio_file, image_file, video_file):
    command = '%s -loop 1 -i %s -i %s -c:v libx264 -tune stillimage -c:a libfdk_aac -pix_fmt yuv420p -shortest %s' % (
    FFMPEG, image_file, audio_file, video_file)
    os.system(command)
