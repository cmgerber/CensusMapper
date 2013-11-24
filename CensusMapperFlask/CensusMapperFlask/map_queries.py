#!../env/bin/python

from cartodb import CartoDBAPIKey, CartoDBException
from CensusMapperFlask import app
from db_models import *
from flask import request, Flask, jsonify, render_template
from pgconn import API_KEY

# establish connection to CartoDB server
def connect_to_cartodb():
    return CartoDBAPIKey(API_KEY, 'censusmapper')

# estab

s = cl.sql("select CDB_JenksBins(array_agg(measure::numeric), 5) from (SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, sum(case when b.fieldid in ('B03002012') then cast(b.value as float) else 0 end)/(sum(case when b.fieldid in ('B01001001') then cast(b.value as float) else 0 end) + 1) measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode where length(a.fipscode) = 5 GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator) layer")
