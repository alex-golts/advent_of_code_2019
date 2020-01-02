import numpy as np
import math

f = open('input10.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]


rows = len(txt)
cols = len(txt[0])

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def is_point_on_line(p, line):
    # line - given by [a, b] where y=a*x+b
    if np.isinf(line[0]): 
        if p[1]==line[1]:
            return True
        else:
            return False
    
    if math.isclose(p[0], (line[0]*p[1] + line[1])):
        return True
    else:
        return False
    
    
def is_visible(p1, p2, points):
    points_tmp = points.copy()
    # returns whether p2 is visible from p1
    dist = euclidean_distance(p1, p2)
    ang = math.atan2(p2[0]-p1[0], p2[1]-p1[1])
    if p1[1]!=p2[1]:
        a = (p2[0] - p1[0]) / (p2[1] - p1[1])
        b = p1[0] - a*p1[1]
    else:
        a = np.inf
        b = p1[1]
        
    line = [a, b]
    # remove p1 and p2 from points:
    points_tmp.remove(p1)
    points_tmp.remove(p2)
    # find points that lie on the same line:
    for p in points_tmp:
        if is_point_on_line(p, line):
            # check for minimal distance and same view direction
            if dist > euclidean_distance(p1, p) and math.isclose(ang, math.atan2(p[0]-p1[0],p[1]-p1[1])):
                return False
    return True

points = []
for r in range(rows):
    for c in range(cols):
        if txt[r][c] == '#':
            points.append((r,c))

# matrix denoting visibility from each point to other points:
visibility_mat = np.zeros((len(points), len(points)))
for r in range(len(points)):
    for c in range(len(points)):
        if r==c:
            continue
        visibility_mat[r,c] = is_visible(points[r], points[c], points)

best_idx = np.argmax(np.sum(visibility_mat,0))
best_num_visible = int(np.max(np.sum(visibility_mat,0)))
best_point = points[best_idx]
print('Part 1 answer:')
print('best location = ' + str(best_point))        
print('# of points visible = ' + str(best_num_visible))
