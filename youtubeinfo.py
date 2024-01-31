import requests
import pyperclip
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time


all_videos = []

def initial_videos():
    response = requests.get(f"https://www.youtube.com/@DailyDoseOfInternet/videos")
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if 'var ytInitialData = ' not in str(script):
                continue
            data = json.loads(str(script).split('var ytInitialData = ')[1].rstrip("</script>;"))
            contents = data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents']

            for c in contents:
                if 'richItemRenderer' not in c:
                    continue
                content = c['richItemRenderer']['content']
                all_videos.append(content['videoRenderer']['videoId'])

def remaining_videos(continuation=None):

    if continuation is None:
        continuation = "4qmFsgKvCBIYVUNkQzBBbjRaUE5yX1lpRmlZb1Zid2F3GpIIOGdhSEJocUVCbnFCQmdyOEJRclRCVUZtYW5Fd2RsQllkMWhuUVVaNU1DMVZRWGxuWjJWTk5YUlVOV1o0YkRCamMyZzJaR0Y0YnpKWWRGQkJUMHBMZW5GeWFHNDJiV05rTVVjMlpGWk5lVmc1Y25kbldVaENlV0l0ZG14NllpMVRVM1pxVjJkelZsbERRVmRJVkhWNWNDMHlPWG93WW5SbVprdzNVVTlsWldvNVNYZEtXblpaUjA1dVpHZEdXbVpsTTJzelpHUnlObE5SVmtOM1kyNVVaRzlPWkVVeGVXdEhTbTlMVG10clYxUnlVMUp6ZDJrd2NWWjJaREIwWDNOa1ZVSlZVblJ2WjBWbWFXdEVRa2RJV0ZoNVlURjVOa2w1WW05aVdHYzNZaTFJTjBkamNubGZRMk5GUTNObmFXWnNNMjFHVm5SMU5GSmliMjlIT1ZnMVREZDZOR1JzWmtScGFFczJXVkpDVm5wVllXUndiblZUUzE5Q2FtRkRkV1JGZEcxb1dYYzBWVVozUWpsZlJFbzNVbFpoWWxFNFdpMXRXbTlWTXpWSFVtNVJkekY1VWxwdGJuZ3hNVmxIVVdodk9EbDBNRFZqVFRkeWFIY3dZMUZhVmw5TVowdFBSV3A2ZFVSR2VXVm1NQzFMWDI1bFIxazRPV3BvVjIxaGJDMUtOa0YyWXpaeFZteExiVXRFYWpabWVWRTFNSG8zV1Y5MVZVUnFWREJET0dkSGJuWnJTVkZaZERkU1N6RlJhSHA1VERsMk9HUmhiREZIWlhOTFFXdDFRazV2UlUxbFV6TnJjV0pzTmxoRE5ERlBXSGMzYmtSbmJ6Vm1Na1l6YVZSMldFbzNVVmhTUVZweGJuZG9RemhzUkhKUFNYVnJVVkZXT0dKaldESmxOVFJmVFdOd2NITnFUMEZHUVRKNGRrTkpaa3Q2TUVkQ1VGZE5NSFZSTVhkU05XMXZlSGxVTTNGcFQzSk5OSFkzWWs1d1FsVmxNazQyUVhWQlFVZFpWV1ZsZDJSdVpUZElOblp3WVRoRU1rbEhNVkJ6T0hCTFYxbDZhMGRsY1dweWJYQlNXak5pTWpsSE9YUXpTRTF6TVZORGVtd3pXbFY0YWprdGVXTldibFpxUjAxMlNVVmtRMU5MVG10UWRVYzRRbEY2Ym1ReFNGa3liRzFVVTBWM2MxVnFlbTFvTjNkUmMyUklPVFJoUldacFkxZ3RMUzFsU1dsUGNFRkVWemQxYWtNd1JUbElVREJPWVdjMGVqVmxiRkZwTW1kSVlqRnVTelJKZG1SMWVXdG5VR2d3YnhJa05qWmhaVGMwTXpndE1EQXdNQzB5TnpnMUxXRmpPVEl0WmpSbU5XVTRNR0V3TkRrNEdBRSUzRA%3D%3D"
        
    curl_command = """
        curl 'https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false' \
        -H 'authority: www.youtube.com' \
        -H 'accept: */*' \
        -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,de;q=0.7,fa;q=0.6' \
        -H 'authorization: SAPISIDHASH 1706392192_e71eae9c203df0a4a168a89cba6f20bc2b8c695c' \
        -H 'content-type: application/json' \
        -H 'cookie: CONSENT=PENDING+276; HSID=AQDY_cq_ZU4xpPonn; SSID=AQY1LohRfJL25ClXq; APISID=4yeniRZ4QZLVY9oR/AsjhK6tzUzL8f-uK5; SAPISID=SwGbfm0EBzK8kMBM/A5T3v2sUrV5aCseI-; __Secure-1PAPISID=SwGbfm0EBzK8kMBM/A5T3v2sUrV5aCseI-; __Secure-3PAPISID=SwGbfm0EBzK8kMBM/A5T3v2sUrV5aCseI-; LOGIN_INFO=AFmmF2swRQIgNuiV9JSK_GRz-EXfIt5a4dl4tvOCSH0_Y8BhvMJx7XcCIQDShYWPFUOY2fN0aBzVVA4Um1cVFefuGxTeGlKAXuezQA:QUQ3MjNmd0RlS0NXNGNzUFNGdXZqcXF5dlF1aWpHc3l2ekVKRjBhWmYwU1pvZ2lSMEl1T0FUUHVtSTgxTV9XelBVQnpUc2dGMTEzQXV0Qjlud01ZR25wWFp2U18tb2d4dG9jRFhEeDZsdFlySzN2WjBtQzhOczM2X1A4OTJkNDJHNW1DeW5ZOHlzbk45Nld3dU9vWDdyX0dyZ1VpY0pqZWl3; VISITOR_INFO1_LIVE=ziKpj5evD7k; __Secure-YEC=CgtaUjVaLV9IYjN1WSiNktSrBjIICgJHQhICGgA%3D; VISITOR_PRIVACY_METADATA=CgJHQhIEGgAgVA%3D%3D; SID=fQg30C6F1w7AelT9m5WNwzPP7ekpwszZT1ZSgNKlWrS0VLWae5SgL5RgXIk6FMYnxixzig.; __Secure-1PSID=fQg30C6F1w7AelT9m5WNwzPP7ekpwszZT1ZSgNKlWrS0VLWaR1oTSljMHWn3oN5MUaY7ig.; __Secure-3PSID=fQg30C6F1w7AelT9m5WNwzPP7ekpwszZT1ZSgNKlWrS0VLWakoKHxn9ntX-KSYWBXJkXSQ.; YSC=colCmYq3g2s; SOCS=CAISNQgDEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwODI5LjA3X3AxGgJlbiADGgYIgJnPpwY; PREF=f6=40000480&f7=100&tz=Europe.London&autoplay=true&f5=30000; __Secure-1PSIDTS=sidts-CjEBPVxjSle3wxb7AD8YLzpCyKtivPQ4jYzHQ-9hETZTesi_PUMkIfrSqMTov3ZmdCmLEAA; __Secure-3PSIDTS=sidts-CjEBPVxjSle3wxb7AD8YLzpCyKtivPQ4jYzHQ-9hETZTesi_PUMkIfrSqMTov3ZmdCmLEAA; wide=1; SIDCC=ABTWhQEs3MBTmYCKRv792I5An1VCQGF9omNPOZ5GlNjvYUNDf3K8Smmbblu-hlyViTxR1y1L7n4; __Secure-1PSIDCC=ABTWhQFGV1jntKuVk3VVWTV5eEC90lWca1uGia7te9rdFybLNVjUN7zwM_PDJUfqOTzRCT0llO3T; __Secure-3PSIDCC=ABTWhQHoNuAiaJF1diAiEHZRzeuU3msvlYGFIk0wKBS96Yoc31U-Sr89tGWGeTZthg4oiUOrQld-' \
        -H 'dnt: 1' \
        -H 'origin: https://www.youtube.com' \
        -H 'referer: https://www.youtube.com/@DailyDoseOfInternet/videos' \
        -H 'sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"' \
        -H 'sec-ch-ua-arch: "x86"' \
        -H 'sec-ch-ua-bitness: "64"' \
        -H 'sec-ch-ua-full-version: "120.0.6099.227"' \
        -H 'sec-ch-ua-full-version-list: "Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.227", "Google Chrome";v="120.0.6099.227"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-model: ""' \
        -H 'sec-ch-ua-platform: "Windows"' \
        -H 'sec-ch-ua-platform-version: "15.0.0"' \
        -H 'sec-ch-ua-wow64: ?0' \
        -H 'sec-fetch-dest: empty' \
        -H 'sec-fetch-mode: same-origin' \
        -H 'sec-fetch-site: same-origin' \
        -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
        -H 'x-client-data: CIW2yQEIo7bJAQipncoBCMjxygEIkqHLAQiFoM0BCJXbzQEI5OzNAQii7s0BCN7uzQEIg/DNAQiU8M0BCKnyzQEI+vPNAQiQ9c0BCJ/2zQEY9MnNARin6s0BGPnyzQEYnPjNAQ==' \
        -H 'x-goog-authuser: 0' \
        -H 'x-goog-visitor-id: Cgt6aUtwajVldkQ3ayjd89WtBjIKCgJHQhIEGgAgVA%3D%3D' \
        -H 'x-origin: https://www.youtube.com' \
        -H 'x-youtube-bootstrap-logged-in: true' \
        -H 'x-youtube-client-name: 1' \
        -H 'x-youtube-client-version: 2.20240126.01.00' \
    """
    url = re.search(r"curl '([^']+)'", curl_command).group(1)
    headers = {header.split(': ')[0]: header.split(': ')[1] for header in re.findall(r"-H '([^']+)'", curl_command)}
    data = {"context":{"client":{"hl":"en","gl":"GB","remoteHost":"82.40.48.136","deviceMake":"","deviceModel":"","visitorData":"Cgt6aUtwajVldkQ3ayjd89WtBjIKCgJHQhIEGgAgVA%3D%3D","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20240126.01.00","osName":"Windows","osVersion":"10.0","originalUrl":"https://www.youtube.com/","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CN3z1a0GENPhrwUQyfevBRCCr7AFEOevsAUQ9quwBRDOi_8SEKn3rwUQ9KuwBRDks_4SEInorgUQuIuuBRC9mbAFEPqnsAUQ57qvBRCeoLAFEKylsAUQ_qewBRDM364FENyCsAUQ6sOvBRDCr7AFEL22rgUQuKqwBRD7sLAFENfprwUQ7qKvBRDbr68FELersAUQt--vBRCI468FEPuSsAUQooGwBRDViLAFEKiasAUQn66wBRDNlbAFEN-L_xIQvPmvBRD8hbAFEMyu_hIQ6-j-EhCD368FEKy3rwUQvoqwBRDUoa8FEPOhsAUQ4tSuBRClwv4SENCNsAUQl4OwBRCmmrAFEL75rwUQ7aKwBRCmgbAFENnJrwUQgYz_EhD1-a8FEIiHsAUQpJCwBRCY_P4SEM-osAUQ65OuBRCei7AFEN3o_hIQmvCvBRC3rrAFELSusAUQ4fKvBRDrqbAFEK7U_hIQt-r-Eg%3D%3D"},"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"Europe/London","browserName":"Chrome","browserVersion":"120.0.0.0","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","deviceExperimentId":"ChxOek15T0RnNU56azJNREUzTnpBek1ESTBNdz09EN3z1a0GGN3z1a0G","screenWidthPoints":2714,"screenHeightPoints":1271,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":0,"connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/@DailyDoseOfInternet/videos","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":"true"}},"user":{"lockedSafetyMode":"false"},"request":{"useSsl":"true","internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{"clickTrackingParams":"CDMQ8eIEIhMIyvCtoMb-gwMVXmpBAh2Ftw39"},"adSignalsInfo":{"params":[{"key":"dt","value":"1706392027623"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"0"},{"key":"u_his","value":"3"},{"key":"u_h","value":"1440"},{"key":"u_w","value":"3440"},{"key":"u_ah","value":"1392"},{"key":"u_aw","value":"3440"},{"key":"u_cd","value":"30"},{"key":"bc","value":"31"},{"key":"bih","value":"1271"},{"key":"biw","value":"2698"},{"key":"brdim","value":"0,0,0,0,3440,0,3440,1392,2714,1271"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"continuation":continuation}

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    
    if response.status_code == 200:
        data = response.json()

        continuationItems = data['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
        for item in continuationItems:
            if 'richItemRenderer' not in item:
                continue
            video = item['richItemRenderer']['content']['videoRenderer']
            all_videos.append(video['videoId'])
        
        videos = continuationItems[-1]
        if 'continuationItemRenderer' not in videos:
            with open(f"{headers['referer'].rsplit('/')[-2]}.json","w",encoding="utf8") as file:
                file.write(json.dumps(all_videos, indent=4, ensure_ascii=False))
            exit()

        next_continuation_token = videos['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        if next_continuation_token:
            time.sleep(2)
            remaining_videos(next_continuation_token)

initial_videos()
remaining_videos()