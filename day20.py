import collections

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