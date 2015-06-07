#!/opt/local/bin/python2.7

import sys
import fnmatch
import os
import time
import re
import shutil
import getopt


from PIL import Image
from PIL.ExifTags import TAGS

class ImageFolder(object):
    def __init__(self):
        self.matches = []
        self.path = {}


    def is_video_file(self,filename, extensions = ['.mp4', '.MP4','.mov','.MOV','.3gp']):
        return any(filename.endswith(e) for e in extensions)

    def is_image_file(self,filename, extensions = ['.jpg', '.JPG', '.jpeg', '.gif', '.png' ]):
        return any(filename.endswith(e) for e in extensions)

    def scan(self,folder):
        for root, dirnames, filenames in os.walk(os.path.abspath(os.path.expanduser(folder))):
            for filename in filenames:
                if self.is_image_file(filename) or self.is_video_file(filename):
                   self.matches.append(os.path.join(root, filename))

    def get_exif_field(self,exif,field):
        for (k,v) in exif.iteritems():
            if TAGS.get(k) == field:
                return v

    def analyze(self):
        for m in self.matches:
            datetime = None
            try:
                img = Image.open(m)

                exif_data = img._getexif()

                if exif_data:
                    dateTimeTags = ['DateTimeDigitized','DateTimeOriginal','DateTime']

                    for dtT in dateTimeTags:
                        datetime = self.get_exif_field(exif_data,'DateTimeOriginal')
                        if datetime:
                            break

            except Exception as inst:
                print 'Problem with ', m

            if datetime == None:
                datetime = time.strftime('%Y:%m:%d', time.gmtime(os.path.getmtime(m)))

            pathDateTime = re.split('[ ,:-]*',datetime)

            # use only year/month (for day change to 3)
            pathDateTime = pathDateTime[:2]

            path = '/'.join(pathDateTime)

            self.path[m] = path


    def print_matches(self):
        print self.path

    def copy(self,outputPath):
        for p in self.path:
            folder,filename = os.path.split(p)
            op = os.path.join(outputPath,self.path[p],filename)
            self.path[p] = op

    def is_duplicate(self,src,dst):
        pass

    def run(self,testrun = True):
        for p in self.path:
            folderInput,filenameInput = os.path.split(p)
            folderOutput,filenameOutout = os.path.split(self.path[p])
            if testrun:
                if not os.path.exists(folderOutput):
                    print "mkdir -p ", folderOutput
                if not os.path.exists(self.path[p]):
                    print "copy ",p,self.path[p]
            else:
                if not os.path.exists(folderOutput):
                    os.makedirs(folderOutput)
                if not os.path.exists(self.path[p]):
                    shutil.copy2(p,self.path[p])

def help():
    print sys.argv[0],'-i inputfolder -o outputfolder -v -h'

def run(inputFolder,outputFolder,verbose,trial):
    imgfolder = ImageFolder()
    imgfolder.scan(inputFolder)
    imgfolder.analyze()
    if verbose:
        imgfolder.print_matches()
    imgfolder.copy(os.path.abspath(os.path.expanduser(outputFolder)))
    imgfolder.run(trial)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'i:o:vht')
        inputFolder = None
        outputFolder = None
        verbose = False
        trial = False
        for o, a in opts:
            if o == '-h':
                help()
                sys.exit(0)
            elif o == '-i':
                inputFolder = a
            elif o == '-o':
                outputFolder = a
            elif o == '-v':
                verbose = True
            elif o == '-t':
                trial = True

        run(inputFolder,outputFolder,verbose,trial)


    except getopt.error, msg:
        print msg
        print "for help use -h"
        sys.exit(2)

if __name__ == "__main__":
    main()

#imgfolder = ImageFolder();
#imgfolder.scan("/Users/hartmut/Pictures/")
#imgfolder.analyze()
#imgfolder.copy('/Users/hartmut/Pictures/sorted/')
#imgfolder.print_matches()
#imgfolder.run(True)
