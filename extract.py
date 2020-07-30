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
    fail_count = 0
    content = json.load(open(indexfile))
    saveto = "raw_videos"
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        random_character2 = random.choice(string.ascii_letters)
        video_url = entry['url']
        sign_name = entry['clean_text']
        sign_name = sign_name.replace(" ", "")
        start_time = entry['start_time']
        end_time = entry['end_time']
        file_name = sign_name + random_character2

        if int(start_time)>=10 :
            start_time = "00:00:{}".format(start_time)
        else:
            start_time = "00:00:0{}".format(start_time)
        
        if int(end_time)>=10 :
            end_time = "00:00:{}".format(end_time)
        else:
            end_time = "00:00:0{}".format(end_time)

        print(start_time)

        if not os.path.exists(saveto + "/" + sign_name):
            os.mkdir(saveto + "/" + sign_name)

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

            ffm_cmd = "ffmpeg -ss {} -to {} -i {} -an -c copy {}".format(start_time, end_time, saveto + "/" + sign_name + "/" + file_name + "." + video_ext, saveto + "/" + sign_name + "/" + file_name + random_character2 + ".mp4")
            os.system(ffm_cmd)
            os.remove(saveto + "/" + sign_name + "/" + file_name + "." + video_ext)

    print(fail_count)


if __name__ == '__main__':
    download_yt_videos('extraction_test.json')