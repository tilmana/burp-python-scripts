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
        forbidden = False
        i = 0
        forbiddenPaths = ["/ip"] # paths to not alter requests for
        if headers[i].split(" ")[1].split("?")[0] in forbiddenPaths:
            forbidden = True
        if forbidden != True: # change logic here for handling non-forbidden requests
            for header_name in header_names:
                for header in headers:
                    if header.startswith(header_name):
                        if header_name == "Cookie":
                            pass
                    i = i + 1
        if forbidden == True:
            headers[0] = "GET / HTTP/1.1" # "clear" the request
            headers = headers[0:2]
            print(headers)
        newreq = helpers.buildHttpMessage(headers, body)
        messageInfo.setRequest(newreq)
