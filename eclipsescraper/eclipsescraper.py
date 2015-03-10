#!/usr/bin/python

import re, sys
from datetime import date

from lxml import html

if sys.version[0] is '3':
    import urllib.request
elif sys.version[0] is '2':
    import requests  

try:
    from czml import czml
except ImportError:
    import czml

class EclipseTrack:

    _properties = ('date', 'columns', 'url',
                   'time', 'position', 'ms_diam_ratio',
                   'sun_altitude', 'sun_azimuth',
                   'path_width', 'central_line_duration')

    # Start by taking a raw data string and parsing it build the waypoints list
    def __init__(self, date):

        self.date = date
        self.url = None
        self.html = None
        self.columns = [ 'Time','NorthLimitLat', 'NorthLimitLon', 'SouthLimitLat', 'SouthLimitLon', 'CentralLat', 'CentralLon',
                         'MSDiamRatio', 'SunAltitude', 'SunAzimuth', 'PathWidth', 'CentralLineDuration' ]
        self.time = []
        self.position = { 'north': [], 'south': [], 'central': [] }
        self.ms_diam_ratio = []
        self.sun_altitude = []
        self.sun_azimuth = []
        self.path_width = []
        self.central_line_duration = []

    def loadFromURL(self, url):
        self.url = url
        iso = self.date.isoformat()

        if sys.version[0] is '3':
            r = urllib.request.urlopen(self.url)
            if r.status != 200:
                raise Exception('Unable to load eclipse event: ' + iso + ' (URL: ' + self.url + ')')
            else:
                html = r.read().decode('utf-8','ignore')

        elif sys.version[0] is '2':
            page = requests.get(url)
            html = page.text.encode('ascii','ignore')
        
        self.loadFromRawHTML(html)

    def loadFromRawHTML(self, rawhtml):
        p1 = rawhtml.partition('<pre>');
        p2 = p1[2].partition('</pre>');
        html = p2[0].strip()
        if len(html) == 0:
            raise Exception('raw data string not found between <pre> tags')
        else:
            self.parseHTML(html)

    def parseHTML(self, html):
        allrows = html.split('\n')
        limits = 0
        for row in allrows:
            if 'Limits' in row:
                limits += 1
            elif limits == 1:
                row_stripped = row.strip()
                if len(row_stripped) > 0:
                    row_split = self.preparseHyphens(re.split('\s+',row_stripped))
                    self.parse_row(row_split)

    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def properties(self):
        return self._properties

    def data(self):
        d = {}
        for attr in self.properties:
            a = getattr(self, attr)
            if a is not None:
                d[attr] = a
        return d

    # Expand some single hyphens to two fields
    """ Sometimes a single hyphen will be used to denote a lack of a waypoint but this breaks the parsing
        when we expect each waypoint to be two values separated by whitespace. This function detects
        single hyphens that are placeholders for waypoints and replaces them with two spaced ?s.
        NOTE: Only waypoints apply - sometimes single hyphens are placeholders for other values and that
              alone doesn't break parsing. Hence we only check for hyphens between list indexes 0 and 6.
        This is incredibly hacky, but such is the nature of parsing quirky upstream data."""
    def preparseHyphens(self, row):
        try:
            while (row.index('-') > 0) and (row.index('-') < 6):
                index = row.index('-')
                row[index] = '?'
                row.insert(index+1, '?')
            return row
        except ValueError:
            return row

    # Generic function for converting points in degrees with cardinal direction numbers to floats
    def parseLatLon(self, v1, v2):
        try:
            val = float(v1) + (float(v2.rstrip('NESW'))/60)
            if v2.endswith('S') or v2.endswith('W'):
                val *= -1
            return round(val,3)
        except ValueError:
            return None

    # Parse an individual row, validate all values, store in data structures
    def parse_row(self, row):

        parsed_row = []

        # Ignore rows with ?s for anything (TODO: something better)
        try:
            if row.index('?'):
                return None
        except ValueError:
            pass
        
        def get(column, row):
            def func_not_found(row):
                return None
            func = getattr(self,column,func_not_found)
            return func(row)
        
        for column in self.columns:
            val = get(column, row)
            parsed_row.append(val)

        if (parsed_row[0] != None):
            self.time.append(parsed_row[0])

        if (parsed_row[1] != None) and (parsed_row[2] != None):
            self.position['north'].append((parsed_row[2], parsed_row[1]))
        
        if (parsed_row[3] != None) and (parsed_row[4] != None):
            self.position['south'].append((parsed_row[4], parsed_row[3]))

        if (parsed_row[5] != None) and (parsed_row[6] != None):        
            self.position['central'].append((parsed_row[6], parsed_row[5]))

        if (parsed_row[7] != None):
            self.ms_diam_ratio.append(parsed_row[7])

        if (parsed_row[8] != None):
            self.sun_altitude.append(parsed_row[8])

        if (parsed_row[9] != None):
            self.sun_azimuth.append(parsed_row[9])

        if (parsed_row[10] != None):
            self.path_width.append(parsed_row[10])

        if (parsed_row[11] != None):
            self.central_line_duration.append(parsed_row[11])

        return parsed_row

    # Functions to be called dynamically to extract individual values from the row
    def Time(self, row):
        return row[0]

    def NorthLimitLat(self, row):
        return self.parseLatLon(row[1],row[2])

    def NorthLimitLon(self, row):
        return self.parseLatLon(row[3],row[4])

    def SouthLimitLat(self, row):
        return self.parseLatLon(row[5],row[6])
    
    def SouthLimitLon(self, row):
        return self.parseLatLon(row[7],row[8])

    def CentralLat(self, row):
        return self.parseLatLon(row[9],row[10])

    def CentralLon(self, row):
        return self.parseLatLon(row[11],row[12])

    def MSDiamRatio(self, row):
        try:
            val = float(row[13])
            return val
        except ValueError:
            return None
        
    def SunAltitude(self, row):
        try:
            val = float(row[14])
            return val
        except ValueError:
            return None

    def SunAzimuth(self, row):
        try:
            val = float(row[15])
            return val
        except ValueError:
            return None

    def PathWidth(self, row):
        try:
            val = float(row[16])
            return val
        except ValueError:
            return None

    def CentralLineDuration(self, row):
        return row[17]


    def czml(self):

        doc = czml.CZML();
        iso = self.date.isoformat()

        # Generate time-specific lists for various objects
        north_polyline_degrees = []
        central_polyline_degrees = []
        south_polyline_degrees = []
        ellipse_position = []
        ellipse_semiMajorAxis = []
        ellipse_semiMinorAxis = []
        for t in range(len(self.time)):
            time = iso + "T" + self.time[t] + ":00Z"
            north_polyline_degrees += [self.position['north'][t][0], self.position['north'][t][1], 0.0]
            central_polyline_degrees += [self.position['central'][t][0], self.position['central'][t][1], 0.0]
            south_polyline_degrees += [self.position['south'][t][0], self.position['south'][t][1], 0.0]
            ellipse_position += [time, self.position['central'][t][0], self.position['central'][t][1], 0.0]
            ellipse_semiMajorAxis += [time, self.path_width[t]]
            ellipse_semiMinorAxis += [time, self.path_width[t]]

        # Generate document packet with clock
        start_time = iso + "T" + self.time[0] + ":00Z"
        end_time = iso + "T" + self.time[-1] + ":00Z"
        packet = czml.CZMLPacket(id='document',version='1.0')
        c = czml.Clock()
        c.multiplier = 300
        c.range = "LOOP_STOP"
        c.step = "SYSTEM_CLOCK_MULTIPLIER"
        c.currentTime = start_time
        c.interval = start_time + "/" + end_time
        packet.clock = c
        doc.packets.append(packet)

        # Generate north polyline packet
        packet_id = iso + '_north_polyline'
        packet = czml.CZMLPacket(id=packet_id)
        nsc = czml.SolidColor(color=czml.Color(rgba=(255, 255, 255, 128)))
        nmat = czml.Material(solidColor=nsc)
        npos = czml.Positions(cartographicDegrees=north_polyline_degrees)
        npl = czml.Polyline(show=True, width=1, followSurface=True, material=nmat, positions=npos)
        packet.polyline = npl
        doc.packets.append(packet)

        # Generate central polyline packet
        packet_id = iso + '_central_polyline'
        packet = czml.CZMLPacket(id=packet_id)
        cpg = czml.PolylineGlow(glowPower=0.25, color=czml.Color(rgba=(223, 150, 47, 128)))
        cmat = czml.Material(polylineGlow=cpg)
        cpos = czml.Positions(cartographicDegrees=central_polyline_degrees)
        cpl = czml.Polyline(show=True, width=5, followSurface=True, material=cmat, positions=cpos)
        packet.polyline = cpl
        doc.packets.append(packet)

        # Generate south polyline packet
        packet_id = iso + '_south_polyline'
        packet = czml.CZMLPacket(id=packet_id)
        ssc = czml.SolidColor(color=czml.Color(rgba=(255, 255, 255, 128)))
        smat = czml.Material(solidColor=ssc)
        spos = czml.Positions(cartographicDegrees=south_polyline_degrees)
        spl = czml.Polyline(show=True, width=1, followSurface=True, material=smat, positions=spos)
        packet.polyline = spl
        doc.packets.append(packet)

        # Generate ellipse shadow packet
        packet_id = iso + '_shadow_ellipse'
        packet = czml.CZMLPacket(id=packet_id)
        esc = czml.SolidColor(color=czml.Color(rgba=(0, 0, 0, 160)))
        emat = czml.Material(solidColor=esc)
        xmaj = czml.Number(ellipse_semiMajorAxis)
        xmin = czml.Number(ellipse_semiMinorAxis)
        ell = czml.Ellipse(show=True, fill=True, material=emat, semiMajorAxis=xmaj, semiMinorAxis=xmin)
        packet.ellipse = ell
        packet.position = czml.Position(cartographicDegrees=ellipse_position)
        doc.packets.append(packet)

        return list(doc.data())
