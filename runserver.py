#!/bin/env python3

from multiprocessing import Process

from routewatch.UI import app
from routewatch.Security.crypto import get_secret


def check_state(secret=None):
    """
    The belly of the beast.
    Check state is a simple process that loops approximately every 5 seconds checking all the prefixes defined in the DB
    against the RIB and sends alerts if the status of a prefix changes (I.E. from Found to Missing).
    :param secret:
    :type secret: bytes or None
    :return:
    """
    from time import sleep
    import logging

    from routewatch.Agents.email import email
    from routewatch.Agents.yabgp_api import LookingGlass

    from routewatch.DB.client import DB as database
    LG = LookingGlass(secret)
    DB = database()
    state = dict()
    while True:
        try:
            # Pull all IPv4 Prefixes from the DB
            IPv4 = [prefix.prefix for prefix in DB.get("Prefix", protocol=4)]
            IPv4_result = LG.IPv4.check_prefixes(IPv4)
            # Filter the result for changes
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
            # If there are changes email them to the recipients listed in the DB
            if len(changed) > 0:
                email(changed, [recipient.email for recipient in DB.get("Recipient")], secret)
            sleep(5)
        except:
            logging.exception("An unexpected exception occurred")


if __name__ == "__main__":
    # Launch the RouteWatch[er]
    secret = get_secret()
    state_monitor = Process(target=check_state, kwargs={"secret": secret})
    state_monitor.start()
    # Launch the Web-GUI
    app.run(host="0.0.0.0", port=80)

