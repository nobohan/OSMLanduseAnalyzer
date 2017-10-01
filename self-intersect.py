from shapely.wkt import loads
from shapely.geometry import LineString
from shapely.ops import unary_union, polygonize

layer = iface.activeLayer()

polygons = [ feat.geometry().exportToWkt() for feat in layer.getFeatures() ]

shapely_polygons = [ loads(pol) for pol in polygons ]

rings = [ LineString(pol.exterior.coords) for pol in shapely_polygons ]

union = unary_union(rings)

new_intersections = [ geom.wkt for geom in polygonize(union) ]

epsg = layer.crs().postgisSrid()

uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"

mem_layer = QgsVectorLayer(uri,
                           'new_polygons',
                           'memory')

prov = mem_layer.dataProvider()

feats = [ QgsFeature() for i in range(len(new_intersections)) ]

for i, feat in enumerate(feats):
    feat.setAttributes([i])
    feat.setGeometry(QgsGeometry.fromWkt(new_intersections[i]))

prov.addFeatures(feats)

QgsMapLayerRegistry.instance().addMapLayer(mem_layer)




from qgis.core import *
from qgis.gui import *

canvas = qgis.utils.iface.mapCanvas()

layers = canvas.layers()
layer1 = canvas.layer(0)
layer2 = canvas.layer(3)

from qgis.analysis import *

overlayAnalyzer = QgsOverlayAnalyzer()
overlayAnalyzer.intersection(layer1, layer2, "/home/..../Scrivania/..../output.shp")

layer3 = canvas.layer(0)
