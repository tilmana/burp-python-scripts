from pyscripterer import BaseScript as Script
import re
import urllib.parse

args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]
header_names = ["Cookie", "Authorization"]
script = Script(*args)

if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Extensions"):
  if (messageIsRequest):
    reqBytes = messageInfo.getRequest()
    req = helpers.analyzeRequest(reqBytes)
    body = reqBytes[(req.getBodyOffset()):].tostring()
    headers = req.getHeaders()
    #print(str(script.get_header_value("Cookie", headers)).replace(" ", "").split(";"))
    #print(headers)
    try:
       if "authZ=True" in script.get_header_value("Cookie", headers):
        for header_name in header_names:
            for header in headers:
                if header.startswith(header_name):
                    headers.remove(header)
                    print("[+] Removed header: " + header_name)
                    break
    except Exception as e:
      pass
    if 'viewstate' in state and 'viewstategenerator' in state and 'eventvalidation' in state:
      viewstate = r'(__VIEWSTATE=)[^&]+'
      viewstategenerator = r'(__VIEWSTATEGENERATOR=)[^&]+'
      eventvalidation = r'(__EVENTVALIDATION=)[^&]+'
      body = re.sub(viewstate, urllib.parse.quote("__VIEWSTATE=" + state['viewstate']), body)
      body = re.sub(viewstategenerator, urllib.parse.quote("__VIEWSTATEGENERATOR=" + state['viewstategenerator']), body)
      body = re.sub(eventvalidation, urllib.parse.quote("__EVENTVALIDATION=" + state['eventvalidation']), body)
    newreq = helpers.buildHttpMessage(headers, body)
    messageInfo.setRequest(newreq)
  else:
    viewstate = r'<input[^>]*name="__VIEWSTATE"[^>]*value="([^"]+)"[^>]*>'
    viewstategenerator = r'<input[^>]*name="__VIEWSTATEGENERATOR"[^>]*value="([^"]+)"[^>]*>'
    eventvalidation = r'<input[^>]*name="__EVENTVALIDATION"[^>]*value="([^"]+)"[^>]*>'
    res = messageInfo.getResponse()
    fullRes = helpers.bytesToString(res)
    if re.search(viewstate, fullRes):
      state['viewstate'] = str(re.search(viewstate, fullRes).group(1))
      print(str(re.search(viewstate, fullRes).group(1)))
    if re.search(viewstategenerator, fullRes):
      state['viewstategenerator'] = str(re.search(viewstategenerator, fullRes).group(1))
      print(str(re.search(viewstategenerator, fullRes).group(1)))
    if re.search(eventvalidation, fullRes):
      state['eventvalidation'] = str(re.search(eventvalidation, fullRes).group(1))
      print(str(re.search(eventvalidation, fullRes).group(1)))
