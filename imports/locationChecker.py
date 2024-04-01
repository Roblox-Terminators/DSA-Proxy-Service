import requests
import concurrent.futures

class LocationChecker:
    def __init__(self, ValidLocations = []) -> None:
        self.validLocations = ValidLocations
        self.ipList = []
        self.validIPs = []


    def getLocation(self, IP = "") -> str:
        ip = IP.split(":")[0]

        request = requests.get(f'https://geolocation-db.com/json/{ip}&position=true') # https://ipinfo.io/1{ip}/json # https://geolocation-db.com/json/{ip}&position=true # https://ipapi.co/{ip}/json/

        if request.status_code == 429:
            print("sended to many requestes")

        requestData = request.json()

        return requestData.get("country_name")


    def isLocation(self, IP = "", startedByMass = False) -> bool:
        location = self.getLocation(IP=IP)

        if location in self.validLocations:
            if startedByMass:
                self.validIPs.append(IP)
                
            return True

        return False


    def massIsLocation(self) -> bool:
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=50)
        
        while len(self.ipList) > 0:
            pool.submit(self.isLocation, self.ipList[-1], True)
            self.ipList.pop()
            
        pool.shutdown(wait=True)
        return True
    
    
    def setList(self, IPS = []) -> None:
        self.ipList = IPS


    def getValid(self) -> list:
        return self.validIPs