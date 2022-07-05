'''
##shpfilePoints is all the shapefile points for a map of the US states
##https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
# https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python
'''
import os
import json
from processGeoJson import isInMultiPolygon
from flask import Flask, request
from flattenList import flatten

app = Flask(__name__)

##yields all key-value pairs that contain KEY
def nested_dict_pairs_iterator(dict_obj, KEY):
    ''' This function accepts a nested dictionary as argument
        and iterate over all values of nested dictionaries
    '''
    # Iterate over all key-value pairs of dict argument
    #print("searching for key-value pairs with key: ", KEY)
    for key, value in dict_obj.items():
        # Check if value is of dict type
        print("key: ", key, "value: ", value)
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in  nested_dict_pairs_iterator(value, KEY):
                #print("key: ", key, " pair: ", pair)
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            #yield (key, value)
            if(key == KEY):
                print("key: ", key, " value: ", value)
                yield(key, value)
def returnCoordinates(data):
    ## nested_dict_pairs will:
    ## either will return (message, alert, geometry, coordinates, [45345, 345345] ...
    ## or (alert, geometry, coordinates, [45345, 345345] ...
    tupleWithCoordinates = ()
    for value in nested_dict_pairs_iterator(data, "coordinates"):
        #print("value: ", value)
        if(type(value) is tuple):
            tupleWithCoordinates = value
            print("TUPLE: ", tupleWithCoordinates)
            ##look for index of "coordinates" - pairs are after this
            indexOfFirstCoordinate = tupleWithCoordinates.index("coordinates") + 1 ##integer
            coordsOnly = tupleWithCoordinates[indexOfFirstCoordinate:]
            ## flatten coordinate list - unsure how deeply coordinate pairs are nested
            ## should return the coordinates in order in a list

            flattened = list ( flatten(coordsOnly) )## returns a generator item
            print("flattened LIST : ", flattened)
            coordinateListProcessed = []
            for x in range(0, len(flattened) - 1, 2):
                coordPair = [flattened[x], flattened[x + 1]]
                coordinateListProcessed.append(coordPair)

            #should be a list of coordinates in the form [ [a,b], [c, d] ...]
            return(coordinateListProcessed)


@app.route('/', methods=['POST'])
def index():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        POSTEDdata = json.loads(request.data, strict=False)
        # print(POSTEDdata)
        # for value in nested_dict_pairs_iterator(POSTEDdata, "coordinates"):
        #     print("value: ", value)
        # print(returnCoordinates(POSTEDdata))
        isInMultiPolygon(r"\cb_2018_us_state_500k.zip", returnCoordinates(POSTEDdata))

        return("200")
    else:
        return 'Content-Type not supported!'
        return ('', 200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


