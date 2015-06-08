#!/opt/local/bin/python2.7

# Copyright (c) 2015, Hartmut Seichter
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


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
