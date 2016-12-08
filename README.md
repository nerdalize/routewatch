# routewatch
Routewatch brings automated alerting to YABGP.

Network operators frequently hear about routing issues from their customers before they become aware of it themselves. After all the internet is a complicated constantly changing spaghetti-like graph of loosely associated nodes (networks).

While BGP does a lot to abstract away all the complexity and inconsistencies occasionally routes go missing and suddenly you can't access a website.

A lot of the time BGP instabilities are due to human error such as accidental announcements of internal aggregations to upstream providers (most Tier-1 and Tier-2 networks prefer customer routes to peer routes).
But as with most things, awareness of a problem is the first step towards a solution, and the sooner you are aware the sooner you can fix it.

Routewatch helps by monitoring the availability of CIDR prefixes in your YABGP LookingGlass, if for any reason you loose access to one or more of the prefixes you care about routewatch sends an e-mail to everyone in it's recipient list informing them of the failure. 
When the affected prefixes become visible again it e-mails everyone once more to inform them that the issue has passed.

Routerwatch is considered production ready, although not yet feature rich or by any measure pretty, and is actively used at Nerdalize to monitor both our iBGP and our eBGP RIBs.


*Please pay close attention to the settings part of this readme as misconfiguration will erther result in either no e-mails or large numbers of false positives being sent.*

## Security

While it's presently surplus to requirement as the database is a sqlite3 file stored in the same file as the service, and not to mention I've not added https support yet, it might be interesting to note that routewatch explicitly requires that certain settings are encryptedwhen stored in the DB.
This is because the intention is to support external databases such as postgresql or mariaDB so that prefixes may be inserted automatically by your IPAM (IP Address Management) system, and storing security credentials in plain text on an untrusted location is stupid.

### NOTICE:

It is highly recommended that you use a YABGP instance that is set up as a LookingGlass only, that is to say that your primary BGP routers don't accept announcements or updates from it, because you will be storing the access credentials in routewatch and we don't guarantee the safety of these credentials, nor the routewatch system.


## Running in Docker
Routewatch is expected to be used inside a docker container (Dockerfile supplied), however this is not a strict requirement.


To build the docker image:
	
	docker build -t routewatch .

To run the docker image:

	docker run --name=routewatch --restart=always -p 80:80 -d routewatch


## Running Native
Routewatch doesn't currently have a stable daemonised running mode so it is recommended that production environments utilise the docker image.

For development purposes users can simply start the program in a terminal emulator:
	
	./runserver.py


## Settings
There are a number of settings that must be supplied before routewatch can start monitoring routes. All settings are configured through the web interface that it exposes.
It is required that you configure all the settings correctly before adding either recipients or prefixes, failure to do so may result in anomalous results.

![settings screenshot](https://github.com/nerdalize/routewatch/raw/master/screenshots/settings.png "Settings list")
	
![add setting screenshot](https://github.com/nerdalize/routewatch/raw/master/screenshots/add_setting.png "Add setting form")


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

![prefixes screenshot](https://github.com/nerdalize/routewatch/raw/master/screenshots/prefixes.png "Prefixes list")
	
![add prefix screenshot](https://github.com/nerdalize/routewatch/raw/master/screenshots/add_prefix.png "Add prefix form")

        [prefix]			[protocol]
        some_prefix_in_cidr		4


## Recipients
Every recipient in the recipients list will be sent an e-mail when a monitored prefix changes state.
The states that trigger e-mails are:

 - Not Found / Lost
 - Found / Recovered
 - Cancelled (a special state triggered when a Not Found / Lost prefix is removed from the prefix list)

The initial state is *Found*, meaning that adding a prefix to the monitor list that is not visible to the LookingGlass will trigger an e-mail.

![recipients screenshot](https://github.com/nerdalize/routewatch/raw/master/screenshots/recipients.png "Recipients list")
	
![add recipient screenshot](https://github.com/nerdalize/routewatch/raw/master/screenshots/add_recipient.png "Add recipient form")


## Contributions
Contributions to routewatch are definitely welcome, if you'd like to get involved please get intouch through github.


## Feature requests and bug reports
Yeah... if it's a security issue it'll get fixed, if it's not a security issue then don't hold your breath.


## License and copyright

This software is licensed under the MIT License.
A copy should have been provided to you with the software.
