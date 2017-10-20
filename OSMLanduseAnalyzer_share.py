### SHARE of landuse

## Select the layers by name
### Use the intersect layer to get rid of polygons outside Belgium
landuse = QgsMapLayerRegistry.instance().mapLayersByName("osm_landusages")[0]

# Select the landuse layer in QGIS toc and then run:
area_total = 0
area_forest = 0
area_meadow = 0
area_residential = 0
area_farmland = 0
area_forest_bl = 0
area_forest_nl = 0
area_forest_ml = 0
area_forest_dec = 0
area_forest_eve = 0
area_forest_mc = 0
area_forest_no_type = 0

for f in landuse.getFeatures():
  # sum all areas
  area_total = area_total + f['area']
  # sum areas by type
  if f['type'] == "forest":
     area_forest = area_forest + f['area']
     # type of forest
     if f['leaf_type'] == "broadleaved":
         area_forest_bl = area_forest_bl + f['area']
     if f['leaf_type'] == "needleleaved":
         area_forest_nl = area_forest_nl + f['area']
     if f['leaf_type'] == "mixed":
         area_forest_ml = area_forest_ml + f['area']
     if f['leaf_cycle'] == "deciduous":
         area_forest_dec = area_forest_dec + f['area']
     if f['leaf_cycle'] == "evergreen":
         area_forest_eve = area_forest_eve + f['area']
     if f['leaf_cycle'] == "mixed":
         area_forest_mc = area_forest_mc + f['area']
     if f['leaf_type'] == NULL and f['leaf_cycle'] == NULL:
         area_forest_no_type = area_forest_no_type + f['area']

  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']
  if f['type'] == "residential":
     area_residential = area_residential + f['area']
  if f['type'] == "farmland" or f['type'] == 'meadow':
     area_farmland = area_farmland + f['area']


# Share of meadow/farm/farmland in farmland?

# Landuse share results
print area_forest/area_total
print area_meadow/area_total
print area_residential/area_total
print area_farmland/area_total

# Type of forest
print 'broadleaved : ' + str(area_forest_bl/area_forest)
print 'needleleaved : ' + str(area_forest_nl/area_forest)
print 'mixedleaved : ' + str(area_forest_ml/area_forest)
print 'deciduous : ' + str(area_forest_dec/area_forest)
print 'evergreen : ' + str(area_forest_eve/area_forest)
print 'mixedcycle : ' + str(area_forest_mc/area_forest)
print 'no forest type :' + str(area_forest_no_type/area_forest)
