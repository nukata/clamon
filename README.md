# Clamon

Clamon is a real-time virus scanner for macOS 10.11-10.13.
It monitors the directories you specified and scans every newly created
or modified files there with `clamd` of ClamAV.
It is implemented with Python 2.7.10 that is built in macOS (`/usr/bin/python`).

## Prerequisites

- ClamAV 0.99.4 or above.
  You can install it either with Homebrew or MacPorts, or from the source.

## How to use

1. Set up `clamd.conf` in ClamAV.
```console
/usr/local/etc/clamav$ diff clamd.conf.sample clamd.conf
8c8
< Example
---
> #Example
85c85
< #LocalSocket /tmp/clamd.socket
---
> LocalSocket /tmp/clamd.socket
93c93
< #LocalSocketMode 660
---
> LocalSocketMode 660
```

2. Run `clamd`.
```console
~$ /usr/local/sbin/clamd
```

3. Run `clamon.py` with directories you want to montor.
   If you run it without directories, it will monitor the current directory.
   Whenever a virus file comes to occur under any level of subdirectory of
   monitored directores, its path name and virus name will be `print`ed.
   You can stop `clamon.py` at any time by hitting the return key.
```console
~$ chmod a+x /path/to/clamon.py
~$ /path/to/clamon.py
Monitoring (
    "/Users/suzuki"
)
Hit Return to stop me: 
```


## License

This project is licensed under the MIT License:

> Copyright © 2018 SUZUKI Hisao
> 
> Permission is hereby granted, free of charge, to any person
> obtaining a copy of this software and associated documentation files
> (the "Software"), to deal in the Software without restriction,
> including without limitation the rights to use, copy, modify, merge,
> publish, distribute, sublicense, and/or sell copies of the Software,
> and to permit persons to whom the Software is furnished to do so,
> subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be
> included in all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
> MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
> NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
> BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
> ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
> CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
