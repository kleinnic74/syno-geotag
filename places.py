import psycopg2
import psycopg2.extras
import json

_knownPlaces = dict()
_placeIds = 0

class Place:
    def __init__(self, id, parts):
        self._id = id
        self.parts = _make_unique(parts)
        self.path = ','.join(self.parts)
        self._name = parts[0]
    
    def __str__(self):
        return "%s[%d]" % (self.path, self._id)


class Geotags:
    def __init__(self, db):
        self._knownPlaces = dict()
        self.db = db
        self.cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("""SELECT id, name, info FROM photo_label WHERE category=2""")
        for tag in self.cursor:
            if len(tag['info']) > 0:
                 info = json.loads(tag['info'])
                 place = Place(tag['id'], info['parts'])
                 _knownPlaces[place.path] = place
    
    def place(self, parts):
        uniqueParts = _make_unique(parts)
        key = ','.join(uniqueParts)
        if key in self._knownPlaces:
            return self._knownPlaces[key]
        return self._newPlace(uniqueParts)
    
    def _newPlace(self, parts):
        info = json.dumps({'parts': parts})
        self.cursor.execute("""INSERT INTO photo_label (category, name, info)
                               VALUES (%(category)s, %(name)s, %(info)s) RETURNING id""", 
                               {'category': 2, 'name': info[0], 'info': info})
        id = self.cursor.fetchone()['id']
        self.db.commit()
        place = Place(id, parts)
        self._knownPlaces[place.path] = place
        return place

def _make_unique(items):
    result = []
    for i in items:
        if i != None and i not in result:
            result.append(i)
    return result

def place(parts):
    global _placeIds
    uniqueParts = _make_unique(parts)
    if len(uniqueParts) == 0:
        return None
    key = ','.join(uniqueParts)
    if key in _knownPlaces:
        return _knownPlaces[key]
    place = Place(_placeIds, uniqueParts)
    _placeIds += 1
    _knownPlaces[place.path] = place
    return place


if __name__ == "__main__":
    p1 = place(('Bernardswiller', 'Alsace', 'France'))
    p2 = place(('Obernai', 'Alsace', 'France'))
    print p1
    print p2
    conn = psycopg2.connect("dbname=photo user=postgres")
    geotags = Geotags(conn)


