# -*- coding: cp1252 -*-
from bencode import *
import hashlib
import requests

def client():
    bencodeMetaInfo = get_torrent_info('E:\Downloads\BitTorrentClient\Anathema -- Vol18 [mininova].torrent')
    #bencodeMetaInfo = get_torrent_info('E:\Downloads\BitTorrentClient\debian-live-6.0.7-amd64-gnome-desktop.iso.torrent')
    #print(bencodeMetaInfo)
    announceKey = get_announce(bencodeMetaInfo)
    #print(announceKey)
    length = get_length(bencodeMetaInfo)
    print(length)
    infoDict = get_info(bencodeMetaInfo)
    #print(infoDict)
    encodedInfo = bencode_info(infoDict)
    #print(encodedInfo)
    sha1HashedInfo = hashlib.sha1(encodedInfo).hexdigest()
    announceUrl = announceKey + '?info_hash=' + sha1HashedInfo + '&peer_id=vincentlugli1.0sixty&port=5100&uploaded=0&downloaded=0&left=' + str(length) + '&compact=1'
    print(announceUrl)
    #announceResponse = requests.get(announceUrl)
    #print(announceResponse.status_code)
    

def get_torrent_info(filename):    
    torrentFile = filename;
    metainfo_file = open(str(torrentFile), 'rb')
    metainfo = bdecode(metainfo_file.read())
    info = metainfo['info']
    # torrentDir = info['name']
    return metainfo
    # metainfo_file.close()

    # info = metainfo['announce']
    # print info

    # info = metainfo['info']
    # torrentDir = info['name']
    # print torrentDir

    # This one I have output to a file called test.txt
    # info = metainfo['info']
    # print info

def get_announce(metainfo):
    return metainfo['announce']

def get_info(metainfo):
    return metainfo['info']

def get_length(metainfo):
    if ('files' in metainfo['info']):
        files = metainfo['info']['files']
        total = 0
        for filePart in files:
            total += filePart['length']
        return total        
    else:
        return metainfo['info']['length']

def bencode_info(info):
    encodedInfo = bencode(info)
    return encodedInfo

client()
