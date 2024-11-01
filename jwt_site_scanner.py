from pyscripterer import BaseScript as Script # script requires configuration for applicable endpoints of the site and it's IdP
import json
import re
import urllib

args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]

script = Script(*args)


header_names = ['Authorization: Bearer']



if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Scanner" or callbacks.getToolName(toolFlag) == "Extensions" or callbacks.getToolName(toolFlag) == "Repeater"): # checks that the HTTP message is in-scope, and that it is coming from Repeater, add "or" logic as necessary
    if (messageIsRequest):
        state["prevRefreshRequest"] = "false"
        state["prevLoginRequest"] = "false"
        reqBytes = messageInfo.getRequest()
        req = helpers.analyzeRequest(reqBytes)
        body = reqBytes[(req.getBodyOffset()):].tostring()
        headers = req.getHeaders()
        if headers[0].split(" ")[1] == "LOGOUT ENDPOINT":
            headers[0] = "GET / HTTP/1.1"
            print("Dropped logout request")
        if "POST TOKEN ENDPOINT" in headers[0] and "username=" in body and "password=" in body:
            print("Login request detected")
            state["prevLoginRequest"] = "true"
            for header_name in header_names:
                for header in headers:
                    if header.startswith(header_name):
                        headers.remove(header)
                        break
        elif "POST TOKEN ENDPOINT" in headers[0] and "grant_type=refresh_token" in body:
            print("Refresh token request detected")
            state["prevRefreshRequest"] = "true"
            for header_name in header_names:
                for header in headers:
                    if header.startswith(header_name):
                        headers.remove(header)
                        break
            refresh_token_regex = r'(refresh_token=)[^&]+'
            body = re.sub(refresh_token_regex, "refresh_token=" + urllib.quote(state["refresh_token"]), body)
            print("Replaced refresh token succesfully")
        else:
            for header_name in header_names:
                for header in headers:
                    if header.startswith(header_name):
                        headers.remove(header)
                        break
            headers.add("Authorization: Bearer {0}".format(state["access_token"]))
        newreq = helpers.buildHttpMessage(headers, body)
        messageInfo.setRequest(newreq)
    else:
        responseInfo = helpers.analyzeResponse(messageInfo.getResponse())
        headersR = responseInfo.getHeaders()
        msgResponseBody = messageInfo.getResponse()[responseInfo.getBodyOffset():]
        msgR = helpers.bytesToString(msgResponseBody)
        if state["prevRefreshRequest"] == "true":
            state["refresh_token"] = json.loads(msgR)["refresh_token"]
            print("Token refresh retrieval complete")
        elif state["prevLoginRequest"] == "true":
            state["access_token"] = json.loads(msgR)["access_token"]
            state["refresh_token"] = json.loads(msgR)["refresh_token"]          
            print("Login tokens retrieval complete")
