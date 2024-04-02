import random
import flask

from imports.proxyService import ProxyService


server = flask.Flask(__name__)
proxyServiceInstance = ProxyService(server)


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

    with server.app_context():
        proxyServiceInstance.proxyRefresh()
    
    proxyServiceInstance.startServer()