# Class describing a pair of adjacent tiles
# Used as index into walls map, cleaner than using a 4-tuple

class AdjPair(object):
    def __init__(self, t1, t2):
        (x1,y1) = t1
        (x2,y2) = t2
        if x1 != x2 and y1 != y2:
            raise ValueError("Attempted to create a pair of tiles not adjacent to each other")
        
        if abs(x1-x2) > 1 or abs(y1-y2) > 1:
            raise ValueError("Attempted to create a pair of tiles not adjacent to each other")

        self.t1 = min(t1, t2)
        self.t2 = max(t1, t2)

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2

    def __hash__(self):
        return hash((self.t1, self.t2))

    def get_wall_coords(self, px_per_tile):
        if self.t1[0] != self.t2[0]:
            # vertical wall between two horizontally-adjacent tiles
            wall_x = px_per_tile * self.t2[0]
            wall_y1 = px_per_tile * self.t1[1]
            wall_y2 = px_per_tile * (self.t1[1] + 1)
            return ((wall_x, wall_y1), (wall_x, wall_y2))

        else:
            # horizontal wall between two vertically-adjacent tiles
            wall_y = px_per_tile * self.t2[1]
            wall_x1 = px_per_tile * self.t1[0]
            wall_x2 = px_per_tile * (self.t1[0] + 1)
            return ((wall_x1, wall_y), (wall_x2, wall_y))
