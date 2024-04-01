# DSA-Proxy-Service
The DSA-Proxy-Service is a web server which is holding a list of active proxies.
The Proxy list gets updated every 5 minutes or via a force update request.

It got some inbuild tools:
- ProxyScraper
- LocationChecker
- ProxyChecker

These tools combined are able to filter the proxies for specific regions and also check if they are working.

After a request is sent to the server, it gives you a random proxy of the list back.
