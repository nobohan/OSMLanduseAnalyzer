### SHARE of landuse in CorineLandCover

## Select the layers by name
clc = QgsMapLayerRegistry.instance().mapLayersByName("clc_inter_provinces")[0]

area_meadow = 0
area_farmland = 0
area_orchard = 0

area_forest_bl = 0
area_forest_nl = 0
area_forest_ml = 0

area_urban = 0
area_water = 0
area_industrial = 0

area_total = 0

for f in clc.getFeatures():
  # sum all areas
  area_total = area_total + f['area_31370']

  # sum areas by type
  # forests
  if int(f['CODE_00'][0:2]) == 31 :
     # type of forest
     if int(f['CODE_00']) == 311:
         area_forest_bl = area_forest_bl + f['area_31370']
     if int(f['CODE_00']) == 312:
         area_forest_nl = area_forest_nl + f['area_31370']
     if int(f['CODE_00']) == 313:
         area_forest_ml = area_forest_ml + f['area_31370']

  # Agri areas
  if int(f['CODE_00']) == 231:
     area_meadow = area_meadow + f['area_31370']
  if int(f['CODE_00']) == 211 or int(f['CODE_00'][0]) == 212:
     area_farmland = area_farmland + f['area_31370']
  if int(f['CODE_00']) == 222:
     area_orchard = area_orchard + f['area_31370']

  # Urban areas
  if int(f['CODE_00'][0]) == 1:
      if int(f['CODE_00']) == 121:
          area_industrial = area_industrial + f['area_31370']
      else: #int(f['CODE_00'][0]) != 121
          area_urban = area_urban + f['area_31370']

  # Water areas
  if int(f['CODE_00']) == 511 or int(f['CODE_00']) == 512:
     area_water = area_water + f['area_31370']

# Sum of area for forest types
area_forest = area_forest_bl + area_forest_nl + area_forest_ml

# Sum of area for agricultural types
area_agricultural = area_meadow + area_farmland + area_orchard

# Sum of all areas
area_CLC = area_forest + area_agricultural + area_urban + area_water + area_industrial

# Landuse share results
print 'agri : ' + str(float(area_agricultural)/float(area_CLC))
print 'forest : ' + str(float(area_forest)/float(area_CLC))
print 'urban : ' + str(float(area_urban)/float(area_CLC))
print 'industrial: ' + str(float(area_industrial)/float(area_CLC))
print 'water : ' + str(float(area_water)/float(area_CLC))

# Type of forest
print 'broadleaved : ' + str(float(area_forest_bl)/float(area_forest))
print 'needleleaved : ' + str(float(area_forest_nl)/float(area_forest))
print 'mixedleaved : ' + str(float(area_forest_ml)/float(area_forest))

# Type of agricultural land
print 'farmland : ' + str(float(area_farmland)/float(area_agricultural))
print 'meadow : ' + str(float(area_meadow)/float(area_agricultural))
print 'orchard : ' + str(float(area_orchard)/float(area_agricultural))
