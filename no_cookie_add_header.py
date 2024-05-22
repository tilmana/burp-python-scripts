from pyscripterer import BaseScript as Script
args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]

script = Script(*args)


header_names = ['Cookie']



if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Repeater"): # checks that the HTTP message is in-scope, and that it is coming from Repeater, add "or" logic as necessary
    if (messageIsRequest):
        reqBytes = messageInfo.getRequest()
        req = helpers.analyzeRequest(reqBytes)
        body = reqBytes[(req.getBodyOffset()):]
        headers = req.getHeaders()
        noCookie = True
        i = 0
        for header_name in header_names:
            for header in headers:
                if header.startswith(header_name):
                    if header_name == "Cookie": # if there is a header that starts with "Cookie", add a new cookie (line 27)
                        noCookie = False
                        break
                i = i + 1
        if noCookie == True:
            headers.add("Cookie: noCookie!") # new header
        newreq = helpers.buildHttpMessage(headers, body)
        messageInfo.setRequest(newreq)
