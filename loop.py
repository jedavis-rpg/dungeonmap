# Class representing a forced loop

from adjpair import AdjPair

class Loop(object):

    def __init__(self, corner, width, height):
        # corner is the top-left corner of the loop
        self.corner = corner
        self.width = width
        self.height = height

    def __repr__(self):
        return "Loop((%s), %d, %d)" % (self.corner, self.width, self.height)

    # returns a set of all coordinate tuples on the edge of the loop
    def all_tiles(self):
        x0, y0 = self.corner
        out = set()
        for x in range(self.width):
            out.add((x0+x,y0))
            out.add((x0+x,y0+self.height-1))
        for y in range(self.height):
            out.add(x0,y0+y)
            out.add(x0+self.width-1,y0+y)
        return out

    # returns a set of all adjacent pairs of tuples on the edge of the loop
    def all_adjpairs(self):
        x0, y0 = self.corner
        out = set()
        for xoff in range(self.width-1):
            for yoff in [0, self.height-1]:
                t1 = (x0+xoff, y0+yoff)
                t2 = (x0+xoff+1, y0+yoff)
                out.add(AdjPair(t1, t2))

        for xoff in [0, self.width-1]:
            for yoff in range(0, self.height-1):
                t1 = (x0+xoff, y0+yoff)
                t2 = (x0+xoff, y0+yoff+1)
                out.add(AdjPair(t1, t2))

        return out

    def draw_rect(self, draw, px_per_tile):
        x0, y0 = self.corner
        xp, yp = (x0+0.5) * px_per_tile, (y0+0.5) * px_per_tile
        x2 = xp + ((self.width-1) * px_per_tile)
        y2 = yp + ((self.height-1) * px_per_tile)
        color = (128,0,0)
        draw.rectangle([(xp, yp), (x2, y2)], outline=color)


