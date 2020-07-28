import os
import json
import time
import sys
import urllib.request
from multiprocessing.dummy import Pool

def download_yt_videos(indexfile):
    content = json.load(open(indexfile))
    saveto = "raw_videos"
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        video_url = entry['url']
        sign_name = entry['clean_text']

        if not os.path.exists(saveto + "/" + sign_name):
            os.mkdir(saveto + "/" + sign_name)


        cmd = "youtube-dl \"{}\" -o \"{}%(id)s\"".format(video_url, saveto + "/" + sign_name + os.path.sep)

        os.system(cmd)


if __name__ == '__main__':
    download_yt_videos('extraction_test.json')