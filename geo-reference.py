import psycopg2
import psycopg2.extras
import geocoder

from places import Geotags

class Locations:
    def __init__(self, tags):
        self.tags = tags
        self.cache = dict()
        self.places = dict()
    
    def find(self, lat, lng):
        id = "%f,%f" % (lat, lng)
        if id in self.cache:
            return self.cache[id]
        address = geocoder.here([lat, lng], method='reverse')
        if address == None:
            self.cache[id] = None
            return None
        self.cache[id] = self.tags.place((address.city, address.state, address.country))
        return self.cache[id]


try:
    conn = psycopg2.connect("dbname=photo user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT id, path, lat, lng LIMIT 10 FROM photo_image WHERE lat IS NOT NULL""")
    count = 0
    l = Locations(Geotags(conn))
    for img in cur:
        loc = l.find(img['lat'], img['lng'])
        print "[%s] %s: %s" % (img['id'], img['path'], loc)
        count += 1
    print "Found %d GPS-referenced images" % count
    
except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)
    
finally:
    if conn:
        conn.close()
