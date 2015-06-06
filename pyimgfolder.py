#!/opt/local/bin/python2.7

import sys
import fnmatch
import os
import time
import re
import shutil


from PIL import Image
from PIL.ExifTags import TAGS

class ImageFolder(object):
    def __init__(self):
        self.matches = []
        self.path = {}

    def is_image_file(self,filename, extensions=['.jpg', '.JPG', '.jpeg', '.gif', '.png']):
        return any(filename.endswith(e) for e in extensions)
        
    def scan(self,folder):
        for root, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if self.is_image_file(filename):
                   self.matches.append(os.path.join(root, filename))
                                             
    def getExifField(self,exif,field):
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
                        datetime = self.getExifField(exif_data,'DateTimeOriginal')
                        if datetime:
                            break
                            
            except Exception as inst:
                print m
                pass
                
            if datetime == None:
                datetime = time.strftime('%Y:%m:%d', time.gmtime(os.path.getmtime(m)))
                #print(m,' has no EXIF data!',datetime)
           
            pathDateTime = re.split('[ ,:-]*',datetime)
            
            # use only year/month (for day change to 3)
            pathDateTime = pathDateTime[:2]
            
            path = '/'.join(pathDateTime)
            
            self.path[m] = path 
            

    def printMatches(self):
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
                print "mkdir -p ", folderOutput
                print "copy "
            else:
                if not os.path.exists(folderOutput):
                    os.makedirs(folderOutput)
                shutil.copy2(p,self.path[p])
                

imgfolder = ImageFolder();
imgfolder.scan("/Users/hartmut/Pictures/")
imgfolder.analyze()
imgfolder.copy('/Users/hartmut/Pictures/sorted/')
#imgfolder.printMatches()
imgfolder.run(True)
