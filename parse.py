# -*- coding: cp1252 -*-
from bencode import *
import hashlib
import requests

def client():
    filename = 'E:\Downloads\BitTorrentClient\Anathema -- Vol18 [mininova].torrent'
    #filename = 'E:\Downloads\BitTorrentClient\debian-live-6.0.7-amd64-gnome-desktop.iso.torrent'
    bencodeMetaInfo = get_torrent_info(filename)
    #print(bencodeMetaInfo)
    announceKey = get_announce(bencodeMetaInfo)
    #print(announceKey)
    length = get_length(bencodeMetaInfo)
    #print(length)
    infoDict = get_info(bencodeMetaInfo)
    #print(infoDict)
    encodedInfo = bencode_info(infoDict)
    #encodedInfo = get_info_from_torrent(open(filename, 'rb').read())
    #print(encodedInfo)
    sha1HashedInfo = hashlib.sha1(encodedInfo).digest()
    announceUrl = announceKey + '?info_hash=' + sha1HashedInfo + '&peer_id=vincentlugli1.0sixty&port=5100&uploaded=0&downloaded=0&left=' + str(length) + '&compact=1'
    #print(announceUrl)
    announceResponse = requests.get(announceUrl)
    #print(announceResponse.status_code)
    content = bdecode(announceResponse.content)
    #print(content)
    peerList = content['peers']
    print(peerList)
    peerIPs = []
    peerPorts = []
    ip = ''
    portNumber = 0
    currentByte = 0
    for char in peerList:
        if (currentByte < 4):
            if (currentByte == 0):
                ip = str(ord(char))
            else:
                ip += '.' + str(ord(char))
            currentByte += 1
        else:
            if (currentByte == 4):
                peerIPs.append(ip)
                portNumber = ord(char)*256
                currentByte = 5
            else:
                portNumber += ord(char)
                peerPorts.append(portNumber)
                currentByte = 0
    print(peerIPs)
    print(peerPorts)

def get_torrent_info(filename):
    metainfo_file = open(str(filename), 'rb')
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
