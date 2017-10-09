### SHARE of landuse

# work in progress !!!

## Select the layers by name
### Use the intersect layer to get rid of polygons outside Belgium
landuse = QgsMapLayerRegistry.instance().mapLayersByName("osm_landusages_inter_BEregion")[0]

# Select the landuse layer in QGIS toc and then run:
area_total = 0
area_forest = 0
area_meadow = 0
area_residential = 0
area_farmland = 0

for f in landuse.getFeatures():
  # sum all areas
  tot_area = tot_area + f['area']
  # sum areas by type
  if f['type'] == "forest":
     area_forest = area_forest + f['area']
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']
  if f['type'] == "residential":
     area_residential = area_residential + f['area']
  if f['type'] == "farmland":
     area_farmland = area_farmland + f['area']

# Landuse share results
print area_forest/tot_area
print area_meadow/tot_area
print area_residential/tot_area
print area_farmland/tot_area
