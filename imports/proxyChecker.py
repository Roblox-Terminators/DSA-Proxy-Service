import requests
import concurrent.futures

class ProxyChecker:
    def __init__(self, OutputFile = "checked_proxys.txt"):
        self.outputFile = OutputFile
        self.proxyList = []
        self.validProxys = []

    def checkProxy(self, Proxy) -> bool:
        proxy = Proxy.split(":")

        method = "socks5"
        request = requests.get('https://www.google.com', proxies={'socks': f'{method}://{proxy[0]}:{proxy[1]}'}, timeout=5)

        if request.status_code == 200:
            self.validProxys.append(f"{method}:{Proxy}")
            return True
        
        method = "socks4"
        request = requests.get('https://www.google.com', proxies={'socks': f'{method}://{proxy[0]}:{proxy[1]}'}, timeout=5)

        if request.status_code == 200:
            self.validProxys.append(f"{method}:{Proxy}")
            return True

        return False
    
    def massCheck(self) -> bool:
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=50)
        
        while len(self.proxyList) > 0:
            pool.submit(self.checkProxy, self.proxyList[-1])
            self.proxyList.pop()
            
        pool.shutdown(wait=True)
        return True
    

    def setList(self, Proxys) -> None:
        self.proxyList = Proxys

    def getValid(self, saveAsFile = False) -> list:
        if saveAsFile:
            outputFile = open(self.outputFile, "w")
            toWrite = ""

            for proxy in self.validProxys:
                toWrite += proxy + "\n"
                
            outputFile.write(toWrite)
            outputFile.close()

        return self.validProxys

    


