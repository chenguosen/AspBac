
import urllib3
import urllib
import json

def Http_Post(url, data, h):
    try:
        http = urllib3.PoolManager()
        r = http.request('POST', url, body=data, headers = h)
        return r.status,r.data.decode('utf-8'),r.headers
    except:
        raise

def get(url,data=None, h=None):
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', url,fields=data,headers = h)
        log.info("get response:{} ".format(r.data.decode('utf-8')))        
        return r.status,r.data.decode('utf-8')
    except:
        raise

def delete(url, h=None):
    try:
        http = urllib3.PoolManager()
        r = http.request('DELETE', url, headers = h)
        
        return r.status,r.data.decode('utf-8')
    except:
        raise

def getURLEncode(s):
    return urllib.parse.quote(s)

if __name__=="__main__":
    header = {
        "Content-Type": "application/json"
    }
    url = "http://10.1.3.218:13345/bnf/QuitGDOrderAciotn/queryRecommendationProdList.service"
    #json_data = {"pubInfo": {"appId": "104567","reqTime": "20201202161306","ver": "1.0","tid": "117402020120216130641662","sign": "5CB6E21C15C0BA6827BB8E92CEAD8D4A"},"busiInfo": {"cbUrl": "http://10.12.8.219:8099/common/submit","userId": "35056af4-3476-11eb-a7da-d0abd5c838f8","method": "createUser55","params": "35056af4-3476-11eb-a7da-d0abd5c838f8,117,808"}}
    json_data ={"msgType": "23232323232", "version": "1.0.0", "channelCode": "100000", "tagId": "02206303243", "servNum": "18730196139"}
    status_code = Http_Post(url=url,data=json.dumps(json_data).encode('utf-8'),h=header)[0]
    print(status_code)