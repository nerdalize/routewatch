# RouteWatch
RouteWatch brings automated alerting to YABGP.

It watches a designated YABGP instance for prefix availability, if a prefix becomes unavailable Routewatch sends an e-mail to everyone in it's recipient list informing them of the failure. When the prefix becomes visible again it e-mails everyone once more to inform them that the issue has passed.

Please pay close attention to the settings part of this readme.


## Docker
RouteWatch is expected to be used inside a docker container (Dockerfile supplied), however this is not a strict requirement.


To build the docker image:
	
	docker build -t RouteWatch .

To run the docker image:

	docker run --name=RouteWatch --restart=always -p 80:80 -d RouteWatch


## Running Native
RouteWatch doesn't currently have a stable daemonised running mode so it is recommended that production environments utilise the docker image.

For development purposes users can simply start the program in a terminal emulator:
	
	./runserver.py


## Settings
There are a number of settings that must be supplied before RouteWatch can run.
It is required that you configure all the settings correctly before adding either recipients or prefixes, failure to do so may result in anomalous results.

### E-mail
Before all else it is recommended to configure the e-mail settings.

        [name]              [data]                  [encrypt flag]
        email_address       sender_address        	True
        email_password      smtp_password         	True
        email_user          smtp_user             	True
        email_server        smtp_server           	True

### LookingGlass
After E-mail it's best to configure the LookingGlass settings.
Currently only YABGP is supported, there are no plans to support others.

        [name]              [data]                  [encrypt flag]
        lg_url              YABGP_API_URL         	False
        lg_user             YABGP_user            	True
        lg_password         YABGP_password        	True
        monitored_router    peer_to_be_monitored  	False
        

## Prefixes
Prefixes are stored in CIDR format with an explicit IP protocol number (yes we could auto detect the protocol, but this would complicate the code).
At the time of writing only IPv4 support is being released. IPv6 is expected to be implemented in Q1 2017.

        [prefix]			[protocol]
        some_prefix_in_cidr		4


## Recipients
Every recipient in the recipients list will be sent an e-mail when a monitored prefix changes state.
The states that trigger e-mails are:

 - Not Found / Lost
 - Found / Recovered
 - Cancelled (a special state triggered when a Not Found / Lost prefix is removed from the prefix list)

The initial state is *Found*, meaning that adding a prefix to the monitor list that is not visible to the LookingGlass will trigger an e-mail.


## Contributions
Contributions to RouteWatch are definitely welcome, if you'd like to get involved please get intouch through github.


## Feature requests and bug reports
Yeah... if it's a scurity issue it'll get fixed, if it's not a security issue then don't hold your breath.


## License and copyright

This software is licensed under the Apache License 2.0.
A copy should have been provided to you with the software.
