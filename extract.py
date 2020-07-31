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
    prev_url = ""
    fail_count = 0
    content = json.load(open(indexfile))
    saveto = "raw_videos"
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        # random_character2 = random.choice(string.ascii_letters)
        video_url = entry['url']
        if prev_url == video_url:
            print("CONTINUES")
            continue

        sign_name = entry['clean_text']
        sign_name = sign_name.replace(" ", "")
        file_name = sign_name


        if not os.path.exists(saveto + "/" + sign_name):
            os.mkdir(saveto + "/" + sign_name)
        else:
            continue


        ydl_opts = {'outtmpl' : '{}'.format(saveto + "/" + sign_name + "/" + file_name)}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([video_url])
                info_dict = ydl.extract_info(video_url, download=False)
                video_id = info_dict.get("id", None)
                video_ext = info_dict.get("ext", None)
                # cmd = "youtube-dl \"{}\" -o \"{}%(id)s.%(ext)s\"".format(video_url, saveto + "/" + sign_name + os.path.sep)
                # os.system(cmd)
            except:
                fail_count = fail_count + 1
                continue
            
            if video_ext == "webm" :
                format_cmd = "ffmpeg -i {} {}".format(saveto + "/" + sign_name + "/" + file_name + "." + "mkv", saveto + "/" + sign_name + "/" + file_name + "." + "mp4")
                os.system(format_cmd)
                os.remove(saveto + "/" + sign_name + "/" + file_name + "." + "mkv")
                video_ext = "mp4"
        prev_url = video_url



    print(fail_count)

def cut_videos(indexfile):
    content = json.load(open(indexfile))
    prev_sign_name = ""
    r = 0
    saveto = "raw_videos"
    for entry in content:

        sign_name = entry['clean_text']
        sign_name = sign_name.replace(" ", "")

        start_time = entry['start_time']
        end_time = entry['end_time']
        try:
            _, _, files = next(os.walk("{}".format(saveto + "/" + sign_name + "/")))
            file_count = len(files)
        except:
            print("MADNESS")
            file_count= r + 100
            r = r+1
        file_name = sign_name
        new_file_name = sign_name + str(file_count)

        if prev_sign_name != sign_name and prev_sign_name!="":
            try:
                os.remove(saveto + "/" + prev_sign_name + "/" + prev_file_name + "." + "mp4")
            except:
                pass

        print(sign_name)
        if int(start_time)>=10 and int(start_time) < 60 :
            start_time = "00:00:{}".format(start_time)
        elif int(start_time)>=60 :
            hours = start_time // 3600
            start_time = start_time - hours * 3600
            minutes = start_time // 60
            seconds = start_time - minutes * 60
            if minutes >= 10:
                start_time ="0{}:{}:{}".format(hours,minutes,seconds)
            else:
                start_time ="0{}:0{}:{}".format(hours,minutes,seconds)
            
        else:
            start_time = "00:00:0{}".format(start_time)
        
        if int(end_time)>=10 and int(end_time) < 60:
            end_time = "00:00:{}".format(end_time)
        elif int(end_time)>=60 :
            hours = end_time // 3600
            end_time = end_time - hours * 3600
            minutes = end_time // 60
            seconds = end_time - minutes * 60
            if minutes >= 10:
                end_time ="0{}:{}:{}".format(hours,minutes,seconds)
            else:
                end_time ="0{}:0{}:{}".format(hours,minutes,seconds)
        else:
            end_time = "00:00:0{}".format(end_time)
        
        try:
            ffm_cmd = "ffmpeg -ss {} -i {} -to {} -an -c copy {}".format(start_time, saveto + "/" + sign_name + "/" + file_name + "." + "mp4", end_time, saveto + "/" + sign_name + "/" + new_file_name + ".mp4")
            os.system(ffm_cmd)
            # os.remove(saveto + "/" + sign_name + "/" + file_name + "." + "mp4")
        except:
            print("ERRRROOOORRR")
            continue
        prev_sign_name = sign_name
        prev_file_name = file_name


if __name__ == '__main__':
    download_yt_videos('extraction_test.json')
    cut_videos('extraction_test.json')