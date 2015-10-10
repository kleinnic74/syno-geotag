#!/usr/bin/env python
# encoding: utf-8
"""
geo-tagged-images.py

Created by nico on 2015-10-10.
Copyright (c) 2015 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import psycopg2
import psycopg2.extras


class GeoTaggedImages:
	def __init__(self, conn):
	    self._conn = conn
	    self._cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	    try:
	        self._cursor.execute("""CREATE TABLE geo_tagged_images
	                                (image integer NOT NULL, 
	                                 place integer NOT NULL,
	                                 CONSTRAINT geo_tagged_images_pkey PRIMARY KEY (image, place),
	                                 CONSTRAINT geo_tagged_images_image_fkey1 FOREIGN KEY (image)
	                                     REFERENCES photo_image (id) MATCH SIMPLE
	                                     ON UPDATE RESTRICT ON DELETE CASCADE,
	                                 CONSTRAINT geo_tagged_images_place_fkey1 FOREIGN KEY (place)
	                                     REFERENCES photo_label (id) MATCH SIMPLE
	                                     ON UPDATE RESTRICT ON DELETE CASCADE)""")
	    except psycopg2.DatabaseError, e:
	        print 'Creating table geo_tagged_images failed: %s' % e
	        conn.rollback()
	
	def save(self, image, tags):
	    if (image == None or tags == None or len(tags) == 0):
	        return
	    for tag in tags:
	        self._cursor.execute("""INSERT INTO geo_tagged_images (image, place)
	                            VALUES (%(image)s, %(place)s)""",
	                            {'image':image, 'place': tag._id})
	        self._cursor.execute("""INSERT INTO photo_image_label (image_id, label_id, status)
	                            VALUES (%(image)s, %(place)s, TRUE)""",
	                            {'image':image, 'place': tag._id})
	    self._conn.commit()

