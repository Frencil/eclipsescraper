# Eclipse Scraper

Python module for scraping NASA's eclipse site into usable CZML documents

## Overview

This module is designed for scraping tabular data for the tracks of eclipse events from NASA's eclipse website ([http://eclipse.gsfc.nasa.gov/](http://eclipse.gsfc.nasa.gov/)) and converting such events into CZML documents for dispaly with [Cesium](https://github.com/AnalyticalGraphicsInc/cesium). This module is developed in tandem with [eclipsetracks](https://github.com/Frencil/eclipsetracks), which in turn is hosted for public consumption at [eclipsetracks.org](http://eclipsetracks.org]).

## Dependencies

This module requires [czml](https://github.com/cleder/czml), the Python CZML reader/writer.

## Testing

Run tests in the top-level directory like so:

```
python setup.py test
```

EclipseScraper is cintinually tests with [Travis CI](https://travis-ci.org/Frencil/eclipsescraper).

![last build](https://api.travis-ci.org/Frencil/eclipsescraper.png)
![coverage](https://coveralls.io/repos/Frencil/eclipsescraper/badge.png?branch=master)
