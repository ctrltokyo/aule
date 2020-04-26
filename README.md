# aule
A simple prometheus metrics gateway backed by SQLite.

## Description

The idea behind this is to create a simple boilerplate for a Prometheus "metrics fetch and expose" endpoint.    
This is useful for when you want to run arbitrary code (connect to PSQL, run a function etc.) and expose an endpoint for Prometheus to scrape, without worrying about the format.    
This tool is backed by a simple SQLite database, which allows for ease of backup, and also programmatic insertion of new metrics via plugins (soon).

## Setup
Use `pipenv install` to install dependencies.

## Usage
Look at `aule.py` and implement the components you want for your custom environment.

## Information

Missing:    
* Proper module support.
* Does not support labels at this point.
* Does not support enum types.
* Documentation.

© Alexander Nicholson (ctrlTokyo & DragonStuff)    
_Please read LICENCE.md for licencing information._
