# Geo-coding test #

Here are some coding test examples.

1. Bounding Box definition
2. Canada Cities test
3. Parking slots in Quebec City test

## Bounding Box Definition ##

A Bounding box is a square centered around a geolocated point with a specific side width. When you specify a point and a distance, the resulting bounding box will have a side of twice the distance. You can think it as a box that contains a circle having a radius of the provided distance.

![Bounding Box](https://github.com/prune998/codingtest/raw/master/boundingbox/data/aplikate_eu_bbox_.png)

Check OSM Wiki for more info : http://wiki.openstreetmap.org/wiki/Bounding_Box

To calculate the bounding box, earth radius can be approximate to 6371.01 kilometers.
Then you can approximate the angular distance in radians on a great circle to be : angular_distance = <distance> / <earth radius>

We can approximate the coordinates as if we were on a perfect cartesian sphere, then compute the bottom-left and top-right points of the box. Please refer to http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates for more informations.

Note that you can test your result on the website http://aplikate.eu/bbox/ by providing a string with your coordinates as `<min_lat>,<min_lon>,<max_lat>,<max_lon>` (ex : 46.699007,-71.295438,46.734979,-71.242970)

You can test using the Python example `bounding_box_example.py`

## Canada Cities ##

This coding test requires to :

- open a Geo JSON file located at `data/canada_cities.geojson`
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

- create a HTTPS REST API on port 8443
  - have two API enpoint returning a valid json document and responding to :
      - a GET request `/id/<12345>` where <12345> is the cartodb_id
      it should return a JSON document including the `cartodb_id` requested, the `name`, the `polulation` and the point `coordinates` :
      ex :
      ```
      curl -ks https://localhost:8443/id/744

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
      curl -ks https://localhost:8443/id/744?dist=10

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


## Parking slots in Quebec City (not yet ready) ##
This coding test requires to :

- open a Geo JSON file located at `data/PARCOMETRE.GEOJSON`
  Json file is structured as :
  ```
  Nom	Description	Type
  ID	Identifiant de la borne de stationnement.	Entier
  COTE_RUE	Coté par rapport au centre de chaussée où est le panneau de stationnement.	Réel
  LECT_MET	Distance mesurée à partir du début du tronçon dans le sens des numéros d'immeuble.	Réel
  DIRECTION	Coté du centre de chaussée ou de l'intersection dans le cas d'un terre-plein.	Texte
  SEGMENT_RU	Identifiant du segment de voie publique.	Réel
  NOM_TOPOG	Nom topographique (générique, liaison, spécifique, direction) du centre de chaussée.	Texte
  NO_BORNE	Numéro de la borne de stationnement.	Texte
  NO_CIVIQ	Numéro civique où la borne de stationnement est située.	Réel
  ID_VOIE_PUB	Identifiant de la voie publique sur laquelle la borne de stationnement est située.	Réel
  GEOM	Longitude et latitude de la borne de stationnement selon le standard WKT (Well-known text).	Texte
  ```

  GEOM will not be used. Use the `Point coordinate` instead.

- create a HTTPS REST API on port 8443
- have two API enpoint returning a valid json document like :
  - a GET request `/id/<12345>` where <12345> is the NO_BORNE
    it should return a JSON document including the NO_CIVIQ and NOM_TOPOG of the selected location
    ex :
    ```
    curl -ks https://localhost:8443/id/2069
    {ID: 2069,
     ADDRESS: "555 Rue Saint-Jean",
     "COORDINATE":[-71.2203932633083,46.809783445691]
    }
    ```
	- a range search like GET /id/<1234>?dist=200 where :
		- where <12345> is the NO_BORNE
    - dist is the length of the side of a square bounding box around the selected ID in `meters`

    ex :
    ```
    curl -ks https://localhost:8443/id/2069?dist=200

    [
      {ID: 2069,
       ADDRESS: "555 Rue Saint-Jean",
       "COORDINATE":[-71.2203932633083,46.809783445691]
      },
      {ID: 2066,
       ADDRESS: "537 Rue Saint-Jean",
       "COORDINATE":[-71.2206433390378,46.8096776479961]
      },
      ...
    ]

    ```
