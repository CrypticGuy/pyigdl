import requests
import json
import brotli
from parsel import Selector
from utils import extractHtmlContentFromJsResponse

def _create_headers():
    headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br, zstd", "Accept-Language": "en-US,en;q=0.9", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://saveig.app", "Referer": "https://saveig.app/", "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"', "Sec-Ch-Ua-Mobile": "?1", "Sec-Ch-Ua-Platform": '"Android"', "Sec-Fetch-Dest": "empty"}
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    headers["X-Requested-With"] = "XMLHttpRequest"
    return headers

def _payloadData(url):
    data = {"q": url, "t": "media", "lang": "en", "v": "v2"}
    return data

def _getServerUrl():
    return "https://v3.saveig.app/api/ajaxSearch"

def _parseResponse(response):
    try:
        parsed_response = brotli.decompress(response.content).decode('utf-8')
        parsed_response = json.loads(parsed_response)['data']
    except Exception as e:
        parsed_response = response.json()['data']
    
    if not ("download-items" in parsed_response):
        print('here')
        parsed_response = extractHtmlContentFromJsResponse(parsed_response)

    selector = Selector(text=parsed_response)
    print(selector)
    download_data = []
    for elem in selector.css(".download-items"):
        print(elem)
        download_data.append({
            "thumbnail_link": elem.css(".download-items__thumb > img").attrib["src"],
            "download_link": elem.css(".download-items__btn > a").attrib["href"]
        })
    
    return download_data

def _sendPostRequest(serverUrl, payloadData, headers):
    sess = requests.Session()
    response = sess.post(serverUrl, headers=headers, data=payloadData) # post requests
    resp_json = response.json()
    # print(resp_json)
    if (resp_json.get("mess")):
        raise Exception(resp_json.get("mess"))
    return _parseResponse(response)

def IGDownloader(url):
    payloadData = _payloadData(url)
    serverUrl = _getServerUrl()
    headers = _create_headers()
    try: 
        return _sendPostRequest(serverUrl, payloadData, headers)
    except Exception as e:
        print(e.with_traceback())
