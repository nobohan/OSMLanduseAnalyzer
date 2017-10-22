### SHARE of landuse

## Select the layers by name
### Use the intersect layer to get rid of polygons outside Belgium
landuse = QgsMapLayerRegistry.instance().mapLayersByName("osm_landusages2")[0]

# Select the landuse layer in QGIS toc and then run:
area_total = 0
area_forest = 0
area_meadow = 0
area_residential = 0

area_farm = 0
area_farmland = 0
area_farmyard = 0
area_orchard = 0

area_forest_bl = 0
area_forest_nl = 0
area_forest_ml = 0
area_forest_dec = 0
area_forest_eve = 0
area_forest_mc = 0
area_forest_no_type = 0

area_urban = 0
area_water = 0

for f in landuse.getFeatures():
  # sum all areas
  area_total = area_total + f['area']
  # sum areas by type
  if f['type'] == "forest" or f['type'] == "wood":
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
  # Agri areas
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']
  if f['type'] == "farm":
     area_farm = area_farm + f['area']
  if f['type'] == "farmland":
     area_farmland = area_farmland + f['area']
  if f['type'] == "farmyard":
     area_farmyard = area_farmyard + f['area']
  if f['type'] == "orchard":
     area_orchard = area_orchard + f['area']
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']

  # Urban areas TODO: complete...
  if f['type'] == "residential":
     area_urban = area_urban + f['area']

  # Water areas
  if f['type'] == "water":
     area_water = area_water + f['area']

area_agricultural = area_farm + area_farmland + area_farmyard + area_orchard + area_meadow


# Landuse share results
print 'forest : ' + str(area_forest/area_total)
print 'urban : ' + str(area_urban/area_total)
print 'agri : ' + str(area_agricultural/area_total)

# Type of forest
print 'broadleaved : ' + str(area_forest_bl/area_forest)
print 'needleleaved : ' + str(area_forest_nl/area_forest)
print 'mixedleaved : ' + str(area_forest_ml/area_forest)
print 'deciduous : ' + str(area_forest_dec/area_forest)
print 'evergreen : ' + str(area_forest_eve/area_forest)
print 'mixedcycle : ' + str(area_forest_mc/area_forest)
print 'no forest type :' + str(area_forest_no_type/area_forest)

# Type of agricultural land
print 'farm : ' + str(area_farm/area_agricultural)
print 'farmland : ' + str(area_farmland/area_agricultural)
print 'farmyard : ' + str(area_farmyard/area_agricultural)
print 'meadow : ' + str(area_meadow/area_agricultural)
print 'orchard : ' + str(area_orchard/area_agricultural)
