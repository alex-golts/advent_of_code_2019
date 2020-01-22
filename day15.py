import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# intcode computer function - from Day 9 but modified 
# to account for droid movement 
def intcode_computer(input_val, program, maze):
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    
    visited_mat = np.zeros_like(maze)
    start_pos = [int(maze.shape[0]/2), int(maze.shape[1]/2)]
    visited_mat[start_pos[0], start_pos[1]] = 1
    end_pos = []
    cur_pos = start_pos.copy()
    while halt == False:
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
                #output_vals.append(program[cnt+1] + relative_base)
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
                elif input_val == 2:
                    maze[cur_pos[0]+1, cur_pos[1]] = 1
                elif input_val == 3:
                    maze[cur_pos[0], cur_pos[1]-1] = 1
                elif input_val == 4:
                    maze[cur_pos[0], cur_pos[1]+1] = 1
                else:
                    print('bad input_val')
                    break
            else:
                print('bad output val ' + str(output_vals[-1]))
                break
                
            if output_vals[-1] == 2:
                end_pos = tuple(cur_pos.copy())
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
            
            #relative_base += program[cnt+1]
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
    return output_vals, program, end_pos, maze


f = open('input15.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

# part 1:
maze = np.zeros((50,50)).astype('int')
output, program, end_pos, maze = intcode_computer(1, puzzle_input, maze)
start_pos = (25,25)

# put wall around whole walkable maze:
sum_rows = np.sum(maze,0)
sum_cols = np.sum(maze,1)
first_col = np.where(sum_rows>0)[0][0]
last_col = np.where(sum_rows>0)[0][-1]
first_row = np.where(sum_cols>0)[0][0]
last_row = np.where(sum_cols>0)[0][-1]

maze[first_row-1, :] = 1
maze[last_row+1, :] = 1
maze[:, first_col-1] = 1
maze[:, last_col+1] = 1

# use A* algorithm implementation to find shortest path
maze=(1-maze).tolist()
grid = Grid(matrix=maze)
start = grid.node(start_pos[0], start_pos[1])
end = grid.node(end_pos[0], end_pos[1])
finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)

print('part 1 answer = ' + str(len(path)-1))

