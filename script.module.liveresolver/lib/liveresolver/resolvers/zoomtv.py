# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client,decryptionUtils,constants
from liveresolver.modules.log_utils import log


def resolve(url):
    try:

        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        headers = { 'referer': referer,
                                 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                 'Content-Type' :'application/x-www-form-urlencoded',
                                 'Connection' : 'keep-alive',
                                 'Host' : 'www.zoomtv.me',
                                 'Origin' : urlparse.urlparse(referer).netloc,
                                 'User-Agent' : 'Apple-iPhone/701.341'
                                 }
        fid = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
        pid = urlparse.parse_qs(urlparse.urlparse(url).query)['pid'][0]
        url = 'http://www.zoomtv.me/embed.php?v=%s&vw=660&vh=450'%fid
        pageUrl = url
        post_data = urllib.urlencode({'uagent':'Apple-iPhone/701.341', 'pid':pid})
    
        #get mobile stream
        for i in range(30):
            try:
                result = req(url,post_data,headers)
                streamer = re.findall('src=[\"\'](.+?)[\"\'].+?type=[\"\']video/mp4[\"\']',result)[0]
                break
            except:
                streamer = None


        #get desktop stream
        headers.update({ 'User-Agent' : client.agent() })
        post_data = urllib.urlencode({'uagent':client.agent(), 'pid':pid})
        for i in range(30):
            try:
                result = req(url,post_data,headers)
                rtmp = re.findall('streamer:([^,]+)',result)[0].replace("+''",'').replace("''+",'').replace("+''+",'')
                break
            except:
                rtmp = None

        #for HQ links(no rtmp)
        if rtmp is None:
            return streamer + '|%s' % urllib.urlencode({'user-agent':client.agent(),'Referer':referer})

        #exctract params from m3u8 link and add it to rtmp
        file = urlparse.parse_qs(urlparse.urlparse(streamer).query)['file'][0]
        sg = urlparse.parse_qs(urlparse.urlparse(streamer).query)['sg'][0]
        ts = urlparse.parse_qs(urlparse.urlparse(streamer).query)['ts'][0]
        auth = urlparse.parse_qs(urlparse.urlparse(streamer).query)['auth'][0]
        url = rtmp + ' playpath=' + file + ' swfUrl=http://static.zoomtv.me/player/jwplayer.6.5.3.swf flashver=' +constants.flash_ver() + ' conn=S:' + file + ' conn=S:'+ts+' conn=S:'+sg+' conn=S:'+auth+' live=1 timeout=15 token=Q!lrB@G1)ww(-dQ4J4 swfVfy=1 pageUrl=' + pageUrl

        return url
    except:
        return

def req(url,post_data,headers):
    result = client.request(url, post=post_data,headers = headers)
    result = decryptionUtils.doDemystify(result)
    var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
    vars = dict(var)
    result = re.sub('var.+?=.+?;','',result)
    for v in vars.keys():
        result = result.replace(v,vars[v])
    return result