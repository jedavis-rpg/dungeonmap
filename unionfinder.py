# Class maintaining union-find algorithm state

class UnionFinder(object):

    def __init__(self, width, height):
        self.leaders = {}
        self.ranks = {}
        for t in [(x,y) for x in range (width) for y in range(height)]:
            self.leaders[t] = t
            self.ranks[t] = 0

    # Finds the leader of t's connected component and returns it
    # Updates leader state of all intermediate tiles
    def find(self, t):
        if t not in self.leaders:
            raise ValueError("Attempting to find leader for unknown tile %s" % (t,))
        curr = t
        to_update = set()
        while self.leaders[curr] != curr:
            to_update.add(curr)
            curr = self.leaders[curr]

        for u in to_update:
            self.leaders[u] = curr
        
        return curr

    def check_connected(self, t1, t2):
        l1 = self.find(t1)
        l2 = self.find(t2)
        return l1 == l2

    # Perform union-by-rank
    def union(self, t1, t2):
        l1 = self.find(t1)
        l2 = self.find(t2)
        if l1 == l2:
            return
        r1 = self.ranks[l1]
        r2 = self.ranks[l2]
        if r1 > r2:
            self.leaders[l2] = l1
        elif r1 < r2:
            self.leaders[l1] = l2
        else:
            self.leaders[l2] = l1
            self.ranks[l1] += 1


