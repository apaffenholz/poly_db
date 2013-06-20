#!/usr/bin/python

from xml.dom import minidom
import sys
import array
import string
import pymongo
import datetime
import time

simple_properties = [
	'CONE_DIM', 
	'N_VERTICES', 
	'N_FACETS'
	'FACET_WIDTH',
	'LATTICE_VOLUME',
	'N_INTERIOR_LATTICE_POINTS',
	'N_BOUNDARY_LATTICE_POINTS',
	'CANONICAL',
	'COMPRESSED',
	'ESSENTIALLY_GENERIC',
	'GORENSTEIN',
	'LATTICE_CODEGREE',
	'LATTICE_DEGREE',
	'REFLEXIVE',
	'SMOOTH',
	'TERMINAL',
	'VERY_AMPLE'
]

vector_properties = [
	'FACET_WIDTHS',
	'H_STAR_VECTOR',
	'EHRHART_POLYNOMIAL_COEFF'
]

matrix_properties = [
	'VERTICES',
	'FACETS'
]

def poly2dict(file, contrib, date): 
	pt(file)
		
	xmldoc = minidom.parse(file)
	pt("parsed xml")
	
	obj = xmldoc.getElementsByTagName('object')[0]
	pt ("got obj")
	
	name = obj.attributes['name'].value
	type = obj.attributes['type'].value

	properties = xmldoc.getElementsByTagName('property')
	pt ("got props")
	
	dict = {}
	
	dict['id'] = name
	dict['date'] = date
	dict['contributor'] = contrib
# 	dict['type'] = type
	
	for p in properties:
		key = p.attributes['name'].value
		if key in simple_properties:
			val = p.attributes['value'].value
			if val == 'false': 
				val = 0
			elif val == 'true':
				val = 1
			else:
				val = int(val)
			dict[key] = val
			
# 	dict['DIM'] = dict['CONE_DIM']-1
	pt("built dict")
	return dict


def poly2json(dict):
	return make_json_string(dict)

def make_json_simple(key, value):
	return ''.join(['"',key,'": "',value,'"'])

def make_json_string(dict):
	s = "{\n" +	string.join((make_json_simple(k,v) for k,v in dict.iteritems()), ',\n') + "\n}"
	return s
	
	

def add_to_db(obj, contrib):
	mongo = pymongo.MongoClient("localhost", 27017)
	db = mongo.pm
	db.test.save(poly2dict(obj, contrib, datetime.datetime.now().strftime("%Y-%m-%d")))


def add_list_to_db(objects, contrib):
	pt("start")
	mongo = pymongo.MongoClient("localhost", 27017)
	db = mongo.pm
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	for obj in objects:
		db.lattice_polys.save(poly2dict(obj, contrib, date))
	pt("done")

def pt(s):
	print s
	print time.time()-starting_time

starting_time = time.time()

contrib = "Andreas Paffenholz"
date = datetime.datetime.now().strftime("%Y-%m-%d")
add_list_to_db(sys.argv[1:] , contrib)
