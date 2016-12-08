import requests

from routewatch.DB.client import DB as database
from routewatch.Security.crypto import decrypt

DB = database()


class Protocol(object):
    def __init__(self, LG, proto):
        """
        A Protocol baseclass for wrapping the YABGP API
        :param LG:
        :type LG: LookingGlass
        :param proto:
        :type proto: str
        """
        self.LG = LG
        self.proto = proto

    def check_prefixes(self, prefixes):
        """
        Checks that all the prefixes in the list supplied are in the RIB and returns the prefixes filtered into two lists.
        :param prefixes:
        :type prefixes: list
        :return: results
        :rtype: dict
        """
        try:
            # Get the LookingGlass address and the IP of the router we want to check from the DB.
            lookingglass_url = DB.get("Settings", name="lg_url")[0].data
            router = DB.get("Settings", name="monitored_router")[0].data
        except:
            lookingglass_url = ""
            router = ""
        # Request the prefix list for that router from YABGP
        lg_response = self.LG.__get__("{}{}{}/{}".format(lookingglass_url, "adj-rib-in/", self.proto, router))
        lg_prefixes = lg_response["prefixes"]
        # Search for the monitored prefixes in the list received from the LookingGlass appending them to the
        # appropriate bucket.
        missing = list()
        good = list()
        for prefix in prefixes:
            if prefix not in lg_prefixes:
                missing.append(prefix)
            else:
                good.append(prefix)
        return {"NotFound": missing, "Found": good}

    def check_aspath(self, routes):
        """
        A deeper check than check_prefixes that validates the ASPATH matches the expected path. this has limited
        use cases so it's not exposed anywhere yet. That is to say, I don't need it right now, so I'm just leaving it
        here.
        :param routes:
        :type routes: dict
        :return: results
        :rtype: dict
        """
        try:
            # Get the LookingGlass address and the IP of the router we want to check from the DB.
            lookingglass_url = DB.get("settings", name="lg_url")
            router = DB.get("settings", name="monitored_router")
        except:
            lookingglass_url = ""
            router = ""
        # Request the full ASPATHs from YABGP
        lg_response = self.LG.__get__("{}{}{}/{}".format(lookingglass_url, "adj-rib-all/", self.proto, router))
        # Search for the monitored prefixes in the list received from the LookingGlass checking that the ASPATH matches
        # and sorting them into the appropriate buckets.
        missing = list()
        good = list()
        for prefix in routes.keys():
            if prefix not in lg_response.keys():
                missing.append({"Prefix": prefix, "ASPath": -1, "Valid": False})
            else:
                good.append(dict(Prefix=prefix, ASPath=lg_response[prefix]["2"][0][1],
                                 Match=(routes[prefix] == lg_response[prefix]["2"][0][1])))
        return {"NotFound": missing, "Found": good}


class LookingGlass(object):
    def __init__(self, secret=None):
        """
         A simple container for the to hold the LookingGlass credentials and instances.
         Due to the way most BGP implementations are set up this is split into one face per IP protocol version.
        :param secret:
        :type secret: bytes
        """
        self.IPv4 = Protocol(self, "ipv4")
        self.IPv6 = Protocol(self, "ipv6")
        self.secret = secret

    def __get__(self, url):
        """
        A common get wrapper and authentication holder for all all the sub-levels.
        :param url:
        :type url: str
        :return: results
        :rtype: dict
        """
        try:
            # Get the credentials from the DB
            encrypted_username = DB.get("Settings", name="lg_user")[0].encode()
            encrypted_password = DB.get("Settings", name="lg_password")[0].encode()
            # Decrypt the credentials
            username = decrypt(encrypted_username.data, self.secret).decode()
            password = decrypt(encrypted_password.data, self.secret).decode()
        except:
            username = "admin"
            password = "password"
        # Send the request and pull the json from the result
        return requests.get(url, auth=(username, password)).json()
