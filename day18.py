import random
random.seed(1)
from copy import deepcopy

f = open('tmp.txt','r')
txt = f.read()
txt = txt.split('\n')
maze = txt[:-1]
# turn strings to list of chars (so that they can be changed)
maze = [[c for c in maze[i]] for i in range(len(maze))]
# add row of '#'s on top
maze = [['#' for i in range(len(maze[0]))]]+ maze

def getStartPos(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '@':
                return (j, i)

def getKeyPos(maze, key):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == key:
                return (j, i)

def removeKey(maze, key):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j].lower()==key.lower():
                maze[i][j] = '.'
    return maze

def countKeys(maze):
    cnt = 0
    keys = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j].islower():
                cnt+=1
                keys.append(maze[i][j])
    return cnt, keys

def doorNearby(maze, pos):
    if maze[pos[1]][pos[0]-1].isupper():
        return maze[pos[1]][pos[0]-1], (pos[0]-1, pos[1])
    elif maze[pos[1]][pos[0]+1].isupper():
        return maze[pos[1]][pos[0]+1], (pos[0]+1, pos[1])
    elif maze[pos[1]-1][pos[0]].isupper():
        return maze[pos[1]-1][pos[0]], (pos[0], pos[1]-1)
    elif maze[pos[1]+1][pos[0]].isupper():
        return maze[pos[1]+1][pos[0]], (pos[0], pos[1]+1)
    else:
        return '', pos
    
def keyNearby(maze, pos):
    if maze[pos[1]][pos[0]-1].islower():
        return maze[pos[1]][pos[0]-1], (pos[0]-1, pos[1])
    elif maze[pos[1]][pos[0]+1].islower():
        return maze[pos[1]][pos[0]+1], (pos[0]+1, pos[1])
    elif maze[pos[1]-1][pos[0]].islower():
        return maze[pos[1]-1][pos[0]], (pos[0], pos[1]-1)
    elif maze[pos[1]+1][pos[0]].islower():
        return maze[pos[1]+1][pos[0]], (pos[0], pos[1]+1)
    else:
        return '', pos
    
def visibleKeys(maze, pos):
    if countKeys(maze)[0]==1:
        return countKeys(maze)[1]
    start_pos = pos
    cnt = 0
    keys = []    
    mazeOccupied = deepcopy(maze)
    # try wandering around until 2 visible items are found (doors or keys)
    while cnt<2:
        if len(doorNearby(mazeOccupied, pos)[0]):
            # replace found door position with occupied char, so that it doesn't get found again
            mazeOccupied[doorNearby(mazeOccupied, pos)[1][1]][doorNearby(mazeOccupied, pos)[1][0]] = '&'
            cnt+=1
        if len(keyNearby(mazeOccupied, pos)[0]):
            cnt+=1
            keys.append(keyNearby(mazeOccupied, pos)[0])
            # replace found key position with occupied char
            mazeOccupied[keyNearby(mazeOccupied, pos)[1][1]][keyNearby(mazeOccupied, pos)[1][0]] = '&'
        if cnt<2:
            #r = random.randint(1,4)
            #if r==1: # left
            if mazeOccupied[pos[1]][pos[0]-1] == '.':
                    pos = (pos[0]-1, pos[1])
            #elif r==2: # right
            elif mazeOccupied[pos[1]][pos[0]+1] == '.':
                    pos = (pos[0]+1, pos[1])
            #elif r==3: # up
            elif mazeOccupied[pos[1]-1][pos[0]] == '.':
                    pos = (pos[0], pos[1]-1)
            #elif r==4: # down
            elif mazeOccupied[pos[1]+1][pos[0]] == '.':
                    pos = (pos[0], pos[1]+1)
            else:
                pos = start_pos
    return keys


def getKey(maze, pos, key):
    success = False
    num_steps = 1
    start_pos = pos
    mazeOccupied = deepcopy(maze)
    while not success:
        if keyNearby(mazeOccupied, pos)[0] == key:
            #done = True
            success = True
            break
        mazeOccupied[pos[1]][pos[0]] = '&'
        if mazeOccupied[pos[1]][pos[0]-1] == '.':
            pos = (pos[0]-1, pos[1])
            num_steps+=1
        elif mazeOccupied[pos[1]][pos[0]+1] == '.':
            pos = (pos[0]+1, pos[1])
            num_steps+=1
        elif mazeOccupied[pos[1]-1][pos[0]] == '.':
            pos = (pos[0], pos[1]-1)
            num_steps+=1
        elif mazeOccupied[pos[1]+1][pos[0]] == '.':
            pos = (pos[0], pos[1]+1)
            num_steps += 1
        else:
            pos = start_pos
            num_steps = 1
    pos = keyNearby(maze, pos)[1]
    maze = removeKey(maze, key)
    return maze, num_steps, pos

# points are defined as (x,y) tuple
def countShortestPath(maze, pos):
    keys = visibleKeys(maze, pos)
    import pdb
    pdb.set_trace()
    if countKeys(maze)[0]==1:
        _, num_steps, _ = getKey(maze, pos, keys[0])
        return num_steps
    else:
        paths = []
        for key in keys:
            maze, num_steps, pos = getKey(maze, pos, key)
            paths.append(num_steps + countShortestPath(maze, pos))
        return min(paths)
            
start_pos = getStartPos(maze)
maze[start_pos[1]][start_pos[0]] = '.'
print('part 1 answer = ' + str(countShortestPath(maze, start_pos)))
