from pyscripterer import BaseScript as Script
import re
import urllib

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
    if 'viewstate' in state:
      viewstate = r'(__VIEWSTATE=)[^&]+'
      body = re.sub(viewstate, "__VIEWSTATE=" + urllib.quote(state['viewstate']), body)
    if 'viewstategenerator' in state:
      viewstategenerator = r'(__VIEWSTATEGENERATOR=)[^&]+'
      body = re.sub(viewstategenerator, "__VIEWSTATEGENERATOR=" + urllib.quote(state['viewstategenerator']), body)
    if 'eventvalidation' in state:
      eventvalidation = r'(__EVENTVALIDATION=)[^&]+'
      body = re.sub(eventvalidation, "__EVENTVALIDATION=" + urllib.quote(state['eventvalidation']), body)
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
