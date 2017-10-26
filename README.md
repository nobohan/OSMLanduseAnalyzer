# OSMLanduseAnalyzer

This small repository is about computing some basic statistics about OpenStreetMap (OSM) land-use coverage and share over a given region/country. This was made for Belgium, in the framework of a presentation at the FOSS4G.be conference, held in October 2017 in Brussels. The output are (1) the regional coverage of "land-use" features in OSM, namely the percentage of land-use area compared to total area and (2) the share of the land-use in different categories (e.g., farmland, residential, forest, ...)

! This repository is definitely not a push-button solution. I'm probably far the from the smartest solution for computing these basic stats but it worked for me. Note that the basic GIS operations involved in this project (intersection, dissolve, etc.) can be particularly tricky when dealing with OSM data because of the presence of topological errors and the large size of the layer (huge number of geometries implying a huge processing time).

Author: Julien Minet, juminet@gmail.com

# 1) Pre-processing

## 1.1) Import OSM land-use data using imposm

### Create a database
The instructions for creating the db are in create-db.sh.
Run the following in a terminal to create this db:

`sudo su postgres`
`sh ./create-db.sh`
`exit`
`sudo service postgresql restart`

### Custom mapping
OSM land-use data were imported into a postgresql database using `imposm` with a custom mapping of the tags. See the `imposm-mapping.py` file for knowing which OSM tags are considered as "land-use" in this analysis. This mapping was inspired from OSMBright. See also OSMlanduse.org for another mapping.

### Import OSM data into the database
`imposm --proj=EPSG:3857 --read belgium-latest.osm.bz2 -m imposm-mapping.py`
`imposm -U osm -d osmlanduse -m imposm-mapping.py --write --optimize --deploy-production-tables`

### To remove existing backup data
`imposm -d osmlanduse --remove-backup-tables`


## 1.2) Get some administrative boundaries for analysing the land-use
### Overpass queries to get the boundary data
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

After that, the layers were exported as geojson and saved as shp to be able to edit them. For unknown reason, the geojson was not editable in QGIS. Then, area of each features was computed. Some overlapping polygons (such as Province of Liège with and without the German community) were removed/clean.

### Import these layers in postgresql
`ogr2ogr -f PostgreSQL PG:"dbname=osmlanduse user=osm password=osm host=localhost" -nlt POLYGON -a_srs EPSG:3857 BEprovince3857.shp`


# 2) Geoprocessing
## 2.1) Make an intersection of the layer
Intersection of the whole layer osm_landusages with province, regions. Can be done using the QGIS Intersect tool or a PostGIS query (see `PostGIS.sql` for examples)

## 2.2) Make a dissolve layer (for computing coverage)
Dissolve the osm_landusages_inter_province layer by the province field.

## 2.3) Recompute polygon areas
Compute the area of the dissolved layer for computing the coverage

# 3) Land-use statistics
## 3.1) Compute total coverage
See the area of the dissolved layer and compare to the reference intersect layer area.

## 3.2) Share of land-use
Run the script OSMLanduseAnalyzer_share.py
