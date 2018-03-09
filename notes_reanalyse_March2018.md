OSMLanduseAnalyzer
==================

Re-did the analysis in March 2018 with new OSM data


* download the latest pdf file for Belgium
* imposm --proj=EPSG:3857 --read belgium-latest.osm.pbf -m imposm-mapping.py --overwrite-cache
* imposm -U osm -d osmlanduse -m imposm-mapping.py --write --optimize --deploy-production-tables
  * pw is osm

Processing:

0) test the validity of geometries
```
SELECT ST_IsValid(geometry)
FROM osm_landusages_march18
```
1) Make the geometries valid

```
CREATE TABLE osm_landusages_march_valid AS
SELECT id, osm_id, name, type, leaf_type, leaf_cycle, ST_MakeValid(geometry) AS geometry
FROM osm_landusages_march18
```

2) Intersection avec l'outil intersection de QGIS et sauvegarde dans une table postgis:


3) Dissolution en PostGIS:
```
CREATE TABLE landuse_province_dissolve_byprovince AS
SELECT iso3166_2, ST_Multi(ST_Union(f.the_geom)) AS geometry
FROM landuse_provinces_byqgis AS f
GROUP BY iso3166_2
```

4) calcul de l'aire avec QGIS

Sans problème

NOTES
-----

Messages de is-valid:

messages: NOTICE:  Self-intersection at or near point 629357.01204243151 6591480.6965010129
NOTICE:  Ring Self-intersection at or near point 598945.25617033185 6637973.6856942885
NOTICE:  Self-intersection at or near point 569727.35237811971 6564575.0158073911
NOTICE:  Self-intersection at or near point 575471.71596778336 6565885.3980685975
NOTICE:  Ring Self-intersection at or near point 578695.35932867427 6640781.2400754746
NOTICE:  Self-intersection at or near point 420408.29546584265 6571901.2445839318
NOTICE:  Self-intersection at or near point 579841.81383557559 6564250.5576442936
NOTICE:  Self-intersection at or near point 622218.17850562371 6390116.1021769317
NOTICE:  Self-intersection at or near point 453948.57604773057 6616906.6327600377
NOTICE:  Self-intersection at or near point 423460.78695469099 6509526.0270944545
NOTICE:  Self-intersection at or near point 423460.78695469099 6509526.0270944545
NOTICE:  Self-intersection at or near point 372175.06810947764 6575299.5339062102
NOTICE:  Self-intersection at or near point 433441.63376695151 6520638.4368764944
NOTICE:  Self-intersection at or near point 437100.41158588743 6518706.2450562958
NOTICE:  Ring Self-intersection at or near point 422358.8415682675 6517428.7987086521
NOTICE:  Self-intersection at or near point 447902.3300908751 6523495.129323177
NOTICE:  Ring Self-intersection at or near point 602603.35394209321 6649417.368426973
NOTICE:  Ring Self-intersection at or near point 614123.62336505658 6616912.6393456571
NOTICE:  Ring Self-intersection at or near point 696840.11403125443 6549833.6410912424
NOTICE:  Self-intersection at or near point 666570.29504829587 6544681.561618642
NOTICE:  Self-intersection at or near point 661693.61065132613 6540688.0387520548
NOTICE:  Self-intersection at or near point 658382.83140714106 6563390.3441726044
NOTICE:  Self-intersection at or near point 546142.70021733758 6623215.3933578366
NOTICE:  Self-intersection at or near point 453253.8353861855 6581835.0543584898
NOTICE:  Self-intersection at or near point 480030.52356979653 6573986.0292540323
NOTICE:  Self-intersection at or near point 420658.69242755428 6603338.8654063689
NOTICE:  Self-intersection at or near point 412203.95201841305 6623650.0474668033
NOTICE:  Ring Self-intersection at or near point 422632.44544777612 6515702.3877813723
NOTICE:  Self-intersection at or near point 507337.00798399968 6635718.7930353675
NOTICE:  Self-intersection at or near point 461641.07904679183 6633968.1084848102
NOTICE:  Self-intersection at or near point 460135.33985450922 6547115.057719213
NOTICE:  Self-intersection at or near point 494904.85407367931 6540625.8697040789
NOTICE:  Self-intersection at or near point 475463.75814384432 6505254.259707856
NOTICE:  Ring Self-intersection at or near point 505123.61856520863 6545981.5770417834
NOTICE:  Ring Self-intersection at or near point 465056.72233405377 6629228.0979600418
NOTICE:  Self-intersection at or near point 321785.83983919345 6614894.0531416899
NOTICE:  Self-intersection at or near point 453948.57604773057 6616906.6327600377
NOTICE:  Ring Self-intersection at or near point 459093.25318399922 6631968.4050005767
Total query runtime: 46.5 secs
950648 rows retrieved.


Intersection with provinces
```
CREATE TABLE landuse_march_inter_provinces AS
SELECT osm_landusages_march_valid.id,
       beprovince3857_valid.name,
       beprovince3857_valid.iso3166_2,
       ST_COLLECT(ST_INTERSECTION(osm_landusages_march_valid.geometry, beprovince3857_valid.wkb_geometry)) AS geometry
FROM osm_landusages_march_valid, beprovince3857_valid
WHERE ST_Intersects(osm_landusages_march_valid.geometry, beprovince3857_valid.wkb_geometry)
GROUP BY osm_landusages_march_valid.id, beprovince3857_valid.name, beprovince3857_valid.iso3166_2;
```
IMPORTANT: pour pouvoir éditer la couche dans QGIS
ALTER TABLE osm_landusages_march_valid ADD PRIMARY KEY (id);

--> 2h30
Mais les multipolygons ne sont pas passés!


NB Extraction by bbox:

CREATE TABLE landuse_march_extract AS
SELECT *
FROM osm_landusages_march_valid
WHERE osm_landusages_march_valid.geometry && ST_Transform(ST_MakeEnvelope(5.33153,50.29012, 5.6634,50.4636, 4326),3857);
