# Class representing a rectangular room

from adjpair import AdjPair

class Room(object):

    def __init__(self, corner, width, height):
        # corner is the top-left corner of the room
        self.corner = corner
        self.width = width
        self.height = height

    def __repr__(self):
        return "Room((%s), %d, %d)" % (self.corner, self.width, self.height)

    # returns a set of all coordinate tuples contained within the room
    def all_tiles(self):
        x0, y0 = self.corner
        out = set()
        for x in range(self.width):
            for y in range(self.height):
                out.add((x0+x,y0+y))
        return out

    # returns a set of all adjacent pairs of tuples within the room
    def all_adjpairs(self):
        x0, y0 = self.corner
        out = set()
        for xoff in range(self.width):
            for yoff in range(self.height):
                t1 = (x0+xoff, y0+yoff)
                if xoff != self.width-1:
                    t2 = (x0+xoff+1, y0+yoff)
                    out.add(AdjPair(t1, t2))
                if yoff != self.height-1:
                    t2 = (x0+xoff, y0+yoff+1)
                    out.add(AdjPair(t1, t2))
        return out

    def draw_ellipse(self, draw, px_per_tile):
        x0, y0 = self.corner
        xp, yp = x0 * px_per_tile, y0 * px_per_tile
        x2 = xp + (self.width * px_per_tile)
        y2 = yp + (self.height * px_per_tile)
        color = (128,0,0)
        draw.ellipse([(xp, yp), (x2, y2)], outline=color)


