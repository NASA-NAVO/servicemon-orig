from astropy.coordinates import SkyCoord

import sys

from query import Query
       
def print_stats(stats):
    # print stats
    if len(stats) > 0:
        stat_string = ''
        stat_string += stats[0].header_string()
        for stat_instance in stats:
            stat_string += stat_instance.values_string()
        print(stat_string)
    else:
        print('No stats collected.')
    
services = [
    {'base_name': 'CSC', 
     'service_type': 'cone', 
     'access_url': 'http://cda.harvard.edu/cscvo/coneSearch?'
     }
]
    
cones = [
    ((125.886, 21.3377), 0.1),
    ((125.886, 21.3377), 0.5),
    ((125.7, 21.5), 0.1),
    ((125.7, 21.5), 0.5)
]
        
def do_queries():
    stats = []
    
    for service in services:
        for cone in cones:
            try:
                query = Query(service['base_name'], service['service_type'], 
                              service, cone[0], cone[1], 'results')
                query.run()
            except Exception as e:
                print(f'Error reading result table: {e}', file=sys.stderr, flush=True)
            else:
                stats.append(query.stats)
        
    print_stats(stats)


if __name__ == '__main__':
    do_queries()
