import imports.proxyScraper as proxyScraper
import imports.locationChecker as locationChecker
import imports.proxyChecker as proxyChecker

import threading

import random
import flask
import time

class ProxyService:
    def __init__(self):
        self.forceRefresh = False
        self.validProxys = []

    def proxyRefresh(self) -> None:
        locateInstance = locationChecker.LocationChecker(ValidLocations=["Germany", "Spain", "France", "Greece", "Italy", "Finland", "Ireland", "Croatia", "Sweden", "Netherlands", "Norway", "Poland"])
        scrapeInstance = proxyScraper.ProxyScraper()
        checkerInstance = proxyChecker.ProxyChecker()

        lastUpdate = 0

        while True:
            if time.time() - lastUpdate > 300 or self.forceRefresh:

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


    def getValid(self) -> list:
        return self.validProxys

    def triggerForceRefresh(self) -> bool:
        self.forceRefresh = True
        return True
    
    def getArrayLenght(self) -> int:
        return len(self.validProxys)

    def startServer(self) -> None:
        server.run(debug=True, host='0.0.0.0')


server = flask.Flask(__name__)
proxyServiceInstance = ProxyService()


@server.route("/")
def index():
    return ""


@server.route("/proxy", methods = ['GET'])
def proxy():
    proxys = proxyServiceInstance.getValid()
    if len(proxys) == 0:
        return {
            "status": False
        }
    
    return {
        "status": True,
        "proxy": random.choice(proxys)
    }


@server.route("/proxy_array_length", methods = ['GET'])
def proxy_array_lenght():
    return str(proxyServiceInstance.getArrayLenght())


@server.route("/proxy_array_force_refresh", methods = ['POST'])
def proxy_array_force_refresh():
    return str(proxyServiceInstance.triggerForceRefresh())


if __name__ == "__main__":

    cool = threading.Thread(target=proxyServiceInstance.proxyRefresh)
    cool.start()

    proxyServiceInstance.startServer()

    while True:
        time.sleep(1)