from requests import get
from concurrent.futures import ThreadPoolExecutor

class LocationChecker:
    def __init__(self, ValidLocations = []) -> None:
        self.validLocations = ValidLocations
        self.ipList = []
        self.validIPs = []
        self.rdap_api = "https://rdap.apnic.net/ip/"

    def getLocation(self, IP = "") -> str:
        ip = IP.split(":")[0]

        request = get(f'{self.rdap_api}{ip}')

        if request.status_code == 429:
            print("Sent too many requestes")

        requestData = request.json()

        return requestData.get("country")


    def isLocation(self, IP = "", startedByMass = False) -> bool:
        location = self.getLocation(IP=IP)

        if location in self.validLocations:
            if startedByMass:
                self.validIPs.append(IP)
                
            return True

        return False


    def massIsLocation(self) -> bool:
        pool = ThreadPoolExecutor(max_workers=50)
        
        while len(self.ipList) > 0:
            pool.submit(self.isLocation, self.ipList[-1], True)
            self.ipList.pop()
            
        pool.shutdown(wait=True)
        return True
    
    
    def setList(self, IPS = []) -> None:
        self.ipList = IPS


    def getValid(self) -> list:
        return self.validIPs