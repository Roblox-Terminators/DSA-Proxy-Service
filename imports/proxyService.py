from imports.proxyScraper import ProxyScraper
from imports.locationChecker import LocationChecker
from imports.proxyChecker import ProxyChecker

import time

class ProxyService:
    def __init__(self, server):
        self.forceRefresh = False
        self.validProxys = []
        self.server = server

    def proxyRefresh(self) -> None:
        locateInstance = LocationChecker(ValidLocations = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"])
        scrapeInstance = ProxyScraper()
        checkerInstance = ProxyChecker()

        lastUpdate = 0

        while True:
            refreshTimer = (time.time() - lastUpdate > 300)
            if refreshTimer or self.forceRefresh:

                self.forceRefresh = False
                lastUpdate = time.time()

                proxys = scrapeInstance.scrape(saveAsFile=False)

                locateInstance.setList(proxys)
                locateInstance.massIsLocation()
                locatedProxies = locateInstance.getValid()

                checkerInstance.setList(locatedProxies)
                checkerInstance.massCheck()

                self.validProxys = checkerInstance.getValid()
                print(f"Proxy list updated! amount: {len(self.validProxys)}")
            time.sleep(1)


    def getValid(self) -> list:
        return self.validProxys

    def triggerForceRefresh(self) -> bool:
        self.forceRefresh = True
        return True
    
    def getArrayLenght(self) -> int:
        return len(self.validProxys)

    def startServer(self) -> None:
        self.server.run(debug=True, host='0.0.0.0')