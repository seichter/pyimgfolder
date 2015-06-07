# pyimgfolder
photo and image sorting tool written in Python

This small utility sorts images into a folder structure based on dates such as 2015/05/IMG_0815.jpg - For image files it uses EXIF data when possible. It also copies video files if necessary.

## Dependencies
Python and PIL

## Usage
pyimgfolder -i path/to/files -o path/for/output -v -t -h

-i input path from where the parser will find image files
-o output path where the sorted directories will be created and filled
-v verbose to see what happens
-t trial mode to check first
-h help

## Copyright and License
(c) 2015 [Hartmut Seichter](http://technotecture.com)

distributed under the terms of the 3-Clause BSD License
