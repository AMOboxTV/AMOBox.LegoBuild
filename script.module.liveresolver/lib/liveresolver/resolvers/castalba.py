# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try:
            cid  = urlparse.parse_qs(urlparse.urlparse(url).query)['cid'][0] 
        except:
            cid = re.compile('channel/(.+?)(?:/|$)').findall(url)[0]

        
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer='http://castalba.tv'
        
        url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380&r=%s'%(cid,urlparse.urlparse(referer).netloc)
        pageUrl=url

        result = client.request(url, referer=referer,mobile=True)
        result=urllib.unquote(result)

        var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
        var_dict = dict(var)


        if 'm3u8' in result:
            url = re.compile('file.+?\s*=\s*(?:unescape\()[\'\"](.+?)[\'\"]').findall(result)[0]
            url = 'http://' + url + '.m3u8'
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': referer})
            log("Castalba: Found m3u8 url: " + url)
            
        else:
            try:
                filePath = re.compile("'file'\s*:\s*(?:unescape\()?'(.+?)'").findall(result)[0]
                
            except:
                file = re.findall('var file\s*=\s*(?:unescape\()?(?:\'|\")(.+?)(?:\'|\")',result)[0]
                try:
                    file2 = re.findall("'file':\s*unescape\(file\)\s*\+\s*unescape\('(.+?)'\)",result)[0]
                    filePath = file+file2
                except:
                    filePath = file
            swf = re.compile("'flashplayer'\s*:\s*\"(.+?)\"").findall(result)[0]
            
            strm_func = re.findall('function streamer\(\)\s*\{([^\{]+)',result)[0]
            strm_func = re.sub('\s//[^;]+','',strm_func)

            streamer = re.findall('return\s*([^;]+)',strm_func)[0]
            for v in var_dict.keys():
                streamer = streamer.replace(v,var_dict[v])

            streamer = streamer.replace('"','').replace("'",'').replace('+','').strip()

            url = streamer.replace('///','//') + ' playpath=' + filePath +' swfUrl=' + swf + ' flashver=' + constants.flash_ver() +' live=true timeout=15 swfVfy=1 pageUrl=' + pageUrl
            log("Castalba: Found rtmp link: " + url)

        return url
    
    except:
        log("Castalba: Resolver failed. Returning...")
        return

