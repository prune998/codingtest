# Geo-coding test #

Here are some coding test examples.

1. Bounding Box definition
2. Canada Cities test

## Bounding Box Definition ##

A Bounding box is a square centered around a geolocated point with a specific side width. When you specify a point and a distance, the resulting bounding box will have a side of twice the distance. You can think it as a box that contains a circle having a radius of the provided distance.

![Bounding Box](http://github.com/prune998/codingtest/raw/master/boundingbox/data/aplikate_eu_bbox_.png)

Check OSM Wiki for more info : http://wiki.openstreetmap.org/wiki/Bounding_Box

To calculate the bounding box, earth radius can be approximate to 6371.01 kilometers.
Then you can approximate the angular distance in radians on a great circle to be : angular_distance = <distance> / <earth radius>

We can approximate the coordinates as if we were on a perfect cartesian sphere, then compute the bottom-left and top-right points of the box. Please refer to http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates for more informations.

Note that you can test your result on the website http://aplikate.eu/bbox/ by providing a string with your coordinates as `<min_lat>,<min_lon>,<max_lat>,<max_lon>` (ex : 46.699007,-71.295438,46.734979,-71.242970)

You can test using the Python example `bounding_box_example.py`

## Canada Cities ##

This coding test requires to :

- You have to implement your own data structure to hold the data from the Geo JSON file located at `data/canada_cities.geojson`. Do not reload the data file on every request.

  The file is a GeoJson file compliant with the format described at http://geojson.org/
  It is structured as :

  ```
  {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -80.643498,
          43.069946
        ]
      },
      "properties": {
        "name": "Oriel",
        "place_key": "3500002520",
        "capital": "N",
        "population": 2500,
        "pclass": "2",
        "cartodb_id": 744,
        "created_at": "2015-04-02T23:52:39Z",
        "updated_at": "2015-04-02T23:52:39Z"
      }
    },
    { another feature (city)... }
    ]
  }
    ```
    Each city is represented by a `Point` (not a shape). Coordinates are described as `longitude` and `latitude` (or easting and northing)

- create a HTTP REST API on port 8000
  - have two API enpoint returning a valid json document and responding to :
      - a GET request `/id/<12345>` where <12345> is the cartodb_id
      it should return a JSON document including the `cartodb_id` requested, the `name`, the `polulation` and the point `coordinates` :
      ex :
      ```
      curl -ks http://localhost:8000/id/744

      {"cartodb_id": 744,
       "name": "oriel",
       "population": 2500,
       "coordinates": [-80.643498,43.069946]
      }
      ```

      - a GET request `/id/<12345>?dist=10` where <12345> is a `city ID` and `dist` is the side of a square centered around the city  (definig a bounding box) expressed in Kilometers.

      It should return a json document containing a list of all the cities inside the bounding box.
      ex :
      ```
      curl -ks http://localhost:8000/id/744?dist=10

      [
      {"cartodb_id": 544,
       "name": "Domaine-Pacha",
       "population": 29500,
       "coordinates": [-80.643497,43.069947]
      },
      {"cartodb_id": 998,
       "name": "Rhodena",
       "population": 210,
       "coordinates": [-80.643478,43.069947]
      },
      ...
      ]
      ```
      Note that the example is using random data, not the real expected result.


### Testing ###
#### City data #####
Try to get information for city number 744 :

```
curl -ks http://localhost:8000/id/744

{
  "city": {
    "cartodb_id": 744,
    "coordinates": [
      -80.643498,
      43.069946
    ],
    "name": "Oriel",
    "population": 2500
  }
}
```

#### Closest cities ####
Find all the cities that are 4 kilometers away from Oriel (city number 744) :

```
curl -ks http://localhost:8000/id/744?dist=4
{
  "cities": {
    "737": {
      "cartodb_id": 737,
      "coordinates": [
        -80.598719,
        43.064133
      ],
      "name": "Beaconsfield",
      "population": 2500
    },
    "776": {
      "cartodb_id": 776,
      "coordinates": [
        -80.682714,
        43.098307
      ],
      "name": "Oxford Centre",
      "population": 109
    },
    "778": {
      "cartodb_id": 778,
      "coordinates": [
        -80.62027,
        43.099452
      ],
      "name": "Vandecar",
      "population": 2500
    }
  }
}
```
