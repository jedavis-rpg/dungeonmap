# Class describing a dungeon level

import random

from PIL import Image, ImageDraw, ImageColor

from adjpair import AdjPair
from border import Border
from loop import Loop
from room import Room
from unionfinder import UnionFinder

ANIMATE = True

class Level(object):

    def __init__(self, width=25, height=25):
        self.width = width
        self.height = height
        walls = {}
        for x in range(0, width):
            for y in range(0, height):
                if x != width-1:
                    p1 = [(x,y),(x+1,y)]
                    walls[AdjPair((x,y),(x+1,y))] = Border.WALL
                if y != height - 1:
                    p2 = [(x,y),(x,y+1)]
                    walls[AdjPair((x,y),(x,y+1))] = Border.WALL
        self.walls = walls
        self.uf = UnionFinder(width, height)
        self.rooms = []
        self.loops = []
        self.frames = []

    def add_room(self, r):
        for ap in r.all_adjpairs():
            self.walls[ap] = Border.EMPTY
            self.uf.union(ap.t1, ap.t2)
        self.rooms.append(r)

    def gen_random_rooms(self, room_frac=0.5):
        room_dim_dist = [2, 2, 3, 3, 3, 4, 4, 5]
        total_room_area = 0
        while total_room_area / (self.width * self.height) < room_frac:
            rand_corner = (random.randint(0, self.width-2), random.randint(0, self.height-2))
            rand_width = random.choice(room_dim_dist)
            if rand_corner[0] + rand_width >= self.width:
                rand_width = self.width - rand_corner[0]
            rand_height = random.choice(room_dim_dist)
            if rand_corner[1] + rand_height >= self.height:
                rand_height = self.height - rand_corner[1]
            cand = Room(rand_corner, rand_width, rand_height)

            # no overlapping rooms, only roomify leaderless areas
            rejected = False
            for t in cand.all_tiles():
                if self.uf.ranks[t] != 0 or self.uf.find(t) != t:
                    rejected = True

            if not rejected:
                self.add_room(cand)
                total_room_area += rand_height * rand_width
                self.append_frame()

    def add_loop(self, l):
        for ap in l.all_adjpairs():
            # TODO sometimes place a secret door instead
            # once I have tech for actually drawing secret doors
            self.walls[ap] = Border.EMPTY
            self.uf.union(ap.t1, ap.t2)
        self.loops.append(l)

    def gen_random_loops(self, num_loops = 7):
        loop_dim_dist = [6, 6, 7, 7, 8, 9, 10]
        for i in range(num_loops):
            rand_corner = (random.randint(0, self.width-3), random.randint(0, self.height-3))
            rand_width = random.choice(loop_dim_dist)
            if rand_corner[0] + rand_width >= self.width:
                rand_width = self.width - rand_corner[0]
            rand_height = random.choice(loop_dim_dist)
            if rand_corner[1] + rand_height >= self.height:
                rand_height = self.height - rand_corner[1]
            cand = Loop(rand_corner, rand_width, rand_height)

            self.add_loop(cand)
            self.append_frame()

    def uf_maze(self):
        walls_list = [k for (k,v) in self.walls.items() if v == Border.WALL]
        random.shuffle(walls_list)
        i = 0
        for w in walls_list:
            if not self.uf.check_connected(w.t1, w.t2):
                self.walls[w] = Border.EMPTY
                self.uf.union(w.t1, w.t2)
                i+=1
                if i % 10 == 0:
                    self.append_frame()

    def draw_border(self, draw, px_per_tile):
        max_x = px_per_tile * self.width - 1
        max_y = px_per_tile * self.height - 2
        corners = [(0,1),(0,max_y),(max_x,max_y),(max_x,1),(0,1)]
        draw.line(corners, ImageColor.getrgb("black"), 2)

    def draw_frame(self, px_per_tile=20):
        im = Image.new('RGB', (self.width * px_per_tile, self.height * px_per_tile), ImageColor.getrgb("white"))
        draw = ImageDraw.Draw(im)

        for coords, bord in self.walls.items():
            wall_coords = coords.get_wall_coords(px_per_tile)
            color = (0, 128, 256)  # dim light blue
            width = 1
            if bord == Border.WALL:
                width = 3
                color = ImageColor.getrgb("black")
            draw.line(wall_coords, color, width)

        self.draw_border(draw, px_per_tile)

        return im

    def append_frame(self):
        if ANIMATE:
            self.frames.append(self.draw_frame())

    def draw(self, outpath, px_per_tile=20):
        self.frames.append(self.draw_frame(px_per_tile))

        if outpath.endswith(".gif"):
            self.frames[0].save(outpath, save_all=True, append_images=self.frames[1:] + [self.frames[-1]]*40, duration=100, loop=0)
        else:
            self.frames[-1].save(outpath)

if __name__ == "__main__":
    l = Level()
    l.gen_random_rooms()
    l.gen_random_loops()
    l.uf_maze()
    if ANIMATE:
        l.draw("./test.gif")
    else:
        l.draw("./test.jpg")
