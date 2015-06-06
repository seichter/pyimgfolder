#!/opt/local/bin/python2.7

import sys
import fnmatch
import os
import time
import re


from PIL import Image
from PIL.ExifTags import TAGS

class ImageFolder(object):
    def __init__(self):
        self.matches = []
        self.pathes = []

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
            img = Image.open(m)
            exif_data = img._getexif()
            
            dateTimeTags = ['DateTimeDigitized','DateTimeOriginal','DateTime']

            for dtT in dateTimeTags:
                datetime = self.getExifField(exif_data,'DateTimeOriginal')
                if datetime:
                    break
                    
            if datetime == None:
                datetime = time.strftime('%Y:%m:%d', time.gmtime(os.path.getmtime(m)))
                print(m,' has no EXIF data!',datetime)
           
            pathDateTime = re.split('[ ,:-]*',datetime)
            
            pathDateTime = pathDateTime[:3]
            
            path = '/'.join(pathDateTime)
            
            print m,path
            
            
                        
    def printMatches(self):
        for m in self.matches:
            print(m)

imgfolder = ImageFolder();
imgfolder.scan("/Users/hartmut/Pictures/import/")
# imgfolder.printMatches()
imgfolder.analyze()
