_knownPlaces = dict()
_placeIds = 0

def _make_unique(items):
    result = []
    for i in items:
        if i != None and i not in result:
            result.append(i)
    return result

class Place:
    def __init__(self, id, parts):
        self.id = id
        self.parts = _make_unique(parts)
        self.path = ','.join(self.parts)
        self.name = parts[0]
    
    def __str__(self):
        return "%s[%d]" % (self.path, self.id)
    

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



