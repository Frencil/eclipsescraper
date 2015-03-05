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

    # To prevent excessive load on the actual eclipse site HTML should be presupplied for individual events.
    
    # Test the full scraping of the 2017-08-21 event.
    def test_Scrape20170821(self):

        self.maxDiff = None

        # Define test data
        test_date = date(2017, 8, 21)
        test_html = """foo<pre>
M:S                 Central
Universal  Northern Limit      Southern Limit       Central Line     Diam.  Sun Sun Path   Line
         ------------------  ------------------  ------------------  Ratio  Alt Azm Width Durat.
  Time   Latitude Longitude  Latitude Longitude  Latitude Longitude
          &#176;   &#180;     &#176;   &#180;      &#176;   &#180;     &#176;   &#180;      &#176;   &#180;     &#176;   &#180;            &#176;   &#176;   km
  
 Limits  39 59.7N 171 44.9W  39 28.8N 171 26.0W  39 44.2N 171 35.4W  1.016   0   -   62  00m51.6s
 16:50   41 29.7N 164 30.3W  41 25.2N 161 24.4W  41 29.2N 162 51.0W  1.018   7  80   70  01m01.6s
 20:02      -         -      11 46.0N 031 59.5W  11 34.2N 029 56.2W  1.015   3 282   60  00m50.5s
 Limits  11 15.6N 027 19.9W  10 46.9N 027 33.1W  11 01.2N 027 26.5W  1.014   0   -   57  00m47.1s
</pre>bar"""

        # Test preprocessing of HTML into raw data string
        rawdata = eclipsescraper.prep_raw_html(test_html)
        expected_rawdata = """M:S                 Central
Universal  Northern Limit      Southern Limit       Central Line     Diam.  Sun Sun Path   Line
         ------------------  ------------------  ------------------  Ratio  Alt Azm Width Durat.
  Time   Latitude Longitude  Latitude Longitude  Latitude Longitude
          &#176;   &#180;     &#176;   &#180;      &#176;   &#180;     &#176;   &#180;      &#176;   &#180;     &#176;   &#180;            &#176;   &#176;   km
  
 Limits  39 59.7N 171 44.9W  39 28.8N 171 26.0W  39 44.2N 171 35.4W  1.016   0   -   62  00m51.6s
 16:50   41 29.7N 164 30.3W  41 25.2N 161 24.4W  41 29.2N 162 51.0W  1.018   7  80   70  01m01.6s
 20:02      -         -      11 46.0N 031 59.5W  11 34.2N 029 56.2W  1.015   3 282   60  00m50.5s
 Limits  11 15.6N 027 19.9W  10 46.9N 027 33.1W  11 01.2N 027 26.5W  1.014   0   -   57  00m47.1s"""
        self.assertEqual(rawdata, expected_rawdata)

        # Test processing of raw data string into structured object
        track = eclipsescraper.EclipseTrack(rawdata)
        expected_track = {"vertexpositions":
                              {"central": [-162.85, 41.487, 0.0, -29.937, 11.57, 0.0],
                               "north": [-164.505, 41.495, 0.0],
                               "south": [-161.407, 41.42, 0.0, -31.992, 11.767, 0.0]},
                          "columns": ["Time", "NorthLimitLat", "NorthLimitLon", "SouthLimitLat", "SouthLimitLon", "CentralLat", "CentralLon", "MSDiamRatio", "SunAltitude", "SunAzimuth", "PathWidth", "CentralLineDuration"]}
        self.assertEqual(track.data(), expected_track)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseClassesTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
