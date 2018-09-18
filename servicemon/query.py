from astropy.coordinates import SkyCoord
import astropy.io.fits as fits
import astropy.units as u
from astropy.table import Table

from servicemon.navoutils.cone import Cone


def get_data():
    """Placeholder.  Do a quick cone search of CSC """
    access_url = 'http://cda.harvard.edu/cscvo/coneSearch?'
    position = SkyCoord(125.886, 21.3377, unit='deg')
    search_radius = 0.1
    result_list = Cone.query(service=access_url, coords=position,
                             radius=search_radius)

    return result_list
