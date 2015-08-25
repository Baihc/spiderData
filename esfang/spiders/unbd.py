# coding=utf8
import math

class Offset(object):
    def __init__(self, dataFile=None):
        self._dataFile = dataFile if dataFile and os.path.exists(dataFile) else None
        self._const1 = self._get_const() if self._dataFile else None
        self._const2 = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22)
        self._x_pi = math.pi * 3000.0 / 180.0

    def unBdCoor(self, bdLon, bdLat):
        if self._outOfChina(bdLon, bdLat):
            return bdLon, bdLat
        x = bdLon - 0.0065
        y = bdLat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self._x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self._x_pi)
        gg_lon = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return gg_lon, gg_lat


    def _outOfChina(self, lon, lat):
        if (lon < 72.004 or lon > 137.8347):
            return True
        if (lat < 0.8293 or lat > 55.8271):
            return True
        return False

if __name__ == '__main__':
    test=Offset()
    rawX, rawY = 116.43859100341797,39.94440460205078
    unbdX, unbdY = test.unBdCoor(rawX, rawY)
    print unbdX, unbdY





