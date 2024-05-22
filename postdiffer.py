oldRequest = open("oldrequest.txt", "r")
newRequest = open("newrequest.txt", "r")

oldParams = []
oldValues = []
newParams = []
newValues = []

oldRequestData = oldRequest.readlines()[0].split("&")
newRequestData = newRequest.readlines()[0].split("&")

for value in oldRequestData:
    value = value.split("=")
    oldParams.append(value[0])
    oldValues.append(value[1])

for value in newRequestData:
    value = value.split("=")
    newParams.append(value[0])
    newValues.append(value[1])

oldParams = sorted(oldParams)
oldValues = sorted(oldValues)
newParams = sorted(newParams)
newValues = sorted(newValues)

for i in range(len(oldValues)):
    if oldValues[i] == newValues[i]:
        pass
    else:
        print(f"Diff in {oldParams[i]}")
        print(oldValues[i] + " / " + newValues[i])
