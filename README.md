DCSO Threat Intelligence Engine (TIE) App for Splunk
====================================================

Copyright (c) 2015, 2020, DCSO Deutsche Cyber-Sicherheitsorganisation GmbH

Splunk App (Dashboard) for DCSO Threat Intelligence Engine (TIE).


# Prerequisites and Installation

* Python v3.7 or greater
* Splunk Enterprise 8 or greater
* DCSO TIE (legacy) or Portal API token (with Pinkback permission)
* Connection from your Splunk instance(s) to https://tie.dcso.de:443 (check your firewall setup)

## Installation

You can install the DCSO TIE App within the Splunk Enterprise Web interface:

1. click on the `splunk>enterprise`-logo
2. click on the wheel next next to 'Apps'
3. click 'Install app from file'
4. choose the file, navigating to the folder on your local machine containing a file called like `DCSO_TIE_Splunk_App2-2.0.0b1.zip`
5. if you are upgrading, make sure to check 'Upgrade app'
6. click 'Upload'

You can also install the app through the Splunk CLI (Command Line Interface):

```
${SPLUNK_HOME}/bin/splunk install app DCSO_TIE_Splunk_App2-2.0.0b1.zip
```

# Configuration

After installation, the app needs to be configured.

## Splunk App Setup Page

After installation you must setup the app or add-on.

Important: when a configuration is not correct, it is stored, but an error appears in the Splunk Web tool.
This error, however, does not tell you exactly what is wrong. You have to open the log file (see below) to
find out what exactly is wrong.

An API or Machine Token is required to access the Threat Intelligence Engine or TIE. Both the legacy
token created through `tie.dcso.de` and the newer tokens created through `portal.dcso.de` are supported.
If you have any questions about this Token, please contact DCSO (see below).

There are few more details about the configuration:

* **API Token**: either a legacy tie.dcso.de token, or new one created through the DCSO Portal.


## Pingback

Pingback is a function to report observations of the given IoCs. Only timestamp, count per second, data type and value is transferred.

## CIM Datamodels

For a working retro hunt please enable/accelerate the CIM datamodels "Web" and "Network Traffic".

#  Usage

## Logging

This app will log errors, warnings, and other informative messages to a separate log file within
the folder `${SPLUNK_HOME}/var/log/splunk`. The file is called `dcso_tie.log` and is rotated 6 times.

The entries in this log file are stored, when executed by Splunk, as JSON. This makes it ready to be
monitored by Splunk itself.

# Contact

* Email: ti-support [a] dcso.de
* Website: https://dcso.de

# Development & Deployment

## Deployment

The app can be packaged using the normal `distutils` command. However, for Splunk we need
to adapt a bit so that it is easy to create, deploy and install.

### For Splunk

This app has it's own `distutils` command called `splunkdist`:

```shell
$ python setup.py splunkdist --format=zip
```

The above command will create a ZIP archive in the folder `dist/`. The name of the file is so that
it contains the major and full version of this app. The folder it unpacks too has simply the
major version, for example:

```
$ python setup.py splunkdist --format=zip

# creates:
dist/DCSO_TIE_Splunk_App2-2.0.0b1.zip

$ unzip -l dist/DCSO_TIE_Splunk_App2-2.0.0b6.zip
Archive:  dist/DCSO_TIE_Splunk_App2-2.0.0b6.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  05-26-2020 13:36   DCSO_TIE_App2/
        0  05-26-2020 13:36   DCSO_TIE_App2/bin/
        0  05-26-2020 13:36   DCSO_TIE_App2/default/
        0  05-26-2020 13:36   DCSO_TIE_App2/static/
...
```

# License

See LICENSE file included in the repository.
