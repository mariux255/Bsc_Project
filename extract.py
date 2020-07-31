import os
import json
import time
import sys
import urllib.request
import youtube_dl
import string
import random
from multiprocessing.dummy import Pool

def download_yt_videos(indexfile):
    failed_list = []
    prev_url = ""
    prev_sign_name = ""
    prev_file_name = ""
    fail_count = 0
    content = json.load(open(indexfile))
    saveto = "raw_videos"
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        # random_character2 = random.choice(string.ascii_letters)
        video_url = entry['url']
        sign_name = entry['clean_text']
        sign_name = sign_name.replace(" ", "")
        file_name = sign_name
        start_time = entry['start_time']
        end_time = entry['end_time']

        if not os.path.exists(saveto + "/" + sign_name):
            os.mkdir(saveto + "/" + sign_name)

        if prev_url == video_url:
            # cut video
            cut_videos(saveto, sign_name, start_time, end_time)
            
        else:
            # download and cut video
            try:
                download_video(video_url,sign_name,file_name,saveto)
            except:
                continue

            try:
                cut_videos(saveto,sign_name,start_time, end_time)
            except:
                failed_list.append(sign_name)
                continue

            try:
                os.remove(saveto + "/" + prev_sign_name + "/" + prev_file_name + "." + "mp4")
            except:
                pass

        prev_sign_name = sign_name
        prev_file_name = sign_name
        prev_url = video_url
    print(failed_list)


def download_video(video_url, sign_name, file_name, saveto):
    ydl_opts = {'outtmpl': '{}'.format(
        saveto + "/" + sign_name + "/" + file_name)}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        
        ydl.download([video_url])
        info_dict = ydl.extract_info(video_url, download=False)
        video_ext = info_dict.get("ext", None)
        # cmd = "youtube-dl \"{}\" -o \"{}%(id)s.%(ext)s\"".format(video_url, saveto + "/" + sign_name + os.path.sep)
        # os.system(cmd)
        if video_ext == "webm":
            format_cmd = "ffmpeg -i {} {}".format(saveto + "/" + sign_name + "/" + file_name +
                                                  "." + "mkv", saveto + "/" + sign_name + "/" + file_name + "." + "mp4")
            os.system(format_cmd)
            os.remove(saveto + "/" + sign_name +
                      "/" + file_name + "." + "mkv")
            video_ext = "mp4"


def cut_videos(saveto, sign_name, start_time, end_time):
    try:
        _, _, files = next(os.walk("{}".format(saveto + "/" + sign_name + "/")))
        file_count = len(files)
    except:
        print("MADNESS")
        file_count = 100

    file_name = sign_name
    new_file_name = sign_name + str(file_count)

    d_time = reformat_time((end_time - start_time))
    start_time = reformat_time(start_time)
    end_time = reformat_time(end_time)

           

    ffm_cmd = "ffmpeg -ss {} -t {} -i {}  -an -c copy {}".format(start_time, d_time, saveto + "/" + sign_name + "/" + file_name + "." + "mp4", saveto + "/" + sign_name + "/" + new_file_name + ".mp4")
    os.system(ffm_cmd)
    # os.remove(saveto + "/" + sign_name + "/" + file_name + "." + "mp4")



def reformat_time(time):
    if int(time)>=10 and int(time) < 60:
        time = "00:00:{}".format(time)
    elif int(time)>=60 :
        hours = time // 3600
        time = time - hours * 3600
        minutes = time // 60
        seconds = time - minutes * 60
        if minutes >= 10:
            time ="0{}:{}:{}".format(hours,minutes,seconds)
        else:
            time ="0{}:0{}:{}".format(hours,minutes,seconds)
    else:
        time = "00:00:0{}".format(time)
    return time


if __name__ == '__main__':
    download_yt_videos('extraction_test.json')