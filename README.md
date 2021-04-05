# tabajaraWebmon


[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php) 

## Contents
1. [Introduction](#introduction)
2. [Requirements](#system-design)
3. [Running](#adding-expense)
4. [Features Not Implemented Yet](#Features-Not-Implemented-Yet)
5. [How to Contribute](#how-to-contribute)

##Introduction

This repository contains Tabajara Webmon's code. It is a webmonitor tool
that checks a set of basic metrics of a given URL and also monitors the 
occurencies of a regular expression (regex). It is designed to handle several
URLs and to be extensible to different application protocols (not only HTTP).


## Requirements

This session we describe Tabajara Webmon's main requirements.

### Functional Requirements
* User should be able to add URLs to monitor
* User should be able to specify what should be monitoring (basic monitoring
and/or regex monitoring)

### Non-Functional Requirements
* Reliable - system cannot lose monitoring data
* Scalable - should be able to add more monitoring nodes to the system without
effort

## Running

TBD


## Features Not Implemented Yet

Our Tabajara Webmon already has several cool features, however we are looking
forward to add more cool features. This session list some features that we
would like to add, in short-term, to Tabajara Webmon.
If you want to help us, refer to the session [How to Contribute](#how-to-contribute)
to send your Pull Request.

### Logging
The logging feature is an important feature to add to Tabajara Webmon to help
users to identify problems and crashes.

### Integration Tests
This initial version we implemented just unit tests. However, it would be nice
to add some integration tests to the system.


## How to Contribute

TBD