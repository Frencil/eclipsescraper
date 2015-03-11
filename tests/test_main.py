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
                                  'type': 'unknown',
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
                                              'semiMajorAxis': {'number': ['2017-08-21T16:50:00Z', 35000.0,
                                                                           '2017-08-21T20:00:00Z', 35500.0]},
                                              'semiMinorAxis': {'number': ['2017-08-21T16:50:00Z', 35000.0,
                                                                           '2017-08-21T20:00:00Z', 35500.0]},
                                              
                                              },
                                  'position': {'cartographicDegrees': ['2017-08-21T16:50:00+00:00', -162.85, 41.487, 0.0,
                                                                       '2017-08-21T20:00:00+00:00', -37.658, 13.577, 0.0]},
                                  },
                                 ]

    expected_czml['20150320'] = [{'clock': {'range': 'LOOP_STOP', 'currentTime': '2015-03-20T09:14:00Z', 'step': 'SYSTEM_CLOCK_MULTIPLIER', 'interval': '2015-03-20T09:14:00Z/2015-03-20T10:18:00Z', 'multiplier': 300}, 'id': 'document', 'version': '1.0'}, {'polyline': {'material': {'solidColor': {'color': {'rgba': [255, 255, 255, 128]}}}, 'positions': {'cartographicDegrees': [-37.218, 56.167, 0.0, -33.195, 56.785, 0.0, -30.188, 57.413, 0.0, -27.697, 58.052, 0.0, -25.523, 58.702, 0.0, -23.572, 59.365, 0.0, -21.783, 60.04, 0.0, -20.117, 60.73, 0.0, -18.547, 61.437, 0.0, -17.053, 62.157, 0.0, -15.622, 62.897, 0.0, -14.237, 63.653, 0.0, -12.892, 64.433, 0.0, -11.577, 65.235, 0.0, -10.283, 66.06, 0.0, -9.003, 66.915, 0.0, -7.733, 67.8, 0.0, -6.463, 68.72, 0.0, -5.19, 69.678, 0.0, -3.907, 70.683, 0.0, -2.607, 71.74, 0.0, -1.285, 72.86, 0.0, 0.065, 74.055, 0.0, 1.447, 75.345, 0.0, 2.857, 76.757, 0.0, 4.272, 78.333, 0.0, 5.608, 80.155, 0.0, 6.483, 82.395, 0.0, 3.503, 85.655, 0.0]}, 'show': True, 'width': 1, 'followSurface': True}, 'id': '2015-03-20_north_polyline'}, {'polyline': {'material': {'polylineGlow': {'glowPower': 0.25, 'color': {'rgba': [223, 150, 47, 128]}}}, 'positions': {'cartographicDegrees': [-37.718, 53.97, 0.0, -33.0, 54.535, 0.0, -29.712, 55.115, 0.0, -27.053, 55.705, 0.0, -24.765, 56.307, 0.0, -22.727, 56.92, 0.0, -20.867, 57.545, 0.0, -19.143, 58.18, 0.0, -17.523, 58.828, 0.0, -15.987, 59.49, 0.0, -14.513, 60.165, 0.0, -13.093, 60.857, 0.0, -11.713, 61.562, 0.0, -10.365, 62.285, 0.0, -9.038, 63.025, 0.0, -7.725, 63.787, 0.0, -6.422, 64.568, 0.0, -5.117, 65.375, 0.0, -3.805, 66.208, 0.0, -2.478, 67.068, 0.0, -1.13, 67.962, 0.0, 0.253, 68.892, 0.0, 1.68, 69.863, 0.0, 3.163, 70.883, 0.0, 4.722, 71.96, 0.0, 6.378, 73.102, 0.0, 8.163, 74.327, 0.0, 10.125, 75.655, 0.0, 12.335, 77.118, 0.0, 14.927, 78.773, 0.0, 18.18, 80.72, 0.0, 22.942, 83.215, 0.0, 39.362, 87.733, 0.0]}, 'show': True, 'width': 5, 'followSurface': True}, 'id': '2015-03-20_central_polyline'}, {'polyline': {'material': {'solidColor': {'color': {'rgba': [255, 255, 255, 128]}}}, 'positions': {'cartographicDegrees': [-30.027, 52.943, 0.0, -27.087, 53.49, 0.0, -24.623, 54.048, 0.0, -22.463, 54.618, 0.0, -20.513, 55.198, 0.0, -18.722, 55.79, 0.0, -17.048, 56.392, 0.0, -15.468, 57.003, 0.0, -13.963, 57.628, 0.0, -12.517, 58.265, 0.0, -11.117, 58.913, 0.0, -9.755, 59.577, 0.0, -8.42, 60.253, 0.0, -7.107, 60.945, 0.0, -5.805, 61.653, 0.0, -4.51, 62.378, 0.0, -3.215, 63.123, 0.0, -1.912, 63.888, 0.0, -0.595, 64.677, 0.0, 0.745, 65.488, 0.0, 2.115, 66.328, 0.0, 3.525, 67.198, 0.0, 4.987, 68.102, 0.0, 6.513, 69.043, 0.0, 8.125, 70.03, 0.0, 9.842, 71.067, 0.0, 11.697, 72.163, 0.0, 13.732, 73.332, 0.0, 16.012, 74.59, 0.0, 18.643, 75.962, 0.0, 21.808, 77.488, 0.0, 25.888, 79.235, 0.0, 31.868, 81.345, 0.0]}, 'show': True, 'width': 1, 'followSurface': True}, 'id': '2015-03-20_south_polyline'}, {'ellipse': {'material': {'solidColor': {'color': {'rgba': [0, 0, 0, 160]}}}, 'semiMinorAxis': {'number': ['2015-03-20T09:14:00Z', 219000.0, '2015-03-20T09:16:00Z', 228500.0, '2015-03-20T09:18:00Z', 234500.0, '2015-03-20T09:20:00Z', 238500.0, '2015-03-20T09:22:00Z', 241000.0, '2015-03-20T09:24:00Z', 242500.0, '2015-03-20T09:26:00Z', 243500.0, '2015-03-20T09:28:00Z', 243500.0, '2015-03-20T09:30:00Z', 243500.0, '2015-03-20T09:32:00Z', 242500.0, '2015-03-20T09:34:00Z', 241500.0, '2015-03-20T09:36:00Z', 240000.0, '2015-03-20T09:38:00Z', 238500.0, '2015-03-20T09:40:00Z', 237000.0, '2015-03-20T09:42:00Z', 235000.0, '2015-03-20T09:44:00Z', 233000.0, '2015-03-20T09:46:00Z', 231000.0, '2015-03-20T09:48:00Z', 229000.0, '2015-03-20T09:50:00Z', 227000.0, '2015-03-20T09:52:00Z', 225000.0, '2015-03-20T09:54:00Z', 223000.0, '2015-03-20T09:56:00Z', 221000.0, '2015-03-20T09:58:00Z', 219000.0, '2015-03-20T10:00:00Z', 217000.0, '2015-03-20T10:02:00Z', 215500.0, '2015-03-20T10:04:00Z', 213500.0, '2015-03-20T10:06:00Z', 212000.0, '2015-03-20T10:08:00Z', 210500.0, '2015-03-20T10:10:00Z', 209000.0, '2015-03-20T10:12:00Z', 208000.0, '2015-03-20T10:14:00Z', 207000.0, '2015-03-20T10:16:00Z', 206000.0, '2015-03-20T10:18:00Z', 205000.0]}, 'show': True, 'semiMajorAxis': {'number': ['2015-03-20T09:14:00Z', 219000.0, '2015-03-20T09:16:00Z', 228500.0, '2015-03-20T09:18:00Z', 234500.0, '2015-03-20T09:20:00Z', 238500.0, '2015-03-20T09:22:00Z', 241000.0, '2015-03-20T09:24:00Z', 242500.0, '2015-03-20T09:26:00Z', 243500.0, '2015-03-20T09:28:00Z', 243500.0, '2015-03-20T09:30:00Z', 243500.0, '2015-03-20T09:32:00Z', 242500.0, '2015-03-20T09:34:00Z', 241500.0, '2015-03-20T09:36:00Z', 240000.0, '2015-03-20T09:38:00Z', 238500.0, '2015-03-20T09:40:00Z', 237000.0, '2015-03-20T09:42:00Z', 235000.0, '2015-03-20T09:44:00Z', 233000.0, '2015-03-20T09:46:00Z', 231000.0, '2015-03-20T09:48:00Z', 229000.0, '2015-03-20T09:50:00Z', 227000.0, '2015-03-20T09:52:00Z', 225000.0, '2015-03-20T09:54:00Z', 223000.0, '2015-03-20T09:56:00Z', 221000.0, '2015-03-20T09:58:00Z', 219000.0, '2015-03-20T10:00:00Z', 217000.0, '2015-03-20T10:02:00Z', 215500.0, '2015-03-20T10:04:00Z', 213500.0, '2015-03-20T10:06:00Z', 212000.0, '2015-03-20T10:08:00Z', 210500.0, '2015-03-20T10:10:00Z', 209000.0, '2015-03-20T10:12:00Z', 208000.0, '2015-03-20T10:14:00Z', 207000.0, '2015-03-20T10:16:00Z', 206000.0, '2015-03-20T10:18:00Z', 205000.0]}, 'fill': True}, 'id': '2015-03-20_shadow_ellipse', 'position': {'cartographicDegrees': ['2015-03-20T09:14:00+00:00', -37.718, 53.97, 0.0, '2015-03-20T09:16:00+00:00', -33.0, 54.535, 0.0, '2015-03-20T09:18:00+00:00', -29.712, 55.115, 0.0, '2015-03-20T09:20:00+00:00', -27.053, 55.705, 0.0, '2015-03-20T09:22:00+00:00', -24.765, 56.307, 0.0, '2015-03-20T09:24:00+00:00', -22.727, 56.92, 0.0, '2015-03-20T09:26:00+00:00', -20.867, 57.545, 0.0, '2015-03-20T09:28:00+00:00', -19.143, 58.18, 0.0, '2015-03-20T09:30:00+00:00', -17.523, 58.828, 0.0, '2015-03-20T09:32:00+00:00', -15.987, 59.49, 0.0, '2015-03-20T09:34:00+00:00', -14.513, 60.165, 0.0, '2015-03-20T09:36:00+00:00', -13.093, 60.857, 0.0, '2015-03-20T09:38:00+00:00', -11.713, 61.562, 0.0, '2015-03-20T09:40:00+00:00', -10.365, 62.285, 0.0, '2015-03-20T09:42:00+00:00', -9.038, 63.025, 0.0, '2015-03-20T09:44:00+00:00', -7.725, 63.787, 0.0, '2015-03-20T09:46:00+00:00', -6.422, 64.568, 0.0, '2015-03-20T09:48:00+00:00', -5.117, 65.375, 0.0, '2015-03-20T09:50:00+00:00', -3.805, 66.208, 0.0, '2015-03-20T09:52:00+00:00', -2.478, 67.068, 0.0, '2015-03-20T09:54:00+00:00', -1.13, 67.962, 0.0, '2015-03-20T09:56:00+00:00', 0.253, 68.892, 0.0, '2015-03-20T09:58:00+00:00', 1.68, 69.863, 0.0, '2015-03-20T10:00:00+00:00', 3.163, 70.883, 0.0, '2015-03-20T10:02:00+00:00', 4.722, 71.96, 0.0, '2015-03-20T10:04:00+00:00', 6.378, 73.102, 0.0, '2015-03-20T10:06:00+00:00', 8.163, 74.327, 0.0, '2015-03-20T10:08:00+00:00', 10.125, 75.655, 0.0, '2015-03-20T10:10:00+00:00', 12.335, 77.118, 0.0, '2015-03-20T10:12:00+00:00', 14.927, 78.773, 0.0, '2015-03-20T10:14:00+00:00', 18.18, 80.72, 0.0, '2015-03-20T10:16:00+00:00', 22.942, 83.215, 0.0, '2015-03-20T10:18:00+00:00', 39.362, 87.733, 0.0]}}]


    # Test creation of a track object
    def test_Initialize(self):

        test_date = date(2017, 8, 21)
        test_track = eclipsescraper.EclipseTrack(test_date)
        expected_track = {'date': date(2017, 8, 21),
                          'type': 'unknown',
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


    # To prevent excessive load on the actual eclipse site HTML should be presupplied for various types of events.
    # Test loadFromURL once and only once with a test URL staged on eclipsetracks.org
    def test_Scrape20150320_loadFromURL(self):

        test_date = date(2015, 3, 20)
        test_track = eclipsescraper.EclipseTrack(test_date)
        test_track.loadFromURL('http://eclipsetracks.org/test/eclipsescraper_test_SE2015Mar20Tpath.html')
        test_czml = test_track.czml()
        self.assertEqual(test_czml, self.expected_czml['20150320'])

        test_camera_position = test_track.getCameraPosition()
        self.assertEqual(test_camera_position, [-6.422, 64.568, 10000000.0])

        test_json = test_track.json()
        self.assertEqual(test_json, {'type': 'total',
                                     'camera_position': [-6.422, 64.568, 10000000.0]})

    
    # Test the full scraping of the 2017-08-21 event (abbreviated).
    def test_Scrape20170821_loadFromRawHTML(self):

        test_date = date(2017, 8, 21)
        test_track = eclipsescraper.EclipseTrack(test_date)
        test_html = self.test_html['20170821']
        test_track.loadFromRawHTML(test_html)
        self.assertEqual(test_track.data(), self.expected_track['20170821'])

        test_czml = test_track.czml()
        self.assertEqual(test_czml, self.expected_czml['20170821'])

        test_camera_position = test_track.getCameraPosition()
        self.assertEqual(test_camera_position, [-37.658, 13.577, 10000000.0])

        test_json = test_track.json()
        self.assertEqual(test_json, {'type': 'unknown',
                                     'camera_position': [-37.658, 13.577, 10000000.0]})


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseClassesTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
