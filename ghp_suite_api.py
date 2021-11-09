# ghp_suite_api.py
# Helper functions for GHP Suite API
#
# Copyright 2021 – Grupo Hotelero Prisma. All rights reserved.
#   Yukie Ley <yukie.ley@hotelesprisma.com>
#   Rodrigo Cantú <rodrigo.cantu@hotelesprisma.com>
#
# Version 1.4 – 2021/11/05
#
# These methods do not save any data to disk, its only stored in memory.
#
# References:
# https://github.com/pandas-dev/pandas/blob/v1.3.3/pandas/io/parsers/readers.py#L491-L586
# https://docs.python.org/3/c-api/memory.html
# https://www.w3schools.com/tags/ref_httpmethods.asp
# https://developer.mozilla.org/en-US/docs/Glossary/cacheable

import pandas as pd
import requests
import json
from requests.api import get
from http.client import responses
from datetime import datetime

class GHPSuiteApiConnector():
    BASE_ENDPOINT = "https://api.suite.ghp.mx"
    TIMEOUT = 60 # seconds

    def __init__(self,token):
        self.token = token


    # this function returns an empty string if no error was found
    def test_connection(self):
        endpoint=self.BASE_ENDPOINT

        try:
            self.__execute_http_get(endpoint)
            return ''
        except Exception as e:
            return str(e)


    def get_venues(self):
        endpoint=self.BASE_ENDPOINT+'/venue/list'

        return self.__execute_http_get(endpoint)


    def get_venues_df(self):
        json_data = self.get_venues()

        df = pd.json_normalize(json_data)
        return df


    def get_market_daily(self, venue, start_date, end_date):
        endpoint = self.BASE_ENDPOINT+'/market/daily?start_date='+start_date+'&end_date='+end_date+'&venue_code='+venue

        return self.__execute_http_get(endpoint)


    def get_market_daily_df(self, venue, start_date, end_date):
        json_data = self.get_market_daily(venue,start_date,end_date)

        ky = list(json_data.keys())
        df_final = pd.DataFrame()
        for i in range(len(ky)):
            df = pd.DataFrame(json_data[ky[i]]['daily'])
            df.columns = [''] * len(df.columns)
            df = df.T
            df_final = df_final.append(df)

        return df_final


    def get_procurement_material_catalog(self):
        endpoint = self.BASE_ENDPOINT+'/procurement/material-catalog'

        return self.__execute_http_get(endpoint)
    
    def get_procurement_material_catalog_df(self):
        json_data = self.get_procurement_material_catalog()

        df = pd.json_normalize(json_data)
        return df

    def get_procurement_vendor_catalog(self):
        endpoint = self.BASE_ENDPOINT+'/procurement/vendor-catalog'

        return self.__execute_http_get(endpoint)
    
    def get_procurement_vendor_catalog_df(self):
        json_data = self.get_procurement_vendor_catalog()

        df = pd.json_normalize(json_data)
        return df


    def get_procurement_purchase_orders(self, venue, start_date, end_date):
        endpoint = self.BASE_ENDPOINT+'/procurement/purchase-orders?start_date='+start_date+'&end_date='+end_date+'&venue_code='+venue

        return self.__execute_http_get(endpoint)

    def get_procurement_purchase_orders_df(self, venue, start_date,end_date):
        
        json_data = self.get_procurement_purchase_orders(venue,start_date,end_date)
        ky = list(json_data.keys())
        df_final = pd.DataFrame()
        
        for i in range(len(ky)):
            items = pd.json_normalize(json_data[ky[i]]['items'])
        
            purchase_order_id = json_data[ky[i]]['purchase_order_id']
            vendor_id = json_data[ky[i]]['vendor_id']
            date = datetime.strptime(json_data[ky[i]]['date']['date'],'%Y-%m-%d %H:%M:%S.%f').date()
            company_code = json_data[ky[i]]['company_code']
            vendor_negotiation_type = json_data[ky[i]]['vendor_negotiation_type']
            vendor_region_name = json_data[ky[i]]['vendor_region_name']
            document_type = json_data[ky[i]]['document_type']
            
            for j in range(len(items)):
                items['purchase_order_id'] = purchase_order_id
                items['vendor_id'] = vendor_id
                items['date'] = date
                items['company_code'] = company_code
                items['vendor_negotiation_type'] = vendor_negotiation_type
                items['vendor_region_name'] = vendor_region_name
                items['document_type'] = document_type
            
            df_final = df_final.append(items)

        return df_final


    # PRIVATE METHODS (HELPERS)

    def __execute_http_get(self, endpoint):
        # Defining custom headers.
        headers={
            'Authorization': 'Bearer ' + str(self.token),
            'Content-Type': 'application/json'
        }

        # Execute the GET request specifying the custom headers.
        try:
            r = requests.get(endpoint, headers=headers, timeout=self.TIMEOUT)
        except Exception as e:
            raise RuntimeError('Connection error: ' + str(e))

        #if r.status_code != 200:
        #    raise RuntimeError('Invalid HTTP response from server: ' + str(r.status_code) + ': ' + responses[r.status_code])

        try:
            json_results = json.loads(r.text)
        except Exception as e:
            raise RuntimeError('API error: invalid JSON response')

        if 'status' not in json_results:
            raise RuntimeError('API error: invalid JSON envelope (missing "status")')

        if json_results['status'] != 'success':
            raise RuntimeError('API error: ' + self.__get_api_error_string_from_response(json_results))

        if 'data' not in json_results:
            raise RuntimeError('API error: invalid JSON envelope (missing "data")')

        return json_results['data']


    def __get_api_error_string_from_response(self, json_results):
        s = ''
        if "error_code" in json_results:
            s = s + json_results["error_code"] + " - "

        if "error_message" in json_results:
            s = s + json_results["error_message"]

        return s