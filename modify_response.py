import re

from pyscripterer import BaseScript as Script
args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]
script = Script(*args)

if (not messageIsRequest):
    if (callbacks.getToolName(toolFlag) == "Proxy"):
        responseInfo = helpers.analyzeResponse(messageInfo.getResponse())
        headers = responseInfo.getHeaders()
        msgBody = messageInfo.getResponse()[responseInfo.getBodyOffset():]
        response = helpers.bytesToString(msgBody)
        response = re.sub('original', 'modified', response) # regex for modification of response, can also do replacement via "response = 'newresponse'"
        #print(response) # debug
        msgBody = helpers.stringToBytes(response)
        message = helpers.buildHttpMessage(headers, msgBody)
        messageInfo.setResponse(message)
        print('Completed response modification!')
else: # optional request modification
    reqBytes = messageInfo.getRequest()
    req = helpers.analyzeRequest(reqBytes)
    body = reqBytes[(req.getBodyOffset()):].tostring()
    headers = req.getHeaders()
    if "Test123" in body: # value to replace in request
        body = "TEST1234" # new value to use in request
    newreq = helpers.buildHttpMessage(headers, body)
    messageInfo.setRequest(newreq)
