# PostGIS statement

### 1) indexer
# on extract:
CREATE INDEX osm_landusages_extract_gix ON landuse_extract USING GIST (geometry);
--> 62 ms

# on whole BE
CREATE INDEX osm_landusages_gix ON osm_landusages USING GIST (geometry);

### 2) intersection
# on extract:
CREATE TABLE landuse_inter_provinces_extract As
SELECT landuse_extract.id,
       ST_COLLECT(ST_INTERSECTION(landuse_extract.geometry, beprovince3857.geometry))
FROM landuse_extract, beprovince3857
WHERE ST_Intersects(landuse_extract.geometry, beprovince3857.geometry)
GROUP BY landuse_extract.id;

#on whole belgium:
CREATE TABLE landuse_inter_provinces As
SELECT osm_landusages.id,
       ST_COLLECT(ST_INTERSECTION(osm_landusages.geometry, beprovince3857.geometry))
FROM osm_landusages, BE_provinces
WHERE ST_Intersects(osm_landusages.geometry, beprovince3857.geometry)
GROUP BY osm_landusages.id;
--> did not work because of invalid geometry combination

### 3) Aggregate using ST_union - works
# on extract:
CREATE TABLE landuse_extract_dissolve_bytype AS
  SELECT type,
  	   ST_Multi(ST_Union(f.geometry)) as singlegeom
  	 FROM landuse_extract As f
GROUP BY type
--> 4.4 seconds
--> 4.3 | 4.4 seconds after gist indexing --> no improvements. NB: there exist already an index on osm_landusages
# NB: imposm --optimize already make a spatial index of the db

# on whole Belgium
CREATE TABLE landuse_dissolve_bytype AS
  SELECT type,
  	   ST_Multi(ST_Union(f.geometry)) as singlegeom
  	 FROM osm_landusages As f
GROUP BY type
--> several hours (exact time unknown)

## Aggregate to dissolve all - works!
CREATE TABLE landuse_dissolve AS
SELECT ST_Multi(ST_Union(f.geometry)) as singlegeom
	 FROM osm_landusages As f

##
osm_landusages_inter_beprovince was imported from the shp

CREATE TABLE landuse_inter_province_valid AS
SELECT iso3166_2, ST_MakeValid(wkb_geometry) As wkb_geometry
FROM osm_landusages_inter_beprovince
--> 1 min

CREATE TABLE landuse_inter_province_dissolve_byprovince AS
  SELECT iso3166_2,
      ST_Multi(ST_Union(f.wkb_geometry)) as singlegeom
    FROM landuse_inter_province_valid As f
GROUP BY iso3166_2
--> 1h29

NB:
ALTER TABLE BEprovince3857
ALTER COLUMN geom TYPE geometry(MULTIPOLYGON, 3857) USING ST_Transform(ST_SetSRID(geom,4326),3857) ;


error:

ERROR: GEOSUnaryUnion: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 522661.83904841624 6600379.0647823587 at 522661.83904841624 6600379.0647823587
SQL state: XX000

ERROR: GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 594265.89550528105 6606642.5881665461 at 594265.89550528105 6606642.5881665461
SQL state: XX000

ERROR: GEOSUnaryUnion: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 558539.77712105727 6632612.6987627409 at 558539.77712105727 6632612.6987627409
SQL state: XX000

ERROR: GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 572745.59696506651 6634358.0706200358 at 572745.59696506651 6634358.0706200358
SQL state: XX000


ERROR: GEOSUnaryUnion: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 463960.72992908116 6635048.4729057383 at 463960.72992908116 6635048.4729057383
SQL state: XX000


### IS valid:

ST_IsValid

SELECT NOT ST_IsValid(geometry) As bad_geom
FROM osm_landusages

Result:

NOTICE:  Ring Self-intersection at or near point 459154.7144517508 6509223.2543890607: ok
NOTICE:  Self-intersection at or near point 394494.20436404506 6621375.8237991007:ok
NOTICE:  Self-intersection at or near point 394494.20436404506 6621375.8237991007
NOTICE:  Ring Self-intersection at or near point 593300.57944081305 6609353.3047788553 ok
NOTICE:  Self-intersection at or near point 560367.6036862944 6632798.4230890479 ok
NOTICE:  Self-intersection at or near point 562358.64271479787 6626954.0655324357 ok
NOTICE:  Ring Self-intersection at or near point 595708.09390368022 6506606.1798645565 ok
NOTICE:  Ring Self-intersection at or near point 421989.13156186626 6521580.0473698834 ok
NOTICE:  Ring Self-intersection at or near point 585313.42317118717 6502937.2390079098 ok
NOTICE:  Self-intersection at or near point 359895.72809182375 6628641.1144105941 ok
NOTICE:  Self-intersection at or near point 463960.72992908116 6635048.4729057383 ok
NOTICE:  Self-intersection at or near point 462556.7033913756 6634038.5143437367




### Aggregate using ST_collect:
CREATE TABLE landuse_extract_dissolve_bycollect AS
SELECT type, ST_Collect(f.geometry) as singlegeom
	 FROM (SELECT type, (ST_Dump(geometry)).geom As geometry
				FROM
				landuse_extract ) As f
GROUP BY type

--> même résultat


## Make an extract of the layer
CREATE TABLE landuse_extract AS
  SELECT *
FROM osm_landusages
WHERE osm_landusages.geometry && ST_MakeEnvelope(569958,6400011, 637651,6451643, 3857);


WHERE osm_landusages.geometry && ST_MakeEnvelope(5.2, 49.7, 5.4, 50, 4326);


## Errors when running ST_Union
  ERROR:  GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 670749.43891915039 6484396.2533811396 at 670749.43891915039 6484396.2533811396
  ********** Error **********

  ERROR: GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 670749.43891915039 6484396.2533811396 at 670749.43891915039 6484396.2533811396
  SQL state: XX000

  --> Corrected

  ERROR:  GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 475463.75814384432 6505254.259707856 at 475463.75814384432 6505254.259707856
  ********** Error **********

  ERROR: GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 475463.75814384432 6505254.259707856 at 475463.75814384432 6505254.259707856
  SQL state: XX000

ERROR: GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 464652.71621046885 6512849.5294554401 at 464652.71621046885 6512849.5294554401
SQL state: XX000

ERROR: GEOSUnaryUnion: TopologyException: Input geom 1 is invalid: Self-intersection at or near point 437100.41158588743 6518706.2450562958 at 437100.41158588743 6518706.2450562958
SQL state: XX000

ERROR: GEOSUnaryUnion: TopologyException: Input geom 0 is invalid: Self-intersection at or near point 421953.18973654561 6521580.9262668965 at 421953.18973654561 6521580.9262668965
SQL state: XX000


### ST_UnaryUnion:
  CREATE TABLE landuse_extract_dissolve_bystunaryunion AS
    SELECT ST_UnaryUnion(geometry) AS geometry
    FROM landuse_extract
