import numpy as np
import math

f = open('input10.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]


# txt = ['.#..##.###...#######',
#        '##.############..##.',
#        '.#.######.########.#',
#        '.###.#######.####.#.',
#        '#####.##.#.##.###.##',
#        '..#####..#.#########',
#        '####################',
#        '#.####....###.#.#.##',
#        '##.#################',
#        '#####.##.###..####..',
#        '..######..##.#######',
#        '####.##.####...##..#',
#        '.#####..#.######.###',
#        '##...#.##########...',
#        '#.##########.#######',
#        '.####.#.###.###.#.##',
#        '....##.##.###..#####',
#        '.#.#.###########.###',
#        '#.#.#.#####.####.###',
#        '###.##.####.##.#..##']

rows = len(txt)
cols = len(txt[0])

# Note: I use point = (row,col) or (y,x) convention

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

def calc_visibility_mat(points):
    # matrix denoting visibility from each point to other points:
    visibility_mat = np.zeros((len(points), len(points)))
    for r in range(len(points)):
        for c in range(len(points)):
            if r==c:
                continue
            visibility_mat[r,c] = is_visible(points[r], points[c], points)
    return visibility_mat

print('Part 1 - calculating visibility matrix (this takes a while...)')
visibility_mat = calc_visibility_mat(points)
best_idx = np.argmax(np.sum(visibility_mat,0))
best_num_visible = int(np.max(np.sum(visibility_mat,0)))
best_point = points[best_idx]
print('Part 1 answer:')
print('best location = ' + str(best_point))        
print('# of points visible = ' + str(best_num_visible))


# Part 2

start_point = best_point

def angle_to_point(start_point, p):
    # find the angle between the vector from start point
    # to point p, and an upward facing vector (1,0)
    p = np.array(p)
    sp = np.array(start_point)
    up = np.array((-1,0))
    sp_to_p = p - sp

    angle = (180/np.pi)*np.arccos(np.dot(up,sp_to_p)/(np.linalg.norm(up)*np.linalg.norm(sp_to_p)))
    if p[1]<start_point[1]:
        angle = 360-angle
    return angle
    
# remove start point from points:
points.remove(start_point)

# calculate all angles and ranges to different points
angles = []
ranges = []
for p in points:
    angles.append(angle_to_point(start_point, p))
    ranges.append(euclidean_distance(start_point, p))

ang_sort_inds = np.argsort(angles).tolist()
sorted_data = [[points[i], angles[i], ranges[i]] for i in ang_sort_inds]
sorted_data_updated = sorted_data.copy()

cnt = 1
while len(sorted_data_updated)>1:
    data_current = sorted_data_updated
    last_point = data_current[0][0]
    last_angle = data_current[0][1]
    min_dist = data_current[0][2]
    data_current = data_current[1:]
    for i,p in enumerate(data_current):
        if not math.isclose(data_current[i][1], last_angle):
            sorted_data_updated.remove([last_point, last_angle, min_dist])
            if cnt==200:
                print(f'the {cnt}th asteroid to be vaporized is at x={last_point[1]},y={last_point[0]}')
                print(f'part 2 answer = {last_point[1]*100+last_point[0]}')
            cnt+=1
            last_point = data_current[i][0]
            last_angle = data_current[i][1]
            min_dist = data_current[i][2]
            #ind_to_remove = i
        else:
            if data_current[i][2]<min_dist:
                last_point = data_current[i][0]
                last_angle = data_current[i][1]
                min_dist = data_current[i][2]

        
            
        