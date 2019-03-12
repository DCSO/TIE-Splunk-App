DCSO Threat Intelligence Engine (TIE) App for Splunk
=================================================================
Splunk App (Dashboard) for DCSO Threat Intelligence Engine (TIE).

Copyright (c) 2015, 2019, DCSO Deutsche Cyber-Sicherheitsorganisation GmbH

# 1. Prerequisites and Installation
* The default python major version of 
  * 7.1.2 is Python 2.7.x
  * 7.2.4 is Python 2.7.x
* All required python packages are pre-installed from Splunk itself. 
  * If any package is missing please open an issue to us and try to do: `pip install -r requirements.txt --no-cache`

## 1.1 Prerequisites
* Splunk
* [Splunk TIE TA](https://github.com/DCSO/TIE-Splunk-TA)
* Customer for the DCSO TI-Aggregation Package
* Generate an Token in the settings page of [TIE web interface](https://tie.dcso.de) with the following privileges:
  * tie
  * tie:pingback
* Firewall Requirements
    
    | Source                           | Destination | Protocol | Port | Comment    |
    | -------------------------------- | ----------- | -------- | ---- | ---------- |
    | \<Your Splunk server IP with the installed app\> | tie.dcso.de | TCP      | 443  | API access |

  
## 1.2 Installation

This app must be installed on a **Search Head** with an internet connection to reach the [API](https://tie.dcso.de) and the official CIM search add-on.

# 2. Configuration

## 2.1 Splunk Setup Page
The token has to be configured in the setup page of the app on the Splunk SH. You also have to enable the Pingback scripts.

*An access token is required for the API access. If you are already a customer and do not have one, please do not hesitate to contact us. If you are not a customer yet, please feel free to contact us for a demo account.*


## 2.2. Pingback

Pingback is a function to report observations of the given IoCs. 
Only timestamp, count per second, data type and value is transferred.

## 2.3 CIM Datamodels

For a working retro hunt please enable/accelerate the CIM datamodels "Web" and "Network Traffic".

# Contact
Mail: ti-support [a] dcso.de

Website: https://dcso.de

# License

Please have a look at the LICENSE file included in the repository.
