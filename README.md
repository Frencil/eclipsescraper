# Eclipse Scraper

Python module for scraping NASA's eclipse site into usable CZML documents

## Overview

This module is designed for scraping tabular data for the tracks of eclipse events from NASA's eclipse website ([http://eclipse.gsfc.nasa.gov/](http://eclipse.gsfc.nasa.gov/)) and converting such events into CZML documents for display with [Cesium](https://github.com/AnalyticalGraphicsInc/cesium). This module is developed in tandem with [EclipseTracks.org](http://eclipsetracks.org] ([source](https://github.com/Frencil/eclipsetracks)).

Eclipse Predictions by Fred Espenak, NASA's GSFC.

## Dependencies

This module requires [czml](https://github.com/cleder/czml), the Python CZML reader/writer.

## Testing

Run tests in the top-level directory like so:

```
python setup.py test
```

Eclipse Scraper is continually tested with [Travis CI](https://travis-ci.org/Frencil/eclipsescraper).

[![Build Status](https://api.travis-ci.org/Frencil/eclipsescraper.png)](https://travis-ci.org/Frencil/eclipsescraper)
[![Coverage Status](https://coveralls.io/repos/Frencil/eclipsescraper/badge.svg?branch=master)](https://coveralls.io/r/Frencil/eclipsescraper?branch=master)