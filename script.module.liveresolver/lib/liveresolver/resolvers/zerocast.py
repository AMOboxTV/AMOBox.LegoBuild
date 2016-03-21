# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urlparse,base64, urllib
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        if 'chan=' in url:
            result = client.request(url, referer=referer)
            url = re.findall('<script\stype=[\'"]text/javascript[\'"]\ssrc=[\'"](.+?)[\'"]>', result)[0]

        r = re.findall('.+?a=([0-9]+)', url)[0]

        url = 'http://zerocast.tv/embed.php?a=%s&id=&width=640&height=480&autostart=true&strech=' % r

        result = client.request(url, referer=referer)

        r = re.findall('curl\s*=\s*[\'"](.+?)[\'"]', result)
        r += re.findall('file\s*:\s*["\'](.+?)["\']', result)
        r = r[0].decode('base64', 'strict')

        if r.startswith('rtmp'):
            return '%s pageUrl=%s live=1 timeout=30' % (r, url)

        elif '.m3u8' in r:
            chunk = client.request(r)
            chunk = re.compile('(chunklist_.+)').findall(chunk)[0]
            url = r.split('.m3u8')[0].rsplit('/', 1)[0] + '/' + chunk
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent()})
            return url
    except:
        return


