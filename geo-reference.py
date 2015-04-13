import psycopg2
import psycopg2.extras
import geocoder

from places import place

class Locations:
    def __init__(self):
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
        self.cache[id] = place((address.city, address.state, address.country))
        return self.cache[id]


try:
    conn = psycopg2.connect("dbname=photo user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT id, path, lat, lng FROM photo_image')
    count = 0
    l = Locations()
    while True:
        img = cur.fetchone()
        if img == None:
            break
        if img['lat'] != None and img['lng'] != None:
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
