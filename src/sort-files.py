# Author: Mattia
# Date: 01.03.2023
# 
# script sorting gopro photos and videos by date and separating them

import os, argparse, sys
import shutil, filecmp
import time, datetime

# (gopro specific)
DATA_PATH = "/DCIM/100GOPRO/"

# argument handling
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", help = "source folder", required = True)
parser.add_argument("-p", "--photos", help = "photos folder", required = True)
parser.add_argument("-v", "--videos", help = "videos folder", required = True)
args = parser.parse_args()

# structure to handle already copied files
class NextImage(Exception):
    pass
continue_i = NextImage()

 
folder_size = os.path.getsize(args.source)
copied_counter = 0
skipped_counter = 0
c = 0

for element in os.listdir(args.source):
    for file in os.listdir(args.source + element + DATA_PATH):
        c += 1
        print(f"\x1b[2K\r[{round(c/folder_size*100, 2)}%] copied: {copied_counter}, skipped: {skipped_counter}\telement:{element}/{file}", end = "", flush = True)
        try:
            if file.endswith(".JPG") and not file.startswith("."):
                date_counter = 1
                date = time.gmtime(os.path.getmtime(args.source + element + DATA_PATH + file))
                
                if f"{date.tm_year}" not in os.listdir(args.photos):
                    os.mkdir(args.photos + str(date.tm_year))

                while f"{date.tm_year}_{date.tm_mon:02d}_{date.tm_mday:02d}_({date_counter}).JPG" in os.listdir(f"{args.photos}{date.tm_year}/"):
                    if filecmp.cmp(args.source + element + DATA_PATH + file, f"{args.photos}{date.tm_year}/{date.tm_year}_{date.tm_mon:02d}_{date.tm_mday:02d}_({date_counter}).JPG"):
                        raise continue_i
                    date_counter += 1

                shutil.copy(args.source + element + DATA_PATH + file, f"{args.photos}{date.tm_year}/{date.tm_year}_{date.tm_mon:02d}_{date.tm_mday:02d}_({date_counter}).JPG")
            elif file.endswith(".MP4") and not file.startswith("."):
                date_counter = 1
                date = time.gmtime(os.path.getmtime(args.source + element + DATA_PATH + file))
                
                if f"{date.tm_year}" not in os.listdir(args.videos):
                    os.mkdir(args.videos + str(date.tm_year))
                while f"{date.tm_year}_{date.tm_mon:02d}_{date.tm_mday:02d}_({date_counter}).MP4" in os.listdir(f"{args.videos}{date.tm_year}/"):
                    if filecmp.cmp(args.source + element + DATA_PATH + file, f"{args.videos}{date.tm_year}/{date.tm_year}_{date.tm_mon:02d}_{date.tm_mday:02d}_({date_counter}).MP4"):
                        raise continue_i
                    date_counter += 1
                shutil.copy(args.source + element + DATA_PATH + file, f"{args.videos}{date.tm_year}/{date.tm_year}_{date.tm_mon:02d}_{date.tm_mday:02d}_({date_counter}).MP4")
            else:
                raise continue_i
            copied_counter += 1
        except NextImage:
            skipped_counter += 1
            continue
            

