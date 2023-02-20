import cv2 as cv
import numpy as np
import queue
import random

DIRECTION = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
FORWARD = [
    [(0,1),(1,1),(-1,1)],
    [(0,1),(1,1),(-1,1),(1,0),(1,-1)],
    [(1,1),(1,0),(1,-1)],
    [(1,1),(1,0),(1,-1),(0,-1),(-1,-1)],
    [(1,-1),(0,-1),(-1,-1)],
    [(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)],
    [(-1,-1),(-1,0),(-1,1)],
    [(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]
]

roi = cv.imread('1.jpg')

gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

edge = cv.Canny(gray,50,150)

edge_out = edge.copy()

for i in range(1,edge.shape[0]-1):
    for j in range(1,edge.shape[1]-1):
        n0 = edge.item(i,j+1) == 255
        n1 = edge.item(i+1,j+1) == 255
        n2 = edge.item(i+1,j) == 255
        n3 = edge.item(i+1,j-1) == 255
        n4 = edge.item(i,j-1) == 255
        n5 = edge.item(i-1,j-1) == 255
        n6 = edge.item(i-1,j) == 255
        n7 = edge.item(i-1,j+1) == 255
        if edge.item(i,j) == 255 and ((not n0 and(n4 and (n5 or n6 or n2 or n3) and (n6 or not n1) and (n2 or not n1)))
            or (not n4 and (n0 and (n1 or n2 or n6 or n1) and (n2 or not n3) and (n6 or not n5)))
            or (not n2 and (n5 and (n1 or n0 or n4 or n5) and (n0 or not n1) and (n4 or not n3)))
            or (not n6 and (n2 and (n3 or n4 or n0 or n1) and (n4 or not n5) and (n0 or not n1)))):
            edge_out.itemset(i,j,0)
for i in range(1,edge.shape[0]-1):
    for j in range(1,edge.shape[1]-1):
        n0 = edge.item(i,j+1) == 255
        n1 = edge.item(i+1,j+1) == 255
        n2 = edge.item(i+1,j) == 255
        n3 = edge.item(i+1,j-1) == 255
        n4 = edge.item(i,j-1) == 255
        n5 = edge.item(i-1,j-1) == 255
        n6 = edge.item(i-1,j) == 255
        n7 = edge.item(i-1,j+1) == 255
        if edge.item(i,j) == 255 and ((not n0 and(n4 and (n5 or n6 or n2 or n3) and (n6 or not n1) and (n2 or not n1)))
            or (not n4 and (n0 and (n1 or n2 or n6 or n1) and (n2 or not n3) and (n6 or not n5)))
            or (not n2 and (n5 and (n1 or n0 or n4 or n5) and (n0 or not n1) and (n4 or not n3)))
            or (not n6 and (n2 and (n3 or n4 or n0 or n1) and (n4 or not n5) and (n0 or not n1)))):
            edge_out.itemset(i,j,0)

def Edgechange(i,j):
    if i >= edge_out.shape[0]-1 or i < 0 or j >= edge_out.shape[1]-1 or j < 0:
        return 1
    count = 0
    if edge_out.item(i-1,j) == 255 and edge_out.item(i-1,j+1) == 0:
        count +=1
    if edge_out.item(i-1,j+1) == 255 and edge_out.item(i,j+1) == 0:
        count +=1
    if edge_out.item(i,j+1) == 255 and edge_out.item(i+1,j+1) == 0:
        count +=1
    if edge_out.item(i+1,j+1) == 255 and edge_out.item(i+1,j) == 0:
        count +=1
    if edge_out.item(i+1,j) == 255 and edge_out.item(i+1,j-1) == 0:
        count +=1
    if edge_out.item(i+1,j-1) == 255 and edge_out.item(i,j-1) == 0:
        count +=1
    if edge_out.item(i,j-1) == 255 and edge_out.item(i-1,j-1) == 0:
        count +=1
    if edge_out.item(i-1,j-1) == 255 and edge_out.item(i-1,j) == 0:
        count +=1
    return count

Q = queue.Queue()
for i in range(1,edge_out.shape[0]-1):
    for j in range(1,edge_out.shape[1]-1):
        c = Edgechange(i,j)
        if c == 1 or c >=3:
            if edge_out.item(i-1,j) == 255:
                Q.put((i,j,6))
            if edge_out.item(i-1,j+1) == 255:
                Q.put((i,j,7))
            if edge_out.item(i,j+1) == 255:
                Q.put((i,j,0))
            if edge_out.item(i+1,j+1) == 255:
                Q.put((i,j,1))
            if edge_out.item(i+1,j) == 255:
                Q.put((i,j,2))
            if edge_out.item(i+1,j-1) == 255:
                Q.put((i,j,3))
            if edge_out.item(i,j-1) == 255:
                Q.put((i,j,4))
            if edge_out.item(i-1,j-1) == 255:
                Q.put((i,j,5))

visited = np.zeros((edge_out.shape[0],edge_out.shape[1]))
n = 0 # the number of edge segement
segments = []
while not Q.empty():
    y, x, pos = Q.get()
    cy = DIRECTION[pos][0] + y
    cx = DIRECTION[pos][1] + x
    if visited.item(cy,cx) == 255:
        continue
    segment = []
    n += 1
    segment.append((y,x))
    segment.append((cy,cx))
    visited.itemset(y,x,255)
    visited.itemset(cy,cx,255)
    if Edgechange(cy,cx) == 1 or Edgechange(cy,cx) >= 3:
        continue
    exitcode = 0
    while exitcode == 0:
        temp = pos
        for ny,nx in FORWARD[temp]:
            ny += cy
            nx += cx
            if Edgechange(ny,nx) == 1 or Edgechange(ny,nx) >= 3:
                segment.append((ny,nx))
                visited.itemset(ny,nx,255)
                exitcode = 1
                break
            else:
                if edge_out.item(ny,nx) == 255:
                    segment.append((ny,nx))
                    visited.itemset(ny,nx,255)
                    for newpos in range(8):
                        py, px = DIRECTION[newpos]
                        if nx-cx == px and ny-cy == py:
                            pos = newpos
                    cx = nx
                    cy = ny
                else:
                    exitcode = 1
    segments.append(segment)

for seg in segments:
    print(seg)

# new_img = np.zeros((edge_out.shape[0],edge_out.shape[1],3),dtype=np.uint8)

# for seg in segments:
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     for y,x in seg:
#         new_img.itemset(y,x,0,b)
#         new_img.itemset(y,x,1,g)
#         new_img.itemset(y,x,2,r)

# cv.imshow('img',new_img)
# cv.imshow('edge',edge_out)
# cv.waitKey(0)
# cv.destroyAllWindows()