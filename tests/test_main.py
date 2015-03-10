import unittest
from datetime import date

try:
    from czml import czml
except ImportError:
    import czml

try:
    from eclipsescraper import eclipsescraper
except ImportError:
    import eclipsescraper

class BaseClassesTestCase(unittest.TestCase):

    test_html = {}
    expected_track = {}
    expected_czml = {}

    # Define values for source html and expected tracks by event
    test_html['20170821'] = """foo<pre>
M:S                 Central
Universal  Northern Limit      Southern Limit       Central Line     Diam.  Sun Sun Path   Line
         ------------------  ------------------  ------------------  Ratio  Alt Azm Width Durat.
  Time   Latitude Longitude  Latitude Longitude  Latitude Longitude
          &#176;   &#180;     &#176;   &#180;      &#176;   &#180;     &#176;   &#180;      &#176;   &#180;     &#176;   &#180;            &#176;   &#176;   km
  
 Limits  39 59.7N 171 44.9W  39 28.8N 171 26.0W  39 44.2N 171 35.4W  1.016   0   -   62  00m51.6s
 16:50   41 29.7N 164 30.3W  41 25.2N 161 24.4W  41 29.2N 162 51.0W  1.018   7  80   70  01m01.6s
 20:00   13 39.6N 036 48.6W  13 28.6N 038 28.0W  13 34.6N 037 39.5W  1.017  11 280   71  01m02.5s
 Limits  11 15.6N 027 19.9W  10 46.9N 027 33.1W  11 01.2N 027 26.5W  1.014   0   -   57  00m47.1s
</pre>bar"""
    expected_track['20170821'] = {'date': date(2017, 8, 21),
                                  'columns': ['Time', 'NorthLimitLat', 'NorthLimitLon',
                                              'SouthLimitLat', 'SouthLimitLon', 'CentralLat', 'CentralLon',
                                              'MSDiamRatio', 'SunAltitude', 'SunAzimuth', 'PathWidth', 'CentralLineDuration'],
                                  'time': ['16:50','20:00'],
                                  'position': {'north': [(-164.505, 41.495), (-36.81, 13.66)],
                                               'central': [(-162.85, 41.487), (-37.658, 13.577)],
                                               'south': [(-161.407, 41.42), (-38.467, 13.477)]},
                                  'ms_diam_ratio': [1.018, 1.017],
                                  'sun_altitude': [7, 11],
                                  'sun_azimuth': [80, 280],
                                  'path_width': [70, 71],
                                  'central_line_duration': ['01m01.6s', '01m02.5s'],                        
                                  }
    expected_czml['20170821'] = [{'id': 'document',
                                  'version': '1.0',
                                  'clock': {'multiplier': 300,
                                            'range': 'LOOP_STOP',
                                            'step': 'SYSTEM_CLOCK_MULTIPLIER',
                                            'currentTime': '2017-08-21T16:50:00Z',
                                            'interval': '2017-08-21T16:50:00Z/2017-08-21T20:00:00Z',
                                            },
                                  },
                                 {'id': '2017-08-21_north_polyline',
                                  'polyline': {'width': 1,
                                               'show': True,
                                               'followSurface': True,
                                               'material': {'solidColor': {'color': { 'rgba': [255, 255, 255, 128] }}},
                                               'positions': {'cartographicDegrees': [-164.505, 41.495, 0.0, -36.81, 13.66, 0.0]},
                                               },
                                  },
                                 {'id': '2017-08-21_central_polyline',
                                  'polyline': {'width': 5,
                                               'show': True,
                                               'followSurface': True,
                                               'material': {'polylineGlow': {'color': { 'rgba': [223, 150, 47, 128] },
                                                                             'glowPower': 0.25}},
                                               'positions': {'cartographicDegrees': [-162.85, 41.487, 0.0, -37.658, 13.577, 0.0]},
                                               },
                                  },
                                 {'id': '2017-08-21_south_polyline',
                                  'polyline': {'width': 1,
                                               'show': True,
                                               'followSurface': True,
                                               'material': {'solidColor': {'color': { 'rgba': [255, 255, 255, 128] }}},
                                               'positions': {'cartographicDegrees': [-161.407, 41.42, 0.0, -38.467, 13.477, 0.0]},
                                               },
                                  },
                                 {'id': '2017-08-21_shadow_ellipse',
                                  'ellipse': {'fill': True,
                                              'show': True,
                                              'material': {'solidColor': {'color': { 'rgba': [0, 0, 0, 160] }}},
                                              'semiMajorAxis': {'number': ['2017-08-21T16:50:00Z', 70.0,
                                                                           '2017-08-21T20:00:00Z', 71.0]},
                                              'semiMinorAxis': {'number': ['2017-08-21T16:50:00Z', 70.0,
                                                                           '2017-08-21T20:00:00Z', 71.0]},
                                              
                                              },
                                  'position': {'cartographicDegrees': ['2017-08-21T16:50:00+00:00', -162.85, 41.487, 0.0,
                                                                       '2017-08-21T20:00:00+00:00', -37.658, 13.577, 0.0]},
                                  },
                                 ]

    # Test creation of a track object
    def test_Initialize(self):

        test_date = date(2017, 8, 21)
        test_track = eclipsescraper.EclipseTrack(test_date)
        expected_track = {'date': date(2017, 8, 21),
                          'columns': ['Time', 'NorthLimitLat', 'NorthLimitLon',
                                      'SouthLimitLat', 'SouthLimitLon', 'CentralLat', 'CentralLon',
                                      'MSDiamRatio', 'SunAltitude', 'SunAzimuth', 'PathWidth', 'CentralLineDuration'],
                          'time': [],
                          'position': {'north': [], 'central': [], 'south': []},
                          'ms_diam_ratio': [],
                          'sun_altitude': [],
                          'sun_azimuth': [],
                          'path_width': [],
                          'central_line_duration': [],    
                          }
        self.assertEqual(test_track.data(), expected_track)

    # To prevent excessive load on the actual eclipse site HTML should be presupplied for individual events.
    # Test the loadFromURL method once and only once with a test URL staged on eclipsetracks.org
    def test_loadFromURL(self):

        test_date = date(2017, 8, 21)
        test_track = eclipsescraper.EclipseTrack(test_date)
        test_track.loadFromURL('http://eclipsetracks.org/test/eclipsescraper_test_url.txt')
        test_czml = test_track.czml()
        self.assertEqual(test_czml, self.expected_czml['20170821'])
    
    # Test the full scraping of the 2017-08-21 event (abbreviated).
    def test_Scrape20170821(self):

        # Test loading object from raw HTML
        test_date = date(2017, 8, 21)
        test_track = eclipsescraper.EclipseTrack(test_date)
        test_html = self.test_html['20170821']
        test_track.loadFromRawHTML(test_html)
        self.assertEqual(test_track.data(), self.expected_track['20170821'])

        # Test generation of CZML
        test_czml = test_track.czml()
        self.assertEqual(test_czml, self.expected_czml['20170821'])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseClassesTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
