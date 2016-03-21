# -*- coding: utf-8 -*-


import re,urlparse,cookielib,os
from liveresolver.modules import client,unCaptcha,control,constants

cookieFile = os.path.join(control.dataPath, 'finecastcookie.lwp')

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url


        id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        url = 'http://www.finecast.tv/embed4.php?u=%s&vw=640&vh=450'%id

        headers=[("User-Agent", client.agent()), ("Referer", referer)]
        cj = get_cj()

        result = unCaptcha.performCaptcha(url, cj, headers = headers)

        cj.save (cookieFile,ignore_discard=True)
        


        file = re.findall('[\'\"](.+?.stream)[\'\"]',result)[0]
        auth = re.findall('[\'\"](\?wmsAuthSign.+?)[\'\"]',result)[0]
        rtmp = 'rtmp://play.finecast.tv:1935/live%s'%auth

        url = rtmp +  ' playpath=' + file + ' swfUrl=http://www.finecast.tv/player6/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' live=1 timeout=14 pageUrl=' + url
        return url

        
    except:
        return


def get_cj():
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookieFile,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar