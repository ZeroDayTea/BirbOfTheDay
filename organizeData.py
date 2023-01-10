import json

dataFile = open("data.txt", "r")
resultsFile = open("birds.json", "w")

birdFamily = ""
birdsDict = {}
index = 0

for line in dataFile:
    if line[0:3] != "<a ":
        birdFamily = line.split("</h2>")[0]
    else:
        birdUrl = "https://www.allaboutbirds.org" + line.split("\"")[1]
        birdName = line.split("overview\">")[2].split("</a>")[0]
        birdImageUrl = line.split("src=\"")[1].split("\"")[0]
        index += 1
        birdIndex = {
            "name": birdName,
            "family": birdFamily,
            "url": birdUrl,
            "imageurl": birdImageUrl
        }
        birdsDict[index] = birdIndex

json.dump(birdsDict, resultsFile, indent=4)
