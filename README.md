# OSMLanduseAnalyzer


WORK/TODO

* Refine the custom mapping of landuse tags
* Do some geoprocessing
  * self-intersection: how is superimposed the landuse?

* Compute statistics
  * compute total landuse coverage at country / region / province levels
    * compute sum of area - sum of area where there is self intersection
      * see https://gis.stackexchange.com/questions/249934/get-intersections-of-polygons-in-same-layer-in-r-or-qgis
    * NB: there are superposition: see example in Rulles with meadow Sizaire
  * compute the share of landuse type
  * compute part of landuse=forest | natural=wood with leaf_type & leaf_cycle information
* render landuse in a webmap, or use OSMlanduse.org

# Custom mapping

See the `imposm-mapping.py` file for knowing the which OSM tags are considered as land-use in this analysis.

# Import OSM data using imposm

## Create a database

The instructions for creating the db are in create-db.sh.
Run the following in a terminal to create this db:

sudo su postgres
sh ./create-db.sh
exit
sudo service postgresql restart

## Import OSM data into the database
imposm --proj=EPSG:3857 --read belgium-latest.osm.bz2 -m imposm-mapping.py
imposm -U osm -d osmlanduse -m imposm-mapping.py --write --optimize --deploy-production-tables


imposm -d osmlanduse --remove-backup-tables



# Geoprocessing and indicators computation

TODO:
* clip by province

## Get some administrative boundaries for analysing the land-use

Overpass queries to export country, regions and provinces administrative levels:
```
[out:json][timeout:25];
{{geocodeArea:Belgium}}->.searchArea;
(
  relation["admin_level"="6"](area.searchArea);
);
out body;
>;
out skel qt;
```
with different admin_level for
* country: admin_level=2;
* regions: admin_level=4;
* provinces: admin_level=6.

After that, the layers were exported as geojson and saved as shp to be able to edit them. For unknown reason, the geojson was not editable in QGIS. Then, area of each features was computed. Some overlapping polygon (such as Province of Liège with and without the German community) were removed/clean.

## Geoprocessing
* manage self-intersection
* layer intersections

* sum the area of the fields: https://gis.stackexchange.com/questions/17180/how-to-sum-area-of-polygons-by-values-occuring-in-multiple-fields#17187

see also https://nyalldawson.net/tag/pyqgis/


pyqgis: compute area: https://gis.stackexchange.com/questions/180744/calculate-area-of-all-polygons-in-a-shapefile-and-save-it-in-attribute-column-a


TO DO (after some tests)

Intersection of the whole layer landusages with province, regions. Then, simply sum the area with filtering with right field
 * error: Input layer A contains invalid geometries (feature 889179). Unable to complete intersection algorithm.
