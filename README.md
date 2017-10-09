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

# 1) Pre-processing
## Custom mapping

See the `imposm-mapping.py` file for knowing the which OSM tags are considered as land-use in this analysis.

## Import OSM data using imposm

### Create a database

The instructions for creating the db are in create-db.sh.
Run the following in a terminal to create this db:

sudo su postgres
sh ./create-db.sh
exit
sudo service postgresql restart

### Import OSM data into the database
imposm --proj=EPSG:3857 --read belgium-latest.osm.bz2 -m imposm-mapping.py
imposm -U osm -d osmlanduse -m imposm-mapping.py --write --optimize --deploy-production-tables


imposm -d osmlanduse --remove-backup-tables


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

## 2) Geoprocessing

### 1) Prepare the layers
#### Make an intersection of the layer
Intersection of the whole layer landusages with province, regions. Then, simply sum the area with filtering with right field
 * error: Input layer osm_landusages contains invalid geometries (feature 889179). Unable to complete intersection algorithm.

--> This feature was a footway of about 2000 m². I've deleted it.

Intersection works. It took about one night of processing.

TODO: intersection by provinces

#### Make a dissolve layer (for computing coverage)
TODO
#### Recompute polygon areas
for both the dissolved and the intersect layers
TODO

# 2) Total coverage

Run the script OSMLanduseAnalyzer_byregions.py

# 3) Share of land-use

TODO: script OSMLanduseAnalyzer_share_byregions.py
