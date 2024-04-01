import requests

class ProxyScraper:

    def __init__(self, ApiFile = "imports/assets/websiteList.txt", OutputFile = "proxys.txt") -> None:
        self.apiFile = ApiFile
        self.outputFile = OutputFile
        self.apis = []


    def getApis(self) -> None:
        apiFile = open(self.apiFile, "r")
        apiList = apiFile.readlines()

        for api in apiList:
            if api == "\n":
                continue

            self.apis.append(api.strip("\n"))


    def scrape(self, saveAsFile = False) -> list:
        self.getApis()

        proxys = []

        for api in self.apis:
            request = requests.get(api)
            requestData = request.text.split("\n")
            for proxy in requestData:
                if proxy in proxys:
                    continue

                proxys.append(proxy.strip("\r"))
        
        if saveAsFile:
            outputFile = open(self.outputFile, "w")
            toWrite = ""

            for proxy in proxys:
                toWrite += proxy + "\n"
                
            outputFile.write(toWrite)
            outputFile.close()

        return proxys
