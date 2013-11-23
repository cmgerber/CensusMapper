#!../env/bin/python

from CensusMapperFlask import app
from db_models import *
import flask
from flask import request

@app.route('/map', methods = ['POST'])
def update_measure():
    
    cartocss = "#censusgeo { polygon-fill: rgb(178,226,226); line-width: .1; line-color: #444444; polygon-opacity: 0; line-opacity: 0;[ measure <= 1.00 ] { polygon-fill: rgb(179,0,0)}[ measure <= 0.40 ] { polygon-fill: rgb(227,51,74)}[ measure <= 0.25 ] { polygon-fill: rgb(252,89,141)}[ measure <= 0.15 ] { polygon-fill: rgb(253,138,204)}[ measure <= 0.05 ] { polygon-fill: rgb(254,217,240)} [zoom <= 4][geotype = 'state'] { polygon-opacity: 0.8; line-opacity: 1; } [zoom > 4][zoom <= 8][geotype = 'county'] { polygon-opacity: 0.8; line-opacity: 1; } [zoom > 8][geotype = 'tract'] { polygon-opacity: 0.8; line-opacity: 1; }}"
    sqlquery = "SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, sum(case when b.fieldid in ('B03002012') then cast(b.value as float) else 0 end)/(sum(case when b.fieldid in ('B01001001') then cast(b.value as float) else 0 end) + 1) measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator"
    
    js_command = 'add_tiles(map, sqlquery, cartocss);'
    
    return flask.render_template('main_map.html', sqlquery = sqlquery, cartocss = cartocss, js_command = js_command)

