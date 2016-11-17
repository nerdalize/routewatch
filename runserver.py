#!/bin/env python3

from multiprocessing import Process

from RouteWatch.UI import app
from RouteWatch.Security.crypto import get_secret


def check_state(secret=None):
    from time import sleep
    import logging

    from RouteWatch.Agents.email import email
    from RouteWatch.Agents.yabgp_api import LookingGlass

    from RouteWatch.DB.client import DB as database
    LG = LookingGlass(secret)
    DB = database()
    state = dict()
    while True:
        try:
            IPv4 = [prefix.prefix for prefix in DB.get("Prefix", protocol=4)]
            IPv4_result = LG.IPv4.check_prefixes(IPv4)
            changed = list()
            for prefix in IPv4_result["NotFound"]:
                if not bool(state.get(prefix)):
                    changed.append("Route to {} was lost".format(prefix))
                    state[prefix] = "NotFound"
            for prefix in list(state.keys()):
                if prefix not in IPv4:
                    changed.append("Monitoring of {} was stopped".format(prefix))
                    del state[prefix]
                elif prefix not in IPv4_result["NotFound"]:
                    changed.append("Route to {} was found".format(prefix))
                    del state[prefix]
            if len(changed) > 0:
                print("emailing")
                email(changed, [recipient.email for recipient in DB.get("Recipient")], secret)
            sleep(5)
        except:
            logging.exception("An unexpected exception occured")


if __name__ == "__main__":
    secret = get_secret()
    state_monitor = Process(target=check_state, kwargs={"secret": secret})
    state_monitor.start()
    app.run(host="0.0.0.0", port=80)

