import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# intcode computer function - from Day 9 but modified 
# to account for droid movement 
def intcode_computer(input_val, program, maze, min_steps=0):
    halt = False
    foundOxygen = False
    cnt = 0
    output_vals = []
    relative_base = 0
    
    visited_mat = np.zeros_like(maze)
    visited_mat[0:2,:] = 1
    visited_mat[-2:,:] = 1
    visited_mat[:,0:2] = 1
    visited_mat[:,-2:] = 1
    start_pos = [22,22]
    visited_mat[start_pos[0], start_pos[1]] = 1
    end_pos = []
    cur_pos = start_pos.copy()
    steps = 0
    while halt == False:
        steps += 1
        optcode = program[cnt]
        if optcode%10 == 3:
            pointer_increase = 2
            # very naiive and slow way to build the maze but it works
            # just set input_val randomly:
            input_val = np.random.randint(1,5)
            if str(optcode).zfill(2)[0] == '2':
                program[program[cnt+1] + relative_base] = input_val
            else:
                program[program[cnt+1]] = input_val
            
        elif optcode%10 == 4:
            pointer_increase = 2
            if str(optcode).zfill(2)[0]=='1':
                # immediate mode
                output_vals.append(program[cnt+1])
            elif str(optcode).zfill(2)[0]=='0':
                # parameter mode
                output_vals.append(program[program[cnt+1]])
            elif str(optcode).zfill(2)[0]=='2': 
                # relative mode
                output_vals.append(program[program[cnt+1] + relative_base])
            else:
                print('bad mode ' + str(optcode).zfill(2)[0])
            
            # read output and set maze and cur_pos accordingly:
            if output_vals[-1] in (1, 2): # open location. move cur_pos
                if input_val == 1:
                    cur_pos[0]-=1
                elif input_val == 2:
                    cur_pos[0]+=1
                elif input_val == 3:
                    cur_pos[1]-=1
                elif input_val == 4:
                    cur_pos[1]+=1
                else:
                    print('bad input_val')
                    break
                visited_mat[cur_pos[0], cur_pos[1]] = 1
            elif output_vals[-1] == 0: # blocked location - put 1 in maze
                if input_val == 1:
                    maze[cur_pos[0]-1, cur_pos[1]] = 1
                    visited_mat[cur_pos[0]-1, cur_pos[1]] = 1
                elif input_val == 2:
                    maze[cur_pos[0]+1, cur_pos[1]] = 1
                    visited_mat[cur_pos[0]+1, cur_pos[1]] = 1
                elif input_val == 3:
                    maze[cur_pos[0], cur_pos[1]-1] = 1
                    visited_mat[cur_pos[0], cur_pos[1]-1] = 1
                elif input_val == 4:
                    maze[cur_pos[0], cur_pos[1]+1] = 1
                    visited_mat[cur_pos[0], cur_pos[1]+1] = 1
                else:
                    print('bad input_val')
                    break
            else:
                print('bad output val ' + str(output_vals[-1]))
                break
                
            if output_vals[-1] == 2:
                end_pos = cur_pos.copy()
            if len(end_pos)>0 and steps>=min_steps and np.sum(visited_mat==0)<=2:
                # Empirically found that there are obstacle loops around
                # 2 pixels, hence I allow 2 zero values in visited_mat
                halt = True
                
        elif optcode%10 in (1, 2):
            pointer_increase = 4
            if str(optcode).zfill(5)[2]=='0':
                first = program[program[cnt+1]]
            elif str(optcode).zfill(5)[2]=='1':
                first = program[cnt+1]
            elif str(optcode).zfill(5)[2]=='2':
                # relative mode
                first = program[program[cnt+1] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[1])
            if str(optcode).zfill(5)[1]=='0':
                second = program[program[cnt+2]]
            elif str(optcode).zfill(5)[1]=='1':
                second = program[cnt+2]
            elif str(optcode).zfill(5)[1]=='2':
                # relative mode
                second = program[program[cnt+2] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[0])
            if optcode%10 == 1:
                if str(optcode).zfill(5)[0]=='2':
                    program[program[cnt+3] + relative_base] = first+second
                else:
                    program[program[cnt+3]] = first + second
            else:
                if str(optcode).zfill(5)[0]=='2':
                    program[program[cnt+3] + relative_base] = first*second
                else:
                    program[program[cnt+3]] = first*second
    
        # part 2:    
        elif optcode%10 in (5, 6, 7, 8):
            if str(optcode).zfill(5)[2]=='0':
                first = program[program[cnt+1]]
            elif str(optcode).zfill(5)[2]=='1':
                first = program[cnt+1]
            elif str(optcode).zfill(5)[2]=='2':
                first = program[program[cnt+1] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[1])
            if str(optcode).zfill(5)[1]=='0':
                second = program[program[cnt+2]]
            elif str(optcode).zfill(5)[1]=='1':
                second = program[cnt+2]
            elif str(optcode).zfill(5)[1]=='2':
                second = program[program[cnt+2] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[0])
            if optcode%10 == 5:
                if first!=0:
                    cnt = second
                    continue
                else:
                    pointer_increase = 3
            elif optcode%10 == 6:
                if first==0:
                    cnt = second
                    continue
                else:
                    pointer_increase = 3
            elif optcode%10 == 7:
                pointer_increase = 4
                if first<second:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 1
                    else:
                        program[program[cnt+3]] = 1
                else:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 0
                    else:
                        program[program[cnt+3]] = 0
            else:
                pointer_increase = 4
                if first == second:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 1
                    else:
                        program[program[cnt+3]] = 1
                else:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 0
                    else:   
                        program[program[cnt+3]] = 0
        
        elif optcode%10==9 and optcode !=99:
            pointer_increase = 2
            
            if str(optcode).zfill(2)[0] == '2':
                relative_base += program[program[cnt+1] + relative_base]
            elif str(optcode).zfill(2)[0] == '1':
                relative_base += program[cnt+1]
            else:
                relative_base += program[program[cnt+1]]
            
        elif optcode == 99:
            halt = True
            
        else:
            print('Bad opt code ' + str(optcode) + \
                  ' at position ' + str(cnt))
            break
        cnt += pointer_increase
    return output_vals, program, end_pos, maze, visited_mat, steps

def calc_oxygen_spread(maze, start_pos):
    oxygen_spread = maze.copy()
    oxygen_spread[0:2,:] = 1
    oxygen_spread[-2:,:] = 1
    oxygen_spread[:,0:2] = 1
    oxygen_spread[:,-2:] = 1    
    oxygen_spread[start_pos[0], start_pos[1]] = 2
    cnt_time = 0
    Nrows = oxygen_spread.shape[0]
    Ncols = oxygen_spread.shape[1]
    
    while True:
        cnt_time += 1
        r, c = np.where(oxygen_spread==2)
        for i in range(len(r)):
            if oxygen_spread[min(Nrows-1, r[i]+1), c[i]] == 0:
                oxygen_spread[min(Nrows-1, r[i]+1), c[i]] = 2
            if oxygen_spread[max(0, r[i]-1), c[i]] == 0:
                oxygen_spread[max(0, r[i]-1), c[i]] = 2
            if oxygen_spread[r[i], min(Ncols-1, c[i]+1)] == 0:
                oxygen_spread[r[i], min(Ncols-1, c[i]+1)] = 2
            if oxygen_spread[r[i], max(0, c[i]-1)] == 0:
                oxygen_spread[r[i], max(0, c[i]-1)] = 2
        #print('open cells left: ' + str(np.sum(oxygen_spread==0)))
        if np.sum(oxygen_spread == 0)<=2:
            print('done')
            return cnt_time
                    

f = open('input15.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(10000)]

# part 1:
min_steps = 0 # minimum steps - use large value like 10000000
# to explore the whole map
# for part 1, you can use 0 - no minimum but stops when oxygen found
maze = np.zeros((43,43)).astype('int')
start_pos = [22,22]
output, program, end_pos, maze, visited_mat, steps = intcode_computer(1, puzzle_input, maze, min_steps=min_steps)

# use A* algorithm implementation to find shortest path
maze2=(1-maze).tolist()
grid = Grid(matrix=maze2)
start = grid.node(start_pos[0], start_pos[1])
end = grid.node(end_pos[0], end_pos[1])
finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)

print('part 1 answer = ' + str(len(path)-1))

# part 2:
cnt_time = calc_oxygen_spread(maze, start_pos=end_pos)

print('part 2 answer = ' + str(cnt_time))
# btw, I found the minimal grid size of ~43 by manually by exploring with a large 
# min_steps param...

