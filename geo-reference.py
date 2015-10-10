import psycopg2
import psycopg2.extras
import geocoder

from places import Geotags
from geoImages import GeoTaggedImages

class Locations:
    def __init__(self, tags):
        self.tags = tags
        self.cache = dict()
        self.places = dict()
    
    def find(self, lat, lng):
        if (abs(lat) > 180 or abs(lng) > 90):
                return None
        id = "%f,%f" % (lat, lng)
        if id in self.cache:
            return self.cache[id]
        address = geocoder.google([lat, lng], method='reverse')
        if address == None:
            self.cache[id] = None
            return None
        self.cache[id] = self.tags.place((address.city, address.state, address.country))
        found = self.cache[id]
        print " --> %s" % map(str, found)
        return found


try:
    conn = psycopg2.connect("dbname=photo user=postgres")

    l = Locations(Geotags(conn))
    images = GeoTaggedImages(conn)
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT id, path, lat, lng FROM photo_image 
                   WHERE lat IS NOT NULL AND
                         id NOT IN (SELECT image FROM geo_tagged_images)""")
    
    count = 0
    for img in cur:
        print "Image %s... [%f, %f]" % (img['path'], img['lat'], img['lng'])
        loc = l.find(img['lat'], img['lng'])
        images.save(img['id'], loc)
        count += 1
    print "Found %d GPS-referenced images" % count
    
except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)
    
finally:
    if conn:
        conn.close()
