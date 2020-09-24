# -*- coding: utf-8 -*-

'''
# Created on 2020-09-24 09:56
# Author: javy@xu
# Description: download piplines images to local
'''

import os
import sys
import subprocess
import shlex

AIYUNREP="registry.cn-beijing.aliyuncs.com/javy_xu"


def download(imglist_path):
    
    img_local = list()

    with open(imglist_path, "r") as f:
        
        while 1:
            line = f.readline()
            if not line:
                break

            img = line.replace("\n","")
            print(img)
            imgname = img.split("/")[-1]
            img_local.append([os.path.join(AIYUNREP,imgname), img])
        # print(img_local)
    

    for img in img_local:
        print("starting pull {0}".format(img[1]))
        shell_cmd = "docker pull " + img[0]
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                print('Subprogram output: [{}]'.format(line))

        # res = os.popen(cmd)
        # print(res.read())
        cmd = "docker tag " + img[0] + " " + img[1]
        res = os.popen(cmd)
        print(res.read())
        cmd = "docker rmi " + img[0]
        res = os.popen(cmd)
        print(res.read())
        print("{0} images download success".format(img[1]))


if __name__ == "__main__":
    
    args = sys.argv
    if len(args) != 2:
        imglist_path = os.path.join(os.getcwd(), "img-list.txt")
    else:
        imglist_path = args[1]
    print(imglist_path)

    download(imglist_path)
    