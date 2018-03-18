#! /usr/bin/env python

# Real-Time Virus Scanner with "clamd" for macOS 10.11-10.13
# Copyright 2018 SUZUKI Hisao; Licensed under the MIT License.

from FSEvents import *
import os.path, socket, sys, threading, time

threadloop = None

def main(paths):
    global threadloop
    dirs = [ CFStringCreateWithCString(None, path, kCFStringEncodingUTF8) 
             for path in paths ]
    paths = CFArrayCreate(None, dirs, len(dirs), None)
    print "Monitoring", paths

    stream = FSEventStreamCreate(None, callback, None, paths,
                                 kFSEventStreamEventIdSinceNow,
                                 3.0, # latency [seconds]
                                 kFSEventStreamCreateFlagFileEvents)
    try:
        threadloop = CFRunLoopGetCurrent()
        FSEventStreamScheduleWithRunLoop(stream, threadloop,
                                         kCFRunLoopDefaultMode)
        try:
            FSEventStreamStart(stream)
            try:
                CFRunLoopRun()
            finally:
                FSEventStreamStop(stream)
        finally:
            FSEventStreamUnscheduleFromRunLoop(stream, threadloop,
                                               kCFRunLoopDefaultMode)
            FSEventStreamInvalidate(stream)
            threadloop = None
    finally:
        FSEventStreamRelease(stream)
        print "Bye"

ITEM_WRITTEN = (kFSEventStreamEventFlagItemCreated |
                kFSEventStreamEventFlagItemRenamed |
                kFSEventStreamEventFlagItemModified)

def callback(stream, info, numEvents, eventPaths, eventFlags, eventIds):
    for i, flag in enumerate(eventFlags):
        if flag & kFSEventStreamEventFlagItemIsFile:
            if flag & ITEM_WRITTEN:
                path = eventPaths[i]
                # print "%6x %s" % (flag, path)
                if os.path.exists(path):
                    scan(path)

#   0x100 kFSEventStreamEventFlagItemCreated (ln a b)
#   0x800 kFSEventStreamEventFlagItemRenamed (mv a b)
#  0x1000 kFSEventStreamEventFlagItemModified
# 0x10000 kFSEventStreamEventFlagItemIsFile

def scan(path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect("/tmp/clamd.socket")
        s.send("SCAN " + path)
        result = s.recv(1024)
        if result[-3:-1] != 'OK':
            print result,
    finally:
        s.close()

if __name__ == '__main__':
    paths = [ os.path.abspath(path) for path in sys.argv[1:] ]
    if not paths:
        paths = [ os.path.abspath(".") ]
    th = threading.Thread(target=main, args=(paths,))
    th.start()
    while not threadloop:
        time.sleep(1)
    try:
        raw_input("Hit Return to stop me: ")
    finally:
        CFRunLoopStop(threadloop)
