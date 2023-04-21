from pyscripterer import BaseScript as Script
import re

args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]
script = Script(*args)

if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Proxy"): # checks in-scope target host and if tool is from Proxy, add "or" logic as necessary
	if (messageIsRequest):
		reqBytes = messageInfo.getRequest()
		req = helpers.analyzeRequest(reqBytes)
		body = reqBytes[(req.getBodyOffset()):].tostring()
		headers = req.getHeaders()
		if 'token' in state:
			pattern = r"(?<=code=)\w+" # regex to match CSRF token in request body
			body = re.sub(pattern, state['token'], body)
			newreq = helpers.buildHttpMessage(headers, body)
			messageInfo.setRequest(newreq)
	else:
		dompattern = r"<code>(\w+)<\/code>" # regex to match CSRF token in response body
		res = messageInfo.getResponse()
		fullRes = helpers.bytesToString(res)
		if re.search(dompattern, fullRes):
			state['token'] = str(re.search(dompattern, fullRes).group(0).split(">")[1].split("<")[0]) # sets state variable to the value of the CSRF token to be used in the subsequent request
			print(re.search(dompattern, fullRes).group(0).split(">")[1].split("<")[0])
