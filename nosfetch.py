#!/usr/bin/env python2
### nosfetch.py
##
## Copyright (c) 2012, 2013, 2014, 2016, 2017, 2018 Matthew Love <matthew.love@colorado.edu>
##
## Permission is hereby granted, free of charge, to any person obtaining a copy 
## of this software and associated documentation files (the "Software"), to deal 
## in the Software without restriction, including without limitation the rights 
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
## of the Software, and to permit persons to whom the Software is furnished to do so, 
## subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
## INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
## PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
## FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
## ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##
### Code:

import sys
import urllib2
from xml.dom import minidom
import noslib

fnos_version='0.2.1'

nos_file = 'fetch_nos_surveys'

nl = noslib.nosLib()

def Usage(use_error=None):
    print('nosfetch.py [-region xmin xmax ymin ymax]')
    print('            [-list-only] [-fetch] [-data datatype]')
    print('            [-metadata] [-verbose]')
    print('')
    print('Options:')
    print('  -region\tSpecifies the desired input region; xmin xmax ymin ymax')
    print('  -list_only\tObtain only a list of surveys in the given region.')
    print('  -survey\tGet a specific survey, enter the surveyID here; this will also accept a file with a list of')
    print('         \tsurveyIDs')
    print('  -data\t\tSpecify the data type to download, to see what data types are available for a given survey,')
    print('       \t\tuse nos_info.py -survey surveyID, default will fetch all available data types;')
    print('       \t\tseparate datatypes with a `,`')
    print('       \t\tData types include: %s' %(nl.dic_key_list(noslib._nos_extentions)))
    print('  -metadata\tDownload the associated metadata xml file')
    print('')
    print('  -verbose\tIncrease verbosity')
    print('  -help\t\tPrint the usage text')
    print('  -version\tPrint the version information')
    print('')
    print('Example:')
    print('nosfetch.py -region -90.75 -88.1 28.7 31.25 -data XYZ,BAG')
    print('Fetch the metadata only:')
    print('nosfetch.py -region -90.75 -88.1 28.7 31.25 -metadata')
    print('Fetch a single survey:')
    print('nosfetch.py -survey H12120')
    if use_error is not None:
        print('')
        print('Error: %s' %(use_error))
        sys.exit(0)

#--
#
# Mainline
#
#--
if __name__ == '__main__':

    extent = None
    fetch_list = None
    lst_only = False
    get_xml = False
    dtype="ALL"
    verbose=False

    # Process the command line
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == '-region':
            try:
                extent = (float(sys.argv[i+1]),float(sys.argv[i+2]),
                          float(sys.argv[i+3]),float(sys.argv[i+4]))
                i = i + 4
            except: Usage("you must enter a value with the -region switch")

        elif arg == '-list_only':
            lst_only = True

        elif arg == '-data':
            try:
                dtype = sys.argv[i+1]
                i = i + 1
            except: Usage("you must enter a value with the -data switch")

        elif arg == '-metadata':
            get_xml = True

        elif arg == '-survey':
            try:
                fetch_list = sys.argv[i+1]
                i = i + 1
            except: Usage("you must enter a value with the -survey switch")

        elif arg == '-verbose':
            verbose = True

        elif arg == '-help' or arg == '--help' or arg == '-h':
            Usage()
            sys.exit(0)

        elif arg == '-version' or arg == '--version':
            print('nos_fetch.py v.%s | noslib v.%s' %(fnos_version, noslib_version))
            print_license()
            sys.exit(1)

        elif arg[0] == '-':
            Usage()

        else:
            Usage()

        i = i + 1

    bounds = extent

    if extent is None and fetch_list is None:
        Usage("you must either enter a region or a surveyID")
    
    dtypes = dtype.split(",")
    nl._verbose = True
    dts = []
    if dtypes != ['ALL']:
        for dt in dtypes:
            if dt == 'XYZ': dt = 'GEODAS'
            if dt in nl._dtypes: dts.append(dt)
        nl._set_dtypes(dts)

    if fetch_list:
        s = noslib.nosSurvey(fetch_list)
        for dt in nl._dtypes:
            s.fetch(dt)
    else:
        nl.bfilter(extent)
        if lst_only:
            for i in nl.surveys:
                print i
        else:
            nl.fetch()

### End
