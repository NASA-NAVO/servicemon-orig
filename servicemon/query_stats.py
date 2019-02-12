import time
        
class Interval():
    """
    """
    def __init__(self, desc):
        self._desc = desc 
        self._start_time = time.time()
        self._end_time = self._start_time
        
    def close(self):
        self._end_time = time.time()
        return self

    @property
    def desc(self):
        return self._desc

    @property
    def duration(self):
        return self._end_time - self._start_time
    
class QueryStats():
    """
    """
    def __init__(self, name, query_type, access_url, query_params):
        self._start_time = time.time()
        self._name = name
        self._query_type = query_type
        self._access_url = access_url
        self._query_params = query_params
        self._intervals = []
        self._result_meta = {}
        
    def add_interval(self, interval):
        self._intervals.append(interval)
        
    # property result metadata
    @property
    def result_meta(self):
        return self._result_meta
    
    @result_meta.setter
    def result_meta(self, value):
        self._result_meta = value
        
    def _columns(self):
        cols = ['name', 'start_time', 'interval_desc', 'interval_dur']
        cols.extend(list(self._query_params.keys()))
        cols.extend(list(self._result_meta.keys()))
        return cols
    
    def _row_values(self):
        vals = []
        vals.append(self._name)
        vals.append(self._start_time)
        vals.append('{}')
        vals.append('{}')
        vals.extend(list(self._query_params.values()))
        vals.extend(list(self._result_meta.values()))
        return vals
    
    def header_string(self):
        hdr = ",".join(self._columns()) + '\n'
        return hdr
    
    def values_string(self):
        vals = ""
        for interval in self._intervals:
            row_str = ','.join(map(str, self._row_values()))
            row = row_str.format(interval.desc, interval.duration)
            vals += row + '\n'
        return vals

