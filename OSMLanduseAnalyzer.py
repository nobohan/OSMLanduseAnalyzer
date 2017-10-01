from qgis.analysis import *

# work in progress !!!

# 0) PREPROCESSING

## Select the layers by name
landuse = QgsMapLayerRegistry.instance().mapLayersByName("osm_landusages")[0]
BEregion = QgsMapLayerRegistry.instance().mapLayersByName("BEregion")[0]
BEprovince = QgsMapLayerRegistry.instance().mapLayersByName("BEprovince")[0]

### Belgium area
#area_BE = 0
#for f in BEregion.getFeatures():
#    area_BE = area_BE + f['area']
#NB: should be 30,528 km
area_BE = 30528000000

# TODO 1.1) clip by country boundary (to remove out-of-country landuse)
#landuse_clip =
#from qgis.analysis import *
#overlayAnalyzer = QgsOverlayAnalyzer()
#overlayAnalyzer.intersection(layer1, layer2, "/home/julien/Desktop/output.shp")

# Select the landuse layer in QGIS toc and then run:
tot_area = 0
area_forest = 0
area_meadow = 0
area_residential = 0
area_farmland = 0

# MAIN LOOP
for f in landuse.getFeatures():
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



# 1) Landuse coverage

### For the country
print "Country coverage: " + str(tot_area/area_BE*100) + " %"

### By regions
# TODO: avoid overlapping landuse polygon
for region in BEregion.getFeatures(): # TODO: hwo to access polygon by polygon
    # clip by region shp
    region_area = 0
    ##landuse_clip = clip(landuse,region) # TODO: how to clip
    # select region in BEregion.
    overlayAnalyzer = QgsOverlayAnalyzer()
    overlayAnalyzer.intersection(landuse, BEregion, "./gis/temp.shp", onlySelectedFeatures = true)

    for f in landuse_clip.getFeatures():
        region_area = region_area + f['area']
        coverage = region_area/region['area']


# VL

# BXL

# WA


### By provinces
# for province,
# coverage = landuse_area / province_area

# 2) Landuse share
print area_forest/tot_area
print area_meadow/tot_area
print area_residential/tot_area
print area_farmland/tot_area
