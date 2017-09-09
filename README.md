# OSMLanduseAnalyzer


WORK/TODO

* Define the custom mapping of landuse tags
* Import data using imposm and the custom mapping
* Access db in QGIS
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



* sum the area of the fields: https://gis.stackexchange.com/questions/17180/how-to-sum-area-of-polygons-by-values-occuring-in-multiple-fields#17187

With pyqgis:

# Select the layer in QGIS toc and then run:
layer = iface.activeLayer()

tot_area = 0
area_forest = 0
area_meadow = 0
area_residential = 0
area_farmland = 0

for f in layer.getFeatures():
  # sum all areas
  tot_area = tot_area + f['area']
  # sum forested areas
  if f['type'] == "forest":
     area_forest = area_forest + f['area']
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']
  if f['type'] == "residential":
     area_residential = area_residential + f['area']
  if f['type'] == "farmland":
     area_farmland = area_farmland + f['area']

print area_forest/tot_area
print area_meadow/tot_area
print area_residential/tot_area
print area_farmland/tot_area
