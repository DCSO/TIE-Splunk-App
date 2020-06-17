# Changelog

All notable changes to the DCSO Threat Intelligence Engine (TIE) App for Splunk
will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0b1] - 2020-06-17

### Added

* Support for Splunk Enterprise v8, which means dropping support for Python v2.7.
  We will not support any longer Python 2.
* We include a `setup.py` which can be used to create a Splunk distribution using
  `setup.py splunkdist`. The resulting TAR or ZIP files can then be used to install
  through Splunk's web interface.
* The configuration of the Add-On within Splunk's web interface has been a bit
  reorganized and more help has been added.

## [1.0.0] - 2019-03-12

### Added

 Published Splunk app in version 1.0.0 at Github.com
