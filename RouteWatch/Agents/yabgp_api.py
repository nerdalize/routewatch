import requests

from RouteWatch.DB.client import DB as database
from RouteWatch.Security.crypto import decrypt


DB = database()


class Protocol(object):

    def __init__(self, LG, proto):
        self.LG = LG
        self.proto = proto

    def check_prefixes(self, prefixes):
        try:
            lookingglass_url = DB.get("Settings", name="lg_url")[0].data
            router = DB.get("Settings", name="monitored_router")[0].data
        except:
            lookingglass_url = "http://10.1.2.1:8888/v1/"
            router = "10.1.255.251"
        lg_response = self.LG.__get__("{}{}{}/{}".format(lookingglass_url, "adj-rib-in/", self.proto, router))
        lg_prefixes = lg_response["prefixes"]
        missing = list()
        good = list()
        for prefix in prefixes:
            if prefix not in lg_prefixes:
                missing.append(prefix)
            else:
                good.append(prefix)
        return {"NotFound": missing, "Found": good}

    def check_aspath(self, routes):
        try:
            lookingglass_url = DB.get("settings", name="lg_url")
            router = DB.get("settings", name="monitored_router")
        except:
            lookingglass_url = "http://10.1.2.1:8888/v1/"
            router = "10.1.255.251"
        lg_response = self.LG.__get__("{}{}{}/{}".format(lookingglass_url, "adj-rib-all/", self.proto, router))
        missing = list()
        good = list()
        for prefix in routes.keys():
            if prefix not in lg_response.keys():
                missing.append({"Prefix":prefix, "ASPath": -1, "Valid": False})
            else:
                good.append(dict(Prefix=prefix, ASPath=lg_response[prefix]["2"][0][1],
                                 Match=(routes[prefix] == lg_response[prefix]["2"][0][1])))
        return {"NotFound": missing, "Found": good}

class LookingGlass(object):

    def __init__(self, secret=None):
        # Make connection
        self.IPv4 = Protocol(self, "ipv4")
        self.IPv6 = Protocol(self, "ipv6")
        self.secret = secret

    def __get__(self, url):
        try:
            encrypted_username = DB.get("Settings", name="lg_user")[0].encode()
            encrypted_password = DB.get("Settings", name="lg_password")[0].encode()
            username = decrypt(encrypted_username.data, self.secret).decode()
            password = decrypt(encrypted_password.data, self.secret).decode()
        except:
            username = "admin"
            password = "password"
        return requests.get(url, auth=(username, password)).json()
