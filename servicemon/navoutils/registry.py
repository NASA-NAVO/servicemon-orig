# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
VO Queries
"""

from __future__ import print_function, division
from astroquery.query import BaseQuery

from . import utils

__all__ = ['Registry', 'RegistryClass']


class RegistryClass(BaseQuery):
    """
    Registry query class.
    """

    def __init__(self):

        super(RegistryClass, self).__init__()
        self._TIMEOUT = 60  # seconds
        self._RETRIES = 2  # total number of times to try
        self._REGISTRY_TAP_SYNC_URL = "http://vao.stsci.edu/RegTAP/TapService.aspx/sync"

    def query(self, **kwargs):

        adql = self._build_adql(**kwargs)
        if adql is None:
            raise ValueError('Unable to compute query based on input arguments.')

        if kwargs.get('verbose'):
            print('Registry:  sending query ADQL = {}\n'.format(adql))

        url = self._REGISTRY_TAP_SYNC_URL

        tap_params = {
            "request": "doQuery",
            "lang": "ADQL",
            "query": adql
        }

        response = utils.try_query(url, post_data=tap_params, timeout=self._TIMEOUT, retries=self._RETRIES)

        if kwargs.get('verbose'):
            print('Queried: {}\n'.format(response.url))

        aptable = utils.astropy_table_from_votable_response(response)
        return aptable

    # TBD support list of wavebands
    # TBD maybe support raw ADQL clause (or maybe we should just make
    # sure they can call a basic TAP query)
    def _build_adql(self, **kwargs):

        # Default values
        service_type = ""
        keyword = ""
        waveband = ""
        source = ""
        publisher = ""
        order_by = ""
        logic_string = " and "

        # Find the keywords we recognize
        for key, val in kwargs.items():
            if key == 'service_type':
                service_type = val
            elif key == 'keyword':
                keyword = val
            elif key == 'waveband':
                waveband = val
            elif key == 'source':
                source = val
            elif key == 'publisher':
                publisher = val
            elif key == 'order_by':
                order_by = val
            elif key == 'logic_string':
                logic_string = val

        ##
        if "image" in service_type.lower():
            service_type = "simpleimageaccess"
        elif "spectr" in service_type.lower():
            service_type = "simplespectralaccess"
        elif "cone" in service_type.lower():
            service_type = "conesearch"
        elif 'tap' in service_type or 'table' in service_type:
            service_type = "tableaccess"
        else:
            print("ERROR: please give a service_type that is one of image, spectral, cone, or table")
            return None

        query_retcols = """
          select res.waveband,res.short_name,cap.ivoid,res.res_description,
          intf.access_url,res.reference_url,res_role.role_name as publisher,cap.cap_type as service_type
          from rr.capability as cap
            natural join rr.resource as res
            natural join rr.interface as intf
            natural join rr.res_role as res_role
            """

        query_where = " where "

        wheres = []
        if service_type != "":
            wheres.append("cap.cap_type like '%{}%'".format(service_type))

        # currently not supporting SIAv2 in SIA library.
        if service_type == 'simpleimageaccess':
            wheres.append("standard_id != 'ivo://ivoa.net/std/sia#query-2.0'")
        if source != "":
            wheres.append("cap.ivoid like '%{}%'".format(source))
        if waveband != "":
            if ',' in waveband:
                allwavebands = []
                for w in waveband.split(','):
                    allwavebands.append("res.waveband like '%{}%' ".format(w).strip())
                wheres.append("(" + " or ".join(allwavebands) + ")")
            else:
                wheres.append("res.waveband like '%{}%'".format(waveband))

        wheres.append("res_role.base_role = 'publisher'")
        if publisher != "":
            wheres.append("res_role.role_name like '%{}%'".format(publisher))

        if keyword != "":
            keyword_where = """
             (res.res_description like '%{}%' or
            res.res_title like '%{}%' or
            cap.ivoid like '%{}%')
            """.format(keyword, keyword, keyword)
            wheres.append(keyword_where)

        query_where = query_where+logic_string.join(wheres)

        if order_by != "":
            query_order = "order by {}".format(order_by)
        else:
            query_order = ""

        query = query_retcols+query_where+query_order

        return query

    def query_counts(self, field, minimum=1, **kwargs):

        adql = self._build_counts_adql(field, minimum)

        if kwargs.get('verbose'):
            print('Registry:  sending query ADQL = {}\n'.format(adql))

        url = self._REGISTRY_TAP_SYNC_URL

        tap_params = {
            "request": "doQuery",
            "lang": "ADQL",
            "query": adql
        }

        response = self._request('POST', url, data=tap_params, cache=False)

        if kwargs.get('verbose'):
            print('Queried: {}\n'.format(response.url))

        aptable = utils.astropy_table_from_votable_response(response)
        return aptable

    def _build_counts_adql(self, field, minimum=1):

        field_table = None
        field_alias = field
        query_where_filter = ''
        if field.lower() == 'waveband':
            field_table = 'rr.resource'
        elif field.lower() == 'publisher':
            field_table = 'rr.res_role'
            field = 'role_name'
            query_where_filter = ' where base_role = \'publisher\' '
        elif field.lower() == 'service_type':
            field_table = 'rr.capability'
            field = 'cap_type'

        if field_table is None:
            return None
        else:
            query_select = 'select ' + field + ' as ' + field_alias + ', count(' + field + ') as count_' + field_alias
            query_from = ' from ' + field_table
            query_where_count_min = ' where count_' + field_alias + ' >= ' + str(minimum)
            query_group_by = ' group by ' + field
            query_order_by = ' order by count_' + field_alias + ' desc'

            query = 'select * from (' + query_select + query_from + query_where_filter + query_group_by + ') as count_table' + query_where_count_min + query_order_by

            return query


Registry = RegistryClass()


def display_results(results):
    # Display results in a readable way including the
    # short_name, ivoid, res_description and reference_url.

    for row in results:
        md = f'{row["short_name"]} ({row["ivoid"]})'
        print(md)
        print(row['res_description'])
        print(f'(More info: {row["reference_url"]} )')
