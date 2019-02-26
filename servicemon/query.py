from astropy.coordinates import SkyCoord
from astropy.table import Table
from astroquery.utils import parse_coordinates

import warnings

import html
import requests
import os
import sys
import pathlib

from query_stats import Interval, QueryStats

def time_this(interval_name):
    def time_this_decorator(func):
        def wrapper(*args, **kwargs):
            interval = Interval(interval_name)
            result = func(*args, **kwargs)
            interval.close()
            args[0].stats.add_interval(interval)
            
            return result
        return wrapper
    return time_this_decorator

class Query():
    """
    """

    def __init__(self, base_name, query_type, service, coords, radius, out_dir, verbose=False):
        self._base_name = base_name
        self._query_type = query_type
        self._orig_service = service
        self._orig_coords = coords
        self._orig_radius = radius
        self._out_path = pathlib.Path(out_dir)
        self._verbose = verbose
        
        self._access_url = self._compute_access_url(service)
        self._coords = self._compute_coords(coords)
        
        self._query_params = self._compute_query_params()
        self._query_name = self._compute_query_name()
        self._filename = self._out_path / (self._query_name + '.xml')
        
        self._stats = QueryStats(self._query_name, self._base_name, 'cone', 
                                 self._access_url, self._query_params)
    
    @property 
    def stats(self):
        return self._stats
    
    def run(self):
        response = self.do_query()
        self.stream_to_file(response)
        self.gather_response_metadata(response)
    
    @time_this('do_query')
    def do_query(self):
        response = requests.get(self._access_url, self._query_params, stream=True)
        return response
    
    @time_this('stream_to_file')
    def stream_to_file(self, response):
        with open(self._filename, 'wb+') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)   
                
    def gather_response_metadata(self, response):
        result_meta = {
            'status': response.status_code,
            'size': -1,
            'num_rows': -1,
            'num_columns': -1
        }
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                t = Table.read(self._filename, format='votable')
                
            result_meta['size'] = os.path.getsize(self._filename)
            result_meta['num_rows'] = len(t)
            result_meta['num_columns'] = len(t.columns)
        except Exception as e:
            print(value=f'Error reading result table: {e}', file=sys.stderr, flush=True)
        finally:
            self._stats.result_meta = result_meta        
    
    def _compute_access_url(self, service):
        # Get the base URL from service, which might be a url string or a 
        # dictionary with an "access_url" key.
        if type(service) is str:
            access_url = service
        else:
            access_url = html.unescape(service['access_url'])
        if (access_url is None):
            raise ValueError("access_url is None")
        
        return access_url
    
    def _compute_coords(self, in_coords):
        # Get the RA and Dec from in_coords.
        coords = in_coords
        if (type(in_coords) is tuple or type(in_coords) is list) and len(in_coords) == 2:
            coords = parse_coordinates(f"{in_coords[0]} {in_coords[1]}")
        elif type(in_coords) is str:
            coords = parse_coordinates(in_coords)
        elif type(in_coords) is not SkyCoord:
            raise ValueError(f"Cannot parse input coordinates {in_coords}")  
        
        return coords
    
    def _compute_query_params(self):
        params = {
            'RA': self._coords.ra.deg,
            'DEC': self._coords.dec.deg,
            'SR': self._orig_radius
        }
        return params
    
    def _compute_query_name(self):
        name = (f'{self._base_name}_{self._query_type}' + 
                f'_{str(self._query_params["RA"])}' +
                f'_{str(self._query_params["DEC"])}' +
                f'_{str(self._query_params["SR"])}')
        return name




        
        
