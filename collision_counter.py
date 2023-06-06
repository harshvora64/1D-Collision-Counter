import math

def round4(x):
    return round(x,4)

class Point():
    """Point class to store points(objects)
    It stores the mass, position, index, velocity of each object"""
    def __init__(self,i,m,x,v):
        self._index=i
        self._mass=m
        self._position=x
        self._velocity=v

    def m(self):
        return self._mass
    def v(self):
        return self._velocity
    def x(self):
        return self._position
    def i(self):
        return self._index
    
    def update_v(self,v):               # update velocity
        self._velocity = v
    def update_x(self,x):               # update position
        self._position = x
    def update(self,T):                 # update the position to the position after time T (x+=v*T)
        self._position += T* self.v()

    def collide(P1,P2):                 # to update the velocity of two colliding points
        m1=P1.m()
        m2=P2.m()
        v1=P1.v()
        v2=P2.v()
        P2.update_v((2*m1*v1)/(m1+m2)-((m1-m2)*v2)/(m1+m2))
        P1.update_v(((m1-m2)*v1)/(m1+m2)+(2*m2*v2)/(m1+m2))

class Collision():
    """class Collision, whose object stores:
    the time of collision between two objects ( i an i+1)
    the position x where the collision happens
    the 'key' which is the list of [time,index] to compare them for sorting in the minheap
    and 'location' which is the position of the object in the heap list
    this is done to avoid searching for the object in the heap in O(n) .. this makes it O(1)"""
    def __init__(self,P1,P2):
        x1=P1.x()
        x2=P2.x()
        self._time=(x2-x1)/(P1.v()-P2.v()) if P1.v() != P2.v() else math.inf
        m1=P1.m()
        m2=P2.m()
        self._x = x1+self._time*P1.v()              # position of collision
        if self._time<0 or x1>x2:
            self._time=math.inf                     # 'no collision' is stored as infinite time
        self._i=P1.i()
        self._key=[self._time,self._i]
        self._location=self._i                      # location is initialised to index

    def key(self):
        return self._key
    def location(self):
        return self._location
    def set_location(self,l):                       # to update location
        self._location=l
    def update(self,T):                             # to increment the time for collision to happen by T
        self._time += T
        self._key[0]=self._time
    def t(self):
        return self._time
    def x(self):
        return self._x
    def i(self):
        return self._i

class MinHeap():
    """class MinHeap to store the "collision" objects as a minheap
    entries - to store the objects in the list _heap, sorted according to the level order traversal of a minheap
    _collisions - stores theCollision objects in the increasing order of index - it stores the same objects which are in _heap (same reference) but in increasing order of index"""
    def __init__(self,entries):
        l=len(entries)
        self._collisions=entries
        self._heap=entries.copy()       # _heap stores the same (reference) objects as _collisions, but the lists are different
        
        j=l-1
        while(j>=0):                    # fast build heap algorithm using heap_down from the bottom of the heap to the top
                                        # complexity O(n) - runs only once 
            self.heap_down(j)
            j-=1



    def heap_down(self,location):                   # worst case complexity O(log(n))   
                                                    # location is the position in the heap whose position is to be corrected using heap_dowm
        j=location*2+1                              # left child of location
        l=len(self._heap)
        while j<l:
            hloc=self._heap[location].key()         # key list is used to compare Collision objects
            hj=self._heap[j].key()
            if j+1<l:                               # if right child exists then check that too, else initialise it to infinity
                hj1 = self._heap[j+1].key()
            else:
                hj1=[math.inf,math.inf]
            if hloc<min(hj,hj1):
                break
            else:
                k = j if hj<hj1 else j+1
                self._heap[location],self._heap[k]=self._heap[k],self._heap[location]       # swap with smaller child if parent is larger than children
                self._heap[location].set_location(location)                                 # update the location variable of the swapped Collision objects
                self._heap[k].set_location(k)
                location = k                                                                # update location of object and left child
                j=location*2+1
    
    def heap_up(self,location):                     # worst case complexity O(log(n))
                                                    # location is the position in the heap whose position is to be corrected using heap_up
        j=(location-1)//2                           # position of parent
        l=len(self._heap)
        while j>=0:
            hloc=self._heap[location].key()         # key list is used to compare Collision objects
            hj=self._heap[j].key()
            if hloc>hj:
                break
            else:
                self._heap[location],self._heap[j]=self._heap[j],self._heap[location]   # swap if child is larger than parent
                self._heap[location].set_location(location)                             # update the location variable of the swapped Collision objects
                self._heap[j].set_location(j)
                location = j                                                            # update location of object and parent
                j=(location-1)//2
    

    def reorder(self,new,location):         # complexity worst case O(log n)
                                            # used to bring the object at the given location to its correct position
        o=self._heap[location]              # new is a new collision object with updated time and x parameters, to update the object with the given location in the list _heap
        o._x=new._x
        o._time=new._time
        o._key[0]=new._key[0]
        self.heap_up(location)              # at a given time, only heap_up or heap_down will change _heap in O(log n), so the other is terminated in O(1)
        self.heap_down(location)

    def extract_min(self):                  # returns the minimum(root)(earliest collision) of the heap without modifying the heap
        return self._heap[0]

def listCollisions(M,x,v,m,t):
    ans=[]
    T=0
    inf=math.inf
    no_of_collisions=0
    points=[Point(i,M[i],x[i],v[i]) for i in range(len(M))]                     # list of points
    collisions = [Collision(points[i],points[i+1]) for i in range(len(M)-1)]    # list of Collision objects
    heap = MinHeap(collisions)                                                  # heap object created, collisions lsit is passed to initialise the heap


    while(T<=t and no_of_collisions<=m):
        collision=heap.extract_min()
        i=collision._key[1]             # index of the collision i (between particles i and i+1)
        T=collision.t()                 # time at which collision occurs
        if T>t:
            break
        no_of_collisions+=1
        if no_of_collisions>m:
            break
        a=(round4(T),collision.i(),round4(collision.x()))   # add collision to the answer
        ans.append(a)
        tx=ans[-1][2]                                       # position of the collision that just occured
        points[i].collide(points[i+1])                      # update velocities of colliding points

        # when a collision occurs, instead of changing the positions of all points and the time of all collisions,
        # we assume that the colliding particles had their new velocities from the beginning itelf
        # and then find their positions at time zero (T time before)   (tx-Vnew*T)
        # collision[i] time is set to infinity, as they can't collide immediately once they have already collidied
        # now we only need to update the time of collsions[i-1] and collisions[i+1], because only velocities of i and i+1 have changed
        # updating only 3 objects keeps the complexity O(log(n)) (from reorder)
        # and there can be maximum m collisions, so max O(m*logn) complexity

        points[i].update_x(tx-points[i].v()*T)                      # update the points[i] and [i+1]
        points[i+1].update_x(tx-points[i+1].v()*T)
        collisions[i].update(inf)                                   # set collision time of i and i+1 to infinity
        heap.reorder(collisions[i],collisions[i].location())        # bring collisions[i] to correct position

            
        if i!=0:                                                    # update collisions[i-1]
            c=Collision(points[i-1],points[i])
            loc=collisions[i-1].location()                          # find the location of collisions[i-1]
            c.set_location(loc)                                     # change location of c
            heap.reorder(c,loc)                                     # reorder the position at location
            
        if i!=len(M)-2:                                             # update the collisions[i+1]
            c=Collision(points[i+1],points[i+2])
            loc=collisions[i+1].location()
            c.set_location(loc)
            heap.reorder(c,loc)
    return(ans)