from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from copy import deepcopy
import numpy as np

f = open('input18.txt','r')
txt = f.read()
txt = txt.split('\n')
maze = txt[:-1]

# turn strings to list of chars (so that they can be changed)
maze = [[c for c in maze[i]] for i in range(len(maze))]

def direction2char(direction):
    if direction.lower() == 'up':
        return '^'
    elif direction.lower() == 'down':
        return 'v'
    elif direction.lower() == 'left':
        return '<'
    elif direction.lower() == 'right':
        return '>'
    
def draw(maze, pos, direction=None):
    maze2 = maze.copy()
    maze2 = [[c for c in maze2[i]] for i in range(len(maze2))]

    if direction is not None:
        maze2[pos[0]][pos[1]] = direction2char(direction)
    s = ''
    for i in range(len(maze2)):
        print(s.join(maze2[i]))
        
def getStartPos(maze):
    res = []
    symbols = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in ('@', '!', '$', '%'):
                res.append((i, j))
                symbols.append(maze[i][j])
    return res, symbols

def countKeys(maze):
    cnt = 0
    keys = []
    key_positions = []
    doors = []
    door_positions = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j].islower() or maze[i][j] in ('@', '!', '$', '%'):
                cnt+=1
                keys.append(maze[i][j])
                key_positions.append((i, j))
            if maze[i][j].isupper():
                doors.append(maze[i][j])
                door_positions.append((i, j))
                
    return cnt, keys, key_positions, doors, door_positions

def maze2bin(maze, collected_keys):
    bin_maze = [[0 for j in range(len(maze[0]))] for i in range(len(maze))]
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#' or (maze[i][j].isalpha() and maze[i][j].lower() not in collected_keys) or (maze[i][j] in ('!', '@', '$', '%') and maze[i][j] not in collected_keys):
                bin_maze[i][j] = 0
            elif maze[i][j] == '.' or (maze[i][j].isalpha() and maze[i][j].lower() in collected_keys) or (maze[i][j] in ('!', '@', '$', '%') and maze[i][j] in collected_keys):
                bin_maze[i][j] = 1
    return bin_maze

def unfinished_paths(keys_collected, num_keys, path_lengths):
    inds = [i for (i,j) in enumerate(keys_collected) if len(j)<num_keys]
    return inds

def remove_indices_from_list(lst, remove_indices):
    lst_res =  [i for j, i in enumerate(lst) if j not in remove_indices]
    return lst_res

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

def keys_on_path(path):
    res = []
    for p in path[1:-1]:
        if p in key_positions:
            res.append(all_keys[key_positions.index(p)])
        if p in door_positions:
            res.append(all_doors[door_positions.index(p)].lower())
    return res


def calc_dist_mat(maze):
    dist_mat = {}
    middle_keys = {}
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    for i,k1 in enumerate(all_keys):
        for j,k2 in enumerate(all_keys):
            if k1==k2 or frozenset((k1,k2)) in dist_mat:
                continue
            start_pos = key_positions[all_keys.index(k1)]
            end_pos = key_positions[all_keys.index(k2)]
            bin_maze = maze2bin(maze, all_keys)
            bin_maze[end_pos[0]][end_pos[1]] = 1
            grid = Grid(matrix=bin_maze)
            start = grid.node(start_pos[1], start_pos[0])
            end = grid.node(end_pos[1], end_pos[0])
            path, runs = finder.find_path(start, end, grid)
            path = [p[::-1] for p in path]
            path_len = len(path)-1
            middle_keys[frozenset((k1,k2))] = frozenset(keys_on_path(path))
            dist_mat[frozenset((k1,k2))] = path_len if path_len>0 else np.inf
    return dist_mat, middle_keys
            
def reachable_from(key, collected_keys):
    res = []
    for k in frozenset(all_keys)-frozenset(('!', '@', '$', '%')):
        if k==key:
            continue
        if np.isnan(dist_mat[frozenset((key,k))]) or dist_mat[frozenset((key,k))]==np.inf or dist_mat[frozenset((key,k))]<=0:
            continue
        mid_keys = middle_keys[frozenset((key, k))] - frozenset(('!', '@', '$', '%'))
        if mid_keys.issubset(frozenset(collected_keys)):
            res.append(k)
    return res

def reachable_from_robots(key_tup, collected_keys):
    res = []
    for k in frozenset(all_keys)-frozenset(('!', '@', '$', '%'))-frozenset(collected_keys):
        for i,key in enumerate(key_tup):
            if k == key:
                continue
            if np.isnan(dist_mat[frozenset((key,k))]) or dist_mat[frozenset((key,k))]==np.inf or dist_mat[frozenset((key,k))]<=0:
                continue
            mid_keys = middle_keys[frozenset((key, k))] - frozenset(('!', '@', '$', '%'))
            if mid_keys.issubset(frozenset(collected_keys)):
                res.append((i, k))
    return res
    
def calc_shortest_path(maze, pos, memo=True):
    cur_pos = pos
    positions = [cur_pos]
    path_lengths = [0]
    keys_collected = [['@']]
    start_key = '@'
    cnt=0
    while len(unfinished_paths(keys_collected, num_keys, path_lengths)) > 0:
        inds = unfinished_paths(keys_collected, num_keys, path_lengths)
        start_pos = positions[inds[0]]
        start_key = '@' if cnt==0 else all_keys[key_positions.index(start_pos)]
        cnt_visible_keys = 0
        cur_keys = deepcopy(keys_collected[inds[0]])
        cur_path_len = path_lengths[inds[0]]
        for k in frozenset(reachable_from(start_key, cur_keys))-frozenset(keys_collected[inds[0]]):
            end_pos = key_positions[all_keys.index(k)]
            path_len = dist_mat.get((frozenset((start_key, k))))
            if cnt_visible_keys == 0 and path_len>0:
                keys_collected[inds[0]].append(k)
                path_lengths[inds[0]] += path_len
                positions[inds[0]] = end_pos
                cnt_visible_keys += 1
            elif path_len>0:
                keys_collected.append(cur_keys + [k])
                path_lengths.append(cur_path_len + path_len)
                positions.append(end_pos)
        if path_len<=0 and cnt_visible_keys == 0:
            positions.pop(inds[0])
            keys_collected.pop(inds[0])
            path_lengths.pop(inds[0])
        cnt +=1
        num_finished = len([k for k in keys_collected if len(k)==num_keys])
        if num_finished>0:
        #     t1=time()
            inds_finished = [i for i,k in enumerate(keys_collected) if len(k)==num_keys]
            lens_finished = [path_lengths[i] for i in inds_finished]
            min_len_finished = min(lens_finished)
            print(f'shortest path so far: {min_len_finished}')
        
    return path_lengths, keys_collected
            

def distanceToCollectKeys(currentKey, keys, cache): 

    if len(keys)==0:
        return 0
    
    cacheKey = (currentKey, keys)
    if cacheKey in cache:
        return cache[cacheKey]
    
    result = np.inf
    keys_collected = frozenset(all_keys)-keys
    for key in frozenset(reachable_from(currentKey, keys_collected-frozenset(('@',)))) - keys_collected:
       d = dist_mat[frozenset((currentKey, key))] + distanceToCollectKeys(key, keys - frozenset((key,)), cache)
       result = min(result, d)

    cache[cacheKey] = result
    return result


def distanceToCollectKeys_robots(currentKey, keys, cache): 
    # modify recursive function to account for the four robots.
    # here, currentKey is a tuple of four robot current keys
    if len(keys)==0:
        return 0
    
    cacheKey = (currentKey, keys)
    if cacheKey in cache:
        return cache[cacheKey]
    
    result = np.inf
    keys_collected = frozenset(all_keys)-keys
    # reachable_from_robots returns a list of tuples (i, key) where i 
    # is the robot id - 0,1,2,3, and key is the key visible from it
    for key in frozenset(reachable_from_robots(currentKey, keys_collected-frozenset(('!', '@', '$', '%')))) - keys_collected:
       newCurrentKey = deepcopy(list(currentKey))
       newCurrentKey[key[0]] = key[1]
       newCurrentKey = tuple(newCurrentKey)
       d = dist_mat[frozenset((currentKey[key[0]], key[1]))] + distanceToCollectKeys_robots(newCurrentKey, keys - frozenset((key[1],)), cache)
       result = min(result, d)
    cache[cacheKey] = result
    return result
    

# remove dead ends - hopefully this saves some time:
maze = remove_dead_ends(maze)

# get start position
start_pos, _ = getStartPos(maze)
start_pos = start_pos[0]

# get all keys, doors and respective positions
num_keys, all_keys, key_positions, all_doors, door_positions = countKeys(maze)

# pre-calculate a shortest distance map between all pairs of keys
# and a list of all keys/doors in between.
# a KEY observation is that there is always only one path between 
# each pair of keys, no matter how many keys one has collected so far!
dist_mat, middle_keys = calc_dist_mat(maze)


# this is my best attemp before finally resorting to the solution here:
# https://www.reddit.com/r/adventofcode/comments/ec8090/2019_day_18_solutions/fbd8y0b/
# it does not scale well even though I used memoization. probably some other bug...

#path_lengths, keys_collected = calc_shortest_path(maze, start_pos, memo=True)
#print(f'part 1 answer = {min(path_lengths)}')

min_path = distanceToCollectKeys('@',frozenset(all_keys)-frozenset(('@',)), {})
print(f'part 1 answer = {min_path}')


# part 2:

# change maze - use 4 distinct start key symbols - !,@,$,%:
maze[start_pos[0]][start_pos[1]] = '#'
maze[start_pos[0]-1][start_pos[1]] = '#'
maze[start_pos[0]+1][start_pos[1]] = '#'
maze[start_pos[0]][start_pos[1]-1] = '#'
maze[start_pos[0]][start_pos[1]+1] = '#'
maze[start_pos[0]-1][start_pos[1]-1] = '!'
maze[start_pos[0]+1][start_pos[1]+1] = '@'
maze[start_pos[0]-1][start_pos[1]+1] = '$'
maze[start_pos[0]+1][start_pos[1]-1] = '%'

# recalculate start positions, keys, and distance mat:
start_pos, start_keys = getStartPos(maze)
num_keys, all_keys, key_positions, all_doors, door_positions = countKeys(maze)
dist_mat, middle_keys = calc_dist_mat(maze)

min_path = distanceToCollectKeys_robots(('!','@','$','%'), frozenset(all_keys)-frozenset(('!', '@', '$', '%')), {})

print(f'part 2 answer = {min_path}')