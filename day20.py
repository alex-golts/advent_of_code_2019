import collections
import numpy as np
from time import time

f = open('input20.txt','r')
txt = f.read()
txt = txt.split('\n')
maze = txt[:-1]

def find_open_space_next_to_gate(maze, gate):
    res = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == gate[0]:
                if j<len(maze[0])-1 and maze[i][j+1] == gate[1]:
                    if maze[i][j-1] == '.':
                        res.append([(i, j-1), 'left'])
                    elif j<len(maze[0])-2 and maze[i][j+2] == '.':
                        res.append([(i, j+2), 'right'])
                if i<len(maze)-1 and maze[i+1][j] == gate[1]:
                    if maze[i-1][j] == '.':
                        res.append([(i-1, j), 'up'])
                    elif i<len(maze)-2 and maze[i+2][j] == '.':
                        res.append([(i+2, j), 'down'])
    return res

     
def walkable_directions(maze, pos, current_direction):
    res = []
    if current_direction.lower() != 'left' and pos[1]<len(maze[0])-1 and maze[pos[0]][pos[1]+1] == '.':
        res.append('right')
    if current_direction.lower() != 'up' and pos[0]<len(maze)-1 and maze[pos[0]+1][pos[1]] == '.':
        res.append('down')
    if current_direction.lower() != 'right' and pos[1]>0 and maze[pos[0]][pos[1]-1] == '.':
        res.append('left')
    if current_direction.lower() != 'down' and pos[0]>0 and maze[pos[0]-1][pos[1]] == '.':
        res.append('up')
    return res

def is_intersection(maze, pos, direction):
    if len(walkable_directions(maze, pos, direction)) > 1:
        return True
    return False


def is_next_to_gate(maze, pos):
    if pos[1]<len(maze[0])-2 and maze[pos[0]][pos[1]+1].isalpha() and maze[pos[0]][pos[1]+1].isalpha():
        return maze[pos[0]][pos[1]+1] + maze[pos[0]][pos[1]+2]
    elif pos[1]>1 and maze[pos[0]][pos[1]-1].isalpha() and maze[pos[0]][pos[1]-2].isalpha():
        return maze[pos[0]][pos[1]-2] + maze[pos[0]][pos[1]-1]
    elif pos[0]<len(maze)-2 and maze[pos[0]+1][pos[1]].isalpha() and maze[pos[0]+2][pos[1]].isalpha():
        return maze[pos[0]+1][pos[1]] + maze[pos[0]+2][pos[1]]
    elif pos[0]>1 and maze[pos[0]-1][pos[1]].isalpha() and maze[pos[0]-2][pos[1]].isalpha():
        return maze[pos[0]-2][pos[1]] + maze[pos[0]-1][pos[1]]
    else:
        return []

    
def direction2char(direction):
    if direction.lower() == 'up':
        return '^'
    elif direction.lower() == 'down':
        return 'v'
    elif direction.lower() == 'left':
        return '<'
    elif direction.lower() == 'right':
        return '>'
    
def draw(maze, pos, direction):
    maze2 = maze.copy()
    maze2 = [[c for c in maze2[i]] for i in range(len(maze2))]

    maze2[pos[0]][pos[1]] = direction2char(direction)
    s = ''
    for i in range(len(maze2)):
        print(s.join(maze2[i]))
    
def move_in_direction(pos, direction):
    if direction.lower() == 'left':
        return (pos[0], pos[1]-1)
    elif direction.lower() == 'right':
        return (pos[0], pos[1]+1)
    elif direction.lower() == 'up':
        return (pos[0]-1, pos[1])
    elif direction.lower() == 'down':
        return (pos[0]+1, pos[1])
    
def teleport(pos, gate):
    res = find_open_space_next_to_gate(maze, gate)
    if pos == res[0][0]:
        pos = res[1][0]
        direction = res[1][1]
    else:
        pos = res[0][0]
        direction = res[0][1]
    return pos, direction

def unfinished_paths(paths):
    # a finished path is a list of positions 
    # and a final -1 list element
    inds = []
    for i, p in enumerate(paths):
        if p[-1]!=-1:
            inds.append(i)
    return inds

def calc_paths(maze, pos, direction, plot):
    paths = []
    # start the first path to explore
    cur_path = [pos]
    directions = [direction]
    paths.append(cur_path)
    # when a path is done exploring, a -1 is appended.
    # do the following while there are open paths left:
    while len(unfinished_paths(paths)) > 0:
        inds = unfinished_paths(paths)
        cur_path = paths[inds[0]]
        cur_direction = directions[inds[0]]
        cur_pos = cur_path[-1]
        if is_next_to_gate(maze, cur_pos) == 'ZZ':
            cur_path.append(-1)
            continue
        gate = is_next_to_gate(maze, cur_pos)
        if len(gate)>0 and gate not in ('AA', 'ZZ'):
            cur_pos, cur_direction = teleport(cur_pos, gate)
            cur_path.append(cur_pos)
            directions[inds[0]] = cur_direction
        if is_intersection(maze, cur_pos, cur_direction):
            dirs = walkable_directions(maze, cur_pos, cur_direction)
            cur_path_tmp = cur_path.copy()
            for i, d in enumerate(dirs):
                new_pos = move_in_direction(cur_pos, d)
                if plot:
                    draw(maze, new_pos, d)
                if i==0:
                    cur_path.append(new_pos)
                    directions[inds[0]] = d
                else:
                    cur_path_tmp2 = cur_path_tmp.copy()
                    cur_path_tmp2.append(new_pos)
                    paths.append(cur_path_tmp2)
                    directions.append(d)
        else:
            d = walkable_directions(maze, cur_pos, cur_direction)
            if len(d)==0: # dead end
                paths.pop(inds[0])
                directions.pop(inds[0])
                continue
            else:
                d = d[0]
            cur_pos = move_in_direction(cur_pos, d)
            if plot:
                draw(maze, cur_pos, cur_direction)
            cur_path.append(cur_pos)
            directions[inds[0]] = d
        # check current path for duplicate locations. 
        # if there are, it means this path is too long/not relevant
        dups = [item for item, count in collections.Counter(cur_path).items() if count > 1]
        if len(dups)>0:
            paths.pop(inds[0])
            directions.pop(inds[0])
    
    # finally return the found paths and remove the -1's at the end 
    return [p[:-1] for p in paths]
        

# part 2:
def is_outer_gate(maze, pos):
    gate = is_next_to_gate(maze, pos)
    if len(gate)==0:
        return None
    if pos[0]==2 or pos[1]==2 or pos[0]==len(maze[0])-3 or pos[1]==len(maze[0])-3 or pos[0]==len(maze)-3 or pos[1]==len(maze)-3:
        return True
    return False


def teleport_rec(maze, pos, gate, level):
    res = find_open_space_next_to_gate(maze, gate)
    if is_outer_gate(maze, pos):
        level = level-1
    else:
        level = level+1
    if pos == res[0][0]:
        pos = res[1][0]
        direction = res[1][1]
    else:
        pos = res[0][0]
        direction = res[0][1]
    return pos, direction, level
    
def find_item(lst, item):
    return [i for (i,v) in enumerate(lst) if v==item]

def unfinished_paths_sort_by_level(paths, levels):
    inds = []
    for i, p in enumerate(paths):
        if p[-1]!=-1:
            inds.append(i)
    max_levels = [np.max(item) for item in levels]
    good_max_levels = [max_levels[i] for i in inds]
    inds2 = np.argsort(good_max_levels)
    
    return [inds[i] for i in inds2]

def walkable_directions_2(maze, pos):
    res = []
    if pos[1]<len(maze[0])-1 and maze[pos[0]][pos[1]+1] == '.':
        res.append('right')
    if pos[0]<len(maze)-1 and maze[pos[0]+1][pos[1]] == '.':
        res.append('down')
    if pos[1]>0 and maze[pos[0]][pos[1]-1] == '.':
        res.append('left')
    if pos[0]>0 and maze[pos[0]-1][pos[1]] == '.':
        res.append('up')
    return res

def dead_end(maze, pos):
    cnt_walls = 0
    
    if maze[pos[0]][pos[1]] != '.':
        return False
    if maze[pos[0]][pos[1]+1] == '#':
        cnt_walls += 1
    if maze[pos[0]][pos[1]-1] == '#':
        cnt_walls += 1
    if maze[pos[0]+1][pos[1]] == '#':
        cnt_walls += 1
    if maze[pos[0]-1][pos[1]] == '#':
        cnt_walls += 1
    
    if cnt_walls == 3:
        return True
    else:
        return False
            
    
def remove_dead_ends(maze):
    num_dead_ends = 100 # init
    cnt=0
    while num_dead_ends>0:
        for i in range(1, len(maze)-1):
            for j in range(1, len(maze[0])-1):
                if dead_end(maze,(i,j)):
                    cnt+=1
                    maze[i][j] = '#'
        num_dead_ends = cnt
        cnt=0
    return maze

def isSublist(a, b):
    if len(a) > len(b):
        return False
    for i in range(0, len(b) - len(a) + 1):
        if b[i:i+len(a)] == a:
            return True
    return False

def calc_paths_rec(maze, pos, direction, plot):
    # this works but keeps track of whole paths, and is too slow...
    paths = []
    # start the first path to explore
    cur_path = [pos]
    level = 0
    directions = [direction]
    paths.append(cur_path)
    levels = []
    cur_level = [level]
    levels.append(cur_level)
    gate_lists = [['AA']]
    level_switch_lists = []
    # when a path is done exploring, a -1 is appended.
    # do the following while there are open paths left:
    while len(unfinished_paths(paths)) > 0:
        inds = unfinished_paths(paths)
        cur_path = paths[inds[0]]
        cur_direction = directions[inds[0]]
        cur_level = levels[inds[0]]
        cur_pos = cur_path[-1]
        if is_next_to_gate(maze, cur_pos) == 'ZZ' and cur_level[-1]==0:
            cur_path.append(-1)
            continue
        gate = is_next_to_gate(maze, cur_pos)
        if len(gate)>0 and gate not in ('AA', 'ZZ') and not (is_outer_gate(maze, cur_pos) and cur_level[-1]==0):
            cur_pos, cur_direction, level = teleport_rec(maze, cur_pos, gate, cur_level[-1])
            cur_path.append(cur_pos)
            cur_level.append(level)
            directions[inds[0]] = cur_direction
        if is_intersection(maze, cur_pos, cur_direction):
            dirs = walkable_directions(maze, cur_pos, cur_direction)
            cur_path_tmp = cur_path.copy()
            cur_level_tmp = cur_level.copy()
            for i, d in enumerate(dirs):
                new_pos = move_in_direction(cur_pos, d)
                if plot:
                    draw(maze, new_pos, d)
                if i==0:
                    cur_path.append(new_pos)
                    cur_level.append(cur_level[-1])
                    directions[inds[0]] = d
                else:
                    cur_path_tmp2 = cur_path_tmp.copy()
                    cur_path_tmp2.append(new_pos)
                    cur_level_tmp2 = cur_level_tmp.copy()
                    cur_level_tmp2.append(cur_level[-1])
                    paths.append(cur_path_tmp2)
                    levels.append(cur_level_tmp2)
                    directions.append(d)
        else:
            d = walkable_directions(maze, cur_pos, cur_direction)
            if len(d)==0: # dead end
                paths.pop(inds[0])
                directions.pop(inds[0])
                levels.pop(inds[0])
                continue
            else:
                d = d[0]
            cur_pos = move_in_direction(cur_pos, d)
            if plot:
                draw(maze, cur_pos, d)
            cur_level.append(cur_level[-1])
            cur_path.append(cur_pos)
            directions[inds[0]] = d
        # check current path for duplicate locations. 
        # if there are, it means this path is too long/not relevant
        try:
            dup_index = cur_path[:-1].index(cur_path[-1])
        except:
            dup_index = None
        if (dup_index is not None and cur_level[-1]==cur_level[dup_index]) or len(cur_path)>=10000 or cur_level[-1]>150:
            paths.pop(inds[0])
            directions.pop(inds[0])
            levels.pop(inds[0])
        
        num_finished = len([p for p in paths if p[-1]==-1])
        print(f'finished_paths: {num_finished}')
        print(f'num paths: {len(paths)}')

    # finally return the found paths and remove the -1's at the end 
    return [p[:-1] for p in paths], levels
    
def unfinished_pos(positions, path_lengths):
    # return indices of unfinished paths, sorted from lowest path length
    inds = [i for (i,p) in enumerate(positions) if p!=-1]
    good_path_lengths = [path_lengths[i] for i in inds]
    inds2 = np.argsort(good_path_lengths)
    
    return [inds[i] for i in inds2]


def remove_indices_from_list(lst, remove_indices):
    lst_res =  [i for j, i in enumerate(lst) if j not in remove_indices]
    return lst_res

def calc_paths_rec_2(maze, pos, direction, plot):
    # for memory efficiency, I don't keep track of the whole paths
    # but rather only the last position, direction, path length and level
    level = 0
    directions = [direction]
    positions = [pos]
    levels = [level]
    path_lengths = [0]
    # when a path is done exploring, a -1 is appended.
    # do the following while there are open paths left:
    cnt=0
    while len(unfinished_pos(positions, path_lengths)) > 0:
        inds = unfinished_pos(positions, path_lengths)
        cur_pos = positions[inds[0]]
        cur_direction = directions[inds[0]]
        cur_level = levels[inds[0]]
        if is_next_to_gate(maze, cur_pos) == 'ZZ' and cur_level==0:
            cur_pos = -1
            positions[inds[0]] = -1
            return path_lengths[inds[0]]
            # this is when the function ends. if a path is found, it
            # should be the shortest since I always explore paths with the 
            # shortest length first
        gate = is_next_to_gate(maze, cur_pos)
        if len(gate)>0 and gate not in ('AA', 'ZZ') and not (is_outer_gate(maze, cur_pos) and cur_level==0):
            cur_pos, cur_direction, cur_level = teleport_rec(maze, cur_pos, gate, cur_level)
            positions[inds[0]] = cur_pos
            path_lengths[inds[0]]+=1
            levels[inds[0]] = cur_level
            directions[inds[0]] = cur_direction
        if is_intersection(maze, cur_pos, cur_direction):
            dirs = walkable_directions(maze, cur_pos, cur_direction)
            cur_pos_tmp = cur_pos
            cur_level_tmp = cur_level
            for i, d in enumerate(dirs):
                new_pos = move_in_direction(cur_pos, d)
                if plot:
                    draw(maze, new_pos, d)
                if i==0:
                    positions[inds[0]] = new_pos
                    path_lengths[inds[0]]+=1
                    levels[inds[0]] = cur_level
                    directions[inds[0]] = d
                else:
                    positions.append(new_pos)
                    path_lengths.append(path_lengths[inds[0]])
                    levels.append(cur_level)
                    directions.append(d)
        else:
            d = walkable_directions(maze, cur_pos, cur_direction)
            if len(d)==0: # dead end
                positions.pop(inds[0])
                path_lengths.pop(inds[0])
                directions.pop(inds[0])
                levels.pop(inds[0])
                continue
            else:
                d = d[0]
            cur_pos = move_in_direction(cur_pos, d)
            if plot:
                draw(maze, cur_pos, d)
            levels[inds[0]] = cur_level
            positions[inds[0]] = cur_pos
            path_lengths[inds[0]]+=1
            directions[inds[0]] = d
        
        # remove paths with length greater than 10000 
        # found by guessing. kinda cheating a little but fuck it
        remove_indices = [i for (i,j) in enumerate(path_lengths) if j>=10000]
        positions = remove_indices_from_list(positions, remove_indices)
        path_lengths = remove_indices_from_list(path_lengths, remove_indices)
        directions = remove_indices_from_list(directions, remove_indices)
        levels = remove_indices_from_list(levels, remove_indices)
        
        # remove levels greater than 150. kinda conservatively guessed that.
        # not sure how critical this is...
        remove_indices = [i for (i,j) in enumerate(levels) if j>=150]
        positions = remove_indices_from_list(positions, remove_indices)
        path_lengths = remove_indices_from_list(path_lengths, remove_indices)
        directions = remove_indices_from_list(directions, remove_indices)
        levels = remove_indices_from_list(levels, remove_indices)

        # remove paths that for some reason are complete duplicates 
        # same level, position, direction and length
        common_list = list(zip(positions, path_lengths, directions, levels))
        common_list = list(set(common_list))
        positions, path_lengths, directions, levels = list(zip(*common_list))
        positions = list(positions)
        path_lengths = list(path_lengths)
        directions = list(directions)
        levels = list(levels)
        
        num_finished = len([p for p in positions if p==-1])

        cnt+=1

        print(f'steps: {cnt}')
        print(f'finished_paths: {num_finished}')
        print(f'num paths: {len(positions)}')
            

# examples:
if False:
    maze = [\
    '         A           ',
    '         A           ',
    '  #######.#########  ',
    '  #######.........#  ',
    '  #######.#######.#  ',
    '  #######.#######.#  ',
    '  #######.#######.#  ',
    '  #####  B    ###.#  ',
    'BC...##  C    ###.#  ',
    '  ##.##       ###.#  ',
    '  ##...DE  F  ###.#  ',
    '  #####    G  ###.#  ',
    '  #########.#####.#  ',
    'DE..#######...###.#  ',
    '  #.#########.###.#  ',
    'FG..#########.....#  ',
    '  ###########.#####  ',
    '             Z       ',
    '             Z       ']
        
if False:
    maze = [\
'                   A               ',    
'                   A               ',
'  #################.#############  ',
'  #.#...#...................#.#.#  ',
'  #.#.#.###.###.###.#########.#.#  ',
'  #.#.#.......#...#.....#.#.#...#  ',
'  #.#########.###.#####.#.#.###.#  ',
'  #.............#.#.....#.......#  ',
'  ###.###########.###.#####.#.#.#  ',
'  #.....#        A   C    #.#.#.#  ',
'  #######        S   P    #####.#  ',
'  #.#...#                 #......VT',
'  #.#.#.#                 #.#####  ',
'  #...#.#               YN....#.#  ',
'  #.###.#                 #####.#  ',
'DI....#.#                 #.....#  ',
'  #####.#                 #.###.#  ',
'ZZ......#               QG....#..AS',
'  ###.###                 #######  ',
'JO..#.#.#                 #.....#  ',
'  #.#.#.#                 ###.#.#  ',
'  #...#..DI             BU....#..LF',
'  #####.#                 #.#####  ',
'YN......#               VT..#....QG',
'  #.###.#                 #.###.#  ',
'  #.#...#                 #.....#  ',
'  ###.###    J L     J    #.#.###  ',
'  #.....#    O F     P    #.#...#  ',
'  #.###.#####.#.#####.#####.###.#  ',
'  #...#.#.#...#.....#.....#.#...#  ',
'  #.#####.###.###.#.#.#########.#  ',
'  #...#.#.....#...#.#.#.#.....#.#  ',
'  #.###.#####.###.###.#.#.#######  ',
'  #.#.........#...#.............#  ',
'  #########.###.###.#############  ',
'           B   J   C               ',
'           U   P   P               ']
        
start = find_open_space_next_to_gate(maze, 'AA')[0]

paths = calc_paths(maze, start[0], start[1], plot=False)
path_lengths = [len(item)-1 for item in paths]

print(f'part 1 answer = {min(path_lengths)}')

# part 2:

# example:

if False:
    
    maze = [\
'             Z L X W       C                 ',
'             Z P Q B       K                 ',
'  ###########.#.#.#.#######.###############  ',
'  #...#.......#.#.......#.#.......#.#.#...#  ',
'  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  ',
'  #.#...#.#.#...#.#.#...#...#...#.#.......#  ',
'  #.###.#######.###.###.#.###.###.#.#######  ',
'  #...#.......#.#...#...#.............#...#  ',
'  #.#########.#######.#.#######.#######.###  ',
'  #...#.#    F       R I       Z    #.#.#.#  ',
'  #.###.#    D       E C       H    #.#.#.#  ',
'  #.#...#                           #...#.#  ',
'  #.###.#                           #.###.#  ',
'  #.#....OA                       WB..#.#..ZH',
'  #.###.#                           #.#.#.#  ',
'CJ......#                           #.....#  ',
'  #######                           #######  ',
'  #.#....CK                         #......IC',
'  #.###.#                           #.###.#  ',
'  #.....#                           #...#.#  ',
'  ###.###                           #.#.#.#  ',
'XF....#.#                         RF..#.#.#  ',
'  #####.#                           #######  ',
'  #......CJ                       NM..#...#  ',
'  ###.#.#                           #.###.#  ',
'RE....#.#                           #......RF',
'  ###.###        X   X       L      #.#.#.#  ',
'  #.....#        F   Q       P      #.#.#.#  ',
'  ###.###########.###.#######.#########.###  ',
'  #.....#...#.....#.......#...#.....#.#...#  ',
'  #####.#.###.#######.#######.###.###.#.#.#  ',
'  #.......#.......#.#.#.#.#...#...#...#.#.#  ',
'  #####.###.#####.#.#.#.#.###.###.#.###.###  ',
'  #.......#.....#.#...#...............#...#  ',
'  #############.#.#.###.###################  ',
'               A O F   N                     ',
'               A A D   M                     ']

# remove dead ends - should improve speed:
maze = [[c for c in maze[i]] for i in range(len(maze))]        
maze = remove_dead_ends(maze)
maze = [''.join(item) for item in maze]

start = find_open_space_next_to_gate(maze, 'AA')[0]      

# this is slow. takes about 1 hour on the actual input. could be improved probably...
min_path = calc_paths_rec(maze, start[0], start[1], plot=False)

print(f'part 2 answer = {min_path}')
