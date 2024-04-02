from imports.proxyScraper import ProxyScraper
from imports.locationChecker import LocationChecker
from imports.proxyChecker import ProxyChecker

import threading

import random
import flask
import time

class ProxyService:
    def __init__(self):
        self.forceRefresh = False
        self.validProxys = []

    def proxyRefresh(self) -> None:
        locateInstance = LocationChecker(ValidLocations = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"])
        scrapeInstance = ProxyScraper()
        checkerInstance = ProxyChecker()

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