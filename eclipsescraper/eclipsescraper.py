#!/usr/bin/python

import re
import urllib3
import json
from datetime import date

try:
    from czml import czml
except ImportError:
    import czml

def prep_raw_html(html):
    try:
        p1 = html.partition('<pre>');
        p2 = p1[2].partition('</pre>');
        rawdata = p2[0].strip()
        if len(rawdata) == 0:
            raise Exception('raw data string not found between <pre> tags')
        else:
            return rawdata
    except:
        raise Exception('Unable to extract raw data string from html')

class EclipseTrack:

    _properties = ('date', 'columns', 'vertexpositions')

    # Start by taking a raw data string and parsing it build the waypoints list
    def __init__(self, date, rawdata):

        self.date = date
        self.columns = [ 'Time','NorthLimitLat', 'NorthLimitLon', 'SouthLimitLat', 'SouthLimitLon', 'CentralLat', 'CentralLon',
                         'MSDiamRatio', 'SunAltitude', 'SunAzimuth', 'PathWidth', 'CentralLineDuration' ]
        self.vertexpositions = { 'north': [], 'south': [], 'central': [] }

        #allrows = rawdata.split('\r')
        allrows = rawdata.split('\n')
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
        
        def get(column, row):
            def func_not_found(row):
                return None
            func = getattr(self,column,func_not_found)
            return func(row)
        
        for column in self.columns:
            val = get(column, row)
            parsed_row.append(val)

        if (parsed_row[1] != None) and (parsed_row[2] != None):
            self.vertexpositions['north'].append(parsed_row[2])
            self.vertexpositions['north'].append(parsed_row[1])
            self.vertexpositions['north'].append(0.0)
        
        if (parsed_row[3] != None) and (parsed_row[4] != None):
            self.vertexpositions['south'].append(parsed_row[4])
            self.vertexpositions['south'].append(parsed_row[3])
            self.vertexpositions['south'].append(0.0)

        if (parsed_row[5] != None) and (parsed_row[6] != None):        
            self.vertexpositions['central'].append(parsed_row[6])
            self.vertexpositions['central'].append(parsed_row[5])
            self.vertexpositions['central'].append(0.0)

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

        # Generate clock
        packet_id = iso + '_clock'
        packet = czml.CZMLPacket(id=packet_id)
        c = czml.Clock()
        c.multiplier = 300
        c.range = "LOOP_STOP"
        c.step = "SYSTEM_CLOCK_MULTIPLIER"
        packet.clock = c
        doc.packets.append(packet)

        # Generate central polyline
        packet_id = iso + '_central_polyline'
        packet = czml.CZMLPacket(id=packet_id)
        cpg = czml.PolylineGlow(glowPower=0.25, color=czml.Color(rgba=(223, 150, 47, 128)))
        cmat = czml.Material(polylineGlow=cpg)
        cpos = czml.Positions(cartographicDegrees=self.vertexpositions['central'])
        cpl = czml.Polyline(show=True, width=5, followSurface=True, material=cmat, positions=cpos)
        packet.polyline = cpl
        doc.packets.append(packet)

        print "CZML DUMP:"
        print doc.dumps()
        return doc
