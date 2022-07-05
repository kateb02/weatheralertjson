import os
import shapefile
from shapely.geometry import Point, Polygon, MultiPolygon

#multiPolygon argument should be the relative path to whatever shapefile you want to use
#pointsToCheck should be a list of tuple points - eg [ (40, 20), (50, 10), ... ]
def isInMultiPolygon(multiPolygon, pointsToCheck):
    script_dir = os.path.dirname(__file__)
    polygon = shapefile.Reader(script_dir + multiPolygon)
    polygon = polygon.shapes()
    shpfilePoints = [shape.points for shape in polygon]

    polygons = shpfilePoints
    for polygon in polygons: #makes polygon of each set of points from the multiPolygon file
        poly = Polygon(polygon)
        for coordPair in pointsToCheck:
            point = Point(coordPair)
            if(poly.contains(point)):
                print("alert is in the multipolygon!")
                return True

    print("alert is NOT in the multipolygon")
    return False


