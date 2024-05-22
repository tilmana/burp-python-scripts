from pyscripterer import BaseScript as Script
import re

args = [extender, callbacks, helpers, toolFlag, messageIsRequest, messageInfo, macroItems]
header_names = ["Cookie", "Authorization]
script = Script(*args)

if script.is_in_scope() and (callbacks.getToolName(toolFlag) == "Extensions"):
	if (messageIsRequest):
	    headers = req.getHeaders()
		if "authZ=True" in script.get_header_value("Cookie", headers):
			for header in header_names:
				headers.remove(header)
		reqBytes = messageInfo.getRequest()
		req = helpers.analyzeRequest(reqBytes)
		body = reqBytes[(req.getBodyOffset()):].tostring()
		headers = req.getHeaders()
		if 'viewstate' in state and 'viewstategenerator' in state and 'eventvalidation' in state:
			viewstate = r'__VIEWSTATE=([^&]+)'
			viewstategenerator = r'__VIEWSTATEGENERATOR=([^&]+)'
			eventvalidate = r'__EVENTVALIDATION=([^&]+)'
			body = re.sub(viewstate, state['viewstate'], body)
			body = re.sub(viewstategenerator, state['viewstategenerator'], body)
			body = re.sub(eventvalidate, state['eventvalidate'], body)
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
