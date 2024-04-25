from pyscripterer import BaseScript as Script
args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]

script = Script(*args)


header_names = ['Cookie', 'Authorization', 'X-Custom-API-Key'] # headers to replace, add/remove as necessary



if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Repeater"): # checks that the HTTP message is in-scope, and that it is coming from Repeater, add additional logic as necessary
    if (messageIsRequest):
        reqBytes = messageInfo.getRequest()
        req = helpers.analyzeRequest(reqBytes)
        body = reqBytes[(req.getBodyOffset()):].tostring()
        headers = req.getHeaders()
        i = 0
        for header_name in header_names:
            for header in headers:
                if header.startswith(header_name):
                    if header.split(":")[1] == " test=a": # checks header value
                        headers[i] = "Cookie: REPLACE" # replace value
                        pass
                i = i + 1
        newreq = helpers.buildHttpMessage(headers, body)
        messageInfo.setRequest(newreq)
