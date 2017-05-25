import math

# approximated earth radius
earth_radius = 6371.01

# location of the city of Charny, near Quebec City, Quebec, Canada
lon = -71.269204
lat = 46.716993

# distance from the center to the sides of the box
distance = 2

MIN_LAT = math.radians(-90)
MAX_LAT = math.radians(90)
MIN_LON = math.radians(-180)
MAX_LON = math.radians(180)

# compute the angular distance
angular_distance = distance/earth_radius

# convert provided lat/lon to radius
lon_rad = math.radians(lon)
lat_rad = math.radians(lat)

# compute the min/max latitude - easy
min_lat = lat_rad - angular_distance
max_lat = lat_rad + angular_distance

# computing min/max longitude is trickier
# refer to http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates

if min_lat > MIN_LAT and max_lat < MAX_LAT:
      delta_lon = math.asin(math.sin(angular_distance) / math.cos(lat_rad))

      min_lon = lon_rad - delta_lon
      if min_lon < MIN_LON:
          min_lon += 2 * math.pi

      max_lon = lon_rad + delta_lon
      if max_lon > MAX_LON:
          max_lon -= 2 * math.pi

# a pole is within the distance
else:
      min_lat = max(min_lat, MIN_LAT)
      max_lat = min(max_lat, MAX_LAT)
      min_lon = MIN_LON
      max_lon = MAX_LON

min_lon_deg = math.degrees(min_lon)
min_lat_deg = math.degrees(min_lat)
max_lon_deg = math.degrees(max_lon)
max_lat_deg = math.degrees(max_lat)

print("%.6f,%.6f,%.6f,%.6f" % (min_lat_deg,min_lon_deg,max_lat_deg,max_lon_deg))
