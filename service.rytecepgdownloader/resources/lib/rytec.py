#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import gzip
import re
import random
import xbmcvfs
import xml.etree.ElementTree as ET
from StringIO import StringIO
import common

__version__ = '0.5.1'
__author__ = 'Jin'
epgsources = 'aHR0cDovL2VwZ2FsZmFzaXRlLmR5bmRucy50di9rb2RpLWVwZ3NvdXJjZXM='
headers = {'User-Agent': 'Rytec EPG Downloader %s by %s' % (__version__,__author__), 'Referer': 'rytecepgdownloader.%s' % (__version__)}

def get_sources_list():
    sources_list = []
    try:
        print '[Rytec EPG Downloader]: get sources list'
        r = requests.get(common.bdecode(epgsources), headers=headers)
        if r.status_code == 200:
            sources_list = r.text.splitlines()
            random.shuffle(sources_list)
            #sources_list = gzip.GzipFile(fileobj=StringIO(r.content)).read().splitlines()
    except Exception, e:
        print '[Rytec EPG Downloader]: error in get sources list', e
    return sources_list
        
def get_epg(sources_list, description):
    ret = False
    epg_url = None
    print '[Rytec EPG Downloader]: get epg'
    for source in sources_list:
        try:
            r = requests.get(source, headers=headers)
            if r.status_code == 200:
                content = r.content
                epg_url = get_epg_url(content, description)
                if epg_url:
                    ret = download_epg(epg_url)
                    if ret:
                        break
                else:
                    print '[Rytec EPG Downloader]: no epg url found'
            else:
                print '[Rytec EPG Downloader]: source offline', r.status_code
        except Exception, e:
            print '[Rytec EPG Downloader]: error in get epg', e
    if ret and epg_url:
        print '[Rytec EPG Downloader]: save epg url to config'
        try:
            common.save_epg_url(epg_url, description)
        except Exception, e:
            print '[Rytec EPG Downloader]: could not write url to config', e
    return ret

def get_epg_url(content, description):
    epg_url = None
    try:
        print '[Rytec EPG Downloader]: get epg url'
        root = ET.fromstring(content)
        for source in root.findall('source'):
            sd = source.find('description').text
            url = source.find('url').text
            if sd == description:
                epg_url = url
                break
    except Exception, e:
        print '[Rytec EPG Downloader]: error in get epg url', e
    return epg_url
        
def download_epg(epg_url):
    ret = False
    try:
        print '[Rytec EPG Downloader]: download epg'
        name = epg_url.split('/')[-1]
        xml_file = common.get_xml_file(name)
        from contextlib import closing
        with closing(requests.get(epg_url, headers=headers, stream=True)) as r:
            if r.status_code == 200 and r.headers['content-type'] == 'application/x-gzip' and int(r.headers['content-length']) > 1024:
                print '[Rytec EPG Downloader]: epg download started'
                f = xbmcvfs.File(xml_file, 'wb')
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
                    else:
                        print '[Rytec EPG Downloader]: epg download failed'
                        break
                        return ret
                print '[Rytec EPG Downloader]: epg download complete'
                f.close()
                ret = True
            else:
                print '[Rytec EPG Downloader]: epg url offline', r.status_code
    except Exception, e:
        print '[Rytec EPG Downloader]: error in download epg', e
    return ret