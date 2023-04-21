from pyscripterer import BaseScript as Script
args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]

script = Script(*args)


header_names = ['Cookie', 'Authorization', 'X-Custom-API-Key'] # headers to remove, add/remove as necessary



if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Repeater"): # checks that the HTTP message is in-scope, and that it is coming from Repeater, add "or" logic as necessary
    if (messageIsRequest):
        reqBytes = messageInfo.getRequest()
        req = helpers.analyzeRequest(reqBytes)
        body = reqBytes[(req.getBodyOffset()):].tostring()
        headers = req.getHeaders()
        for header_name in header_names:
                for header in headers:
                    if header.startswith(header_name):
                        headers.remove(header)
                        print("[+] Removed header: " + header_name)
                        break
        newreq = helpers.buildHttpMessage(headers, body)
        messageInfo.setRequest(newreq)
