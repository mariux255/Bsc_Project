import os
import json
import time
import sys
import urllib.request
import youtube_dl
import string
import random
from multiprocessing.dummy import Pool
from urllib.parse import urlparse, parse_qs

def download_yt_videos(indexfile):
    failed_list = []
    url_list = []
    id_list = []

    content = json.load(open(indexfile))
    saveto = "originals"
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        video_url = entry['url']
        url_list.append(video_url)
        
    url_list = list(set(url_list))


    for url in url_list:
        video_id = extract_video_id(url)
        id_list.append(video_id)
        if video_id == None:
            failed_list.append(url)
            continue
        if not os.path.exists(saveto + "/" + video_id):
            os.mkdir(saveto + "/" + video_id)
        else:
            continue
        ydl_opts = {'outtmpl': '{}'.format(saveto + "/" + video_id + "/" + video_id)}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                video_ext = info_dict.get("ext", None)

                ydl.download([url])
                # cmd = "youtube-dl \"{}\" -o \"{}%(id)s.%(ext)s\"".format(video_url, saveto + "/" + sign_name + os.path.sep)
                # os.system(cmd)
            except:
                continue
    for a_id in id_list:
        for fname in os.listdir(saveto + "/" + a_id):
            try:
                if fname.endswith(".mp4"):
                    continue
                else:
                    format_cmd = "ffmpeg -i {} {}".format(saveto + "/" + a_id + "/" + a_id +
                                                  "." + "mkv", saveto + "/" + a_id + "/" + a_id + "." + "mp4")
                    os.system(format_cmd)
                    os.remove(saveto + "/" + a_id + "/" + a_id + "." + "mkv")
            except:
                continue
    print(failed_list)

def cut_videos(indexfile):
    content = json.load(open(indexfile))
    saveto = "cut_videos"
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    for entry in content:
        video_url = entry['url']
        video_id = extract_video_id(video_url)
        og_directory = "originals"
        sign_name = entry['clean_text']
        sign_name = sign_name.replace(" ", "")
        file_name = sign_name
        start_time = entry['start_time']
        end_time = entry['end_time']
        start_time = reformat_time(start_time)
        end_time = reformat_time(end_time)

        if not os.path.exists(saveto + "/" + sign_name):
            os.mkdir(saveto + "/" + sign_name)

        try:
            _, _, files = next(os.walk("{}".format(saveto + "/" + sign_name + "/")))
            file_count = len(files)
        except:
            print("MADNESS")
            file_count = 100

        new_file_name = sign_name + str(file_count)


        ffm_cmd = "ffmpeg -ss {} -to {} -i {} -an -c copy {}".format(start_time, end_time, og_directory + "/" + video_id + "/" + video_id + "." + "mp4", saveto + "/" + sign_name + "/" + new_file_name + ".mp4")
        os.system(ffm_cmd)


def extract_video_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def reformat_time(time):
    if int(time)>=10 and int(time) < 60:
        time = "00:00:{}".format(time)
    elif int(time)>=60 :
        hours = int(time // 3600)
        time = time - hours * 3600
        minutes = int(time // 60)
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
    cut_videos('extraction_test.json')
            