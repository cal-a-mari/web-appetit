# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

"""
This notebook includes all the main functions we created to parse Flickr photo data
"""

# <codecell>

import flickrapi
from flickrapi import shorturl
from IPython.display import display, Image
import json

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series, Index
import pandas as pd
from itertools import islice

APIKEY = "800f28ae42a58a95f0005fb0fe022a78"

flickr = flickrapi.FlickrAPI(APIKEY)

# <codecell>

from IPython.display import HTML
from jinja2 import Template

CSS = """
<style>
  .wrap img {
    margin-left: 0px;
    margin-right: 0px;
    display: inline-block;
    width: 150px;
  }
  
.wrap {
   /* Prevent vertical gaps */
   line-height: 0;
   
   -webkit-column-count: 5;
   -webkit-column-gap:   0px;
   -moz-column-count:    5;
   -moz-column-gap:      0px;
   column-count:         5;
   column-gap:           0px;
   
}
.wrap img {
  /* Just in case there are inline attributes */
  width: 100% !important;
  height: auto !important;
}

</style>
"""

IMAGES_TEMPLATE = CSS + """
<div class="wrap">
 {% for item in items %}<img src="{{item}}"/>{% endfor %}
</div>
"""

template = Template(IMAGES_TEMPLATE)

# To display photos in HTML, use:

# photos = get_photos_static_urls(flickr.photos_search(
#     tag_mode='any',
#     text='uc berkeley',
#     format='json'))

#   template = Template(IMAGES_TEMPLATE)
#   HTML(template.render(items=photos[:30]))  # shows first 30 photos

# <codecell>

"""
Given a flickr api search query with format='json', returns the data in actual json format

get_json(flickr.photos_search(
        tag_mode='any',
        tags='dog',
        license='7',
        format='json'))
"""
def get_json(flickr_search_response):
    json_string = flickr_search_response[14:-1]
    return json.loads(json_string)

"""
Returns the json data including pages, total photo count, and list of photos
"""
def get_data(flickr_search_response):
    return get_json(flickr_search_response)['photos']

"""
Returns the json list of photos

u'photo': [{u'farm': 6,
   u'id': u'11292885426',
   u'isfamily': 0,
   u'isfriend': 0,
   u'ispublic': 1,
   u'owner': u'12403504@N02',
   u'secret': u'f09443f484',
   u'server': u'5538',
   u'title': u"Image taken from page 392 of 'Northward over the \u201cGreat Ice\u201d: a 
    narrative of life and work along the shores and upon the interior ice-cap of Northern 
    Greenland in the years 1886 and 1891-1897 ... With maps, diagrams, and about eight hundred illustrations'"},
"""
def get_photos(flickr_search_response):
    return get_json(flickr_search_response)['photos']['photo']

def get_all_photos(tags='', text='', min_taken_date='', max_taken_date='', license='7'):
    res = flickr.photos_search(
        text=text,
        tags=tags,
        extras='license, date_upload, last_update, date_taken, owner_name, geo, tags, views, url_m',
        license=license,
        min_taken_date=min_taken_date,
        max_taken_date=max_taken_date,
        page=1,
        format='json')
    res_json = get_json(res)
    tot_pages = res_json['photos']['pages']
    photos = res_json['photos']['photo']
    
    for i in range(tot_pages): 
        next_page_res =  flickr.photos_search(
            text=text,
            tags=tags,
            extras='license, date_upload, last_update, date_taken, owner_name, geo, tags, views, url_m',
            license=license,
            min_taken_date=min_taken_date,
            max_taken_date=max_taken_date,
            page=i+2,
            format='json')
        next_page_res_json = get_json(next_page_res)
        photos += next_page_res_json['photos']['photo']
        
    num_photos = len(photos)
    return {'photos': photos, 'length': num_photos}

"""
Returns array of Flikr photo URLs -- opens in Flickr photo viewer
"""
def get_photo_urls(flickr_search_response):
    photo_list = get_photos(flickr_search_response)
    photo_urls = []
    for photo in photo_list:
        photo_urls.append(flickrapi.shorturl.url(photo['id']))
    return photo_urls

"""
Returns array of direct photo jpg URLs
"""
def get_photos_static_urls(flickr_search_response):
    photo_list = get_photos(flickr_search_response)
    photo_urls = []
    for photo in photo_list:
        # http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}_o.(jpg|gif|png)
        # http://farm1.staticflickr.com/2/1418878_1e92283336_m.jpg
        size = "m" # m, z, b
        # for list of sizes see https://www.flickr.com/services/api/misc.urls.html
        url = "http://farm" + str(photo['farm']) + ".staticflickr.com/" + photo['server'] + "/" + photo['id'] + "_" + photo['secret'] +  "_" + size + ".jpg"   
        photo_urls.append(url)
    return photo_urls

"""
Returns the count of results
"""
def get_count(flickr_search_response):
    return get_json(flickr_search_response)['photos']['total']

# <codecell>

"""
Search Parameters 

extras

A comma-delimited list of extra information to fetch for each returned record. 
Currently supported fields are: 

description, license, date_upload, date_taken, owner_name, icon_server, 
original_format, last_update, geo, tags, machine_tags, o_dims, views, 
media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o
"""

# <codecell>

"""
Examples of how to use function calls:
"""

# <codecell>

get_count(flickr.photos_search(
        tag_mode='any',
        tags='dog',
        license='7',
        format='json'))

# <codecell>

get_photos(flickr.photos_search(
        text='dog',
        extras='license, date_upload, last_update, date_taken, owner_name, geo, tags, views, url_m',
        license='7',
        format='json'))

# <codecell>

get_all_photos(tags='dogs', text='dogs')

# <codecell>

get_photos(flickr.photos_search(
        text='dog',
        extras='license, date_upload, last_update, date_taken, owner_name, geo, tags, views, url_m',
        license='7',
        format='json'))

# <codecell>

photos = get_photos_static_urls(flickr.photos_search(
        tag_mode='any',
        tags='dog, puppy',
        license='7',
        format='json'))

HTML(template.render(items=photos[:20])) 

# <codecell>


