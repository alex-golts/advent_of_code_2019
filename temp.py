import numpy as np

# day 1

def calc_module_fuel(module_weight):
    total = module_weight
    cur = module_weight
    while True:
        cur = int(np.floor(cur/3)-2)
        if cur<=0:
            break
        total+=cur
    return total

# part 1:

f=open('input1.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]
total = sum([int(np.floor(int(item)/3)-2) for item in txt])

# part 2:

total_with_fuel = sum([calc_module_fuel(int(np.floor(int(item)/3)-2)) for item in txt])


# day 2

# part 1:
f=open('input2.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
nums = [int(item) for item in txt]


nums[1]=12
nums[2]=2

for i in range(0, len(nums), 4):
    if nums[i]==99:
        break
    if nums[i]==1:
        nums[nums[i+3]] = nums[nums[i+1]]+nums[nums[i+2]]
    if nums[i]==2:
        nums[nums[i+3]] = nums[nums[i+1]]*nums[nums[i+2]]


# part 2:

for noun in range(100):
    for verb in range(100):
        nums = [int(item) for item in txt]
        nums[1] = noun
        nums[2] = verb
        for i in range(0, len(nums), 4):
            if nums[i]==99:
                break
            if nums[i]==1:
                nums[nums[i+3]] = nums[nums[i+1]]+nums[nums[i+2]]
            if nums[i]==2:
                nums[nums[i+3]] = nums[nums[i+1]]*nums[nums[i+2]]
        if nums[0]==19690720:
            print('noun=' + str(noun))
            print('verb=' + str(verb))
            break


# day 3:

# part 1:

def calc_wire_path(wire):
    # not very efficient... :( but works
    path = [(0,0)] # x,y convention
    for item in wire:
        if item[0] == 'L':
            path += [(path[-1][0]-n, path[-1][1]) for n in range(1,int(item[1:])+1)]
            #path.append((path[-1][0]-int(item[1:]), path[-1][1]))
        elif item[0] == 'R':
            path += [(path[-1][0]+n, path[-1][1]) for n in range(1,int(item[1:])+1)]
            #path.append((path[-1][0]+int(item[1:]), path[-1][1]))
        elif item[0] == 'U':
            path += [(path[-1][0], path[-1][1]+n) for n in range(1,int(item[1:])+1)]
            #path.append((path[-1][0], path[-1][1]+int(item[1:])))
        elif item[0] == 'D':
            path += [(path[-1][0], path[-1][1]-n) for n in range(1,int(item[1:])+1)]
            #path.append((path[-1][0], path[-1][1]-int(item[1:])))

    return path

def closest_point(points):
    min_dist = abs(points[0][0]) + abs(points[0][1])
    for p in points:
        dist = abs(p[0]) + abs(p[1])
        if dist<min_dist:
            min_dist = dist
    return min_dist

def fastest_point(points, path1, path2):
    min_time = len(path1) + len(path2)
    for p in points:
        t = path1.index(p) + path2.index(p)
        if t<min_time:
            min_time = t
    return min_time

f=open('input3.txt','r')
txt=f.read()
txt = txt.split('\n')
txt=txt[:-1]
wire1 = txt[0].split(',')
wire2 = txt[1].split(',')

wire1_path = calc_wire_path(wire1)
wire2_path = calc_wire_path(wire2)

inter_points = list(set(wire1_path).intersection(wire2_path))
inter_points.remove((0,0))
min_dist = closest_point(inter_points)
print('min_dist=' + str(min_dist))

# part 2
min_time = fastest_point(inter_points, wire1_path, wire2_path)
print('min_time = ' + str(min_time))


# day 4:

# part 1 & 2:

def two_adjacent_digits(num):
    s = str(num)
    for i in range(len(s)-1):
        if s[i]==s[i+1]:
            return True
    return False

def exactly_two_adjacent_digits(num):
    # for part 2
    s = str(num)
    cnt_adjacent = 0
    for i in range(len(s)-1):
        if s[i]==s[i+1]:
            cnt_adjacent+=1
        else:
            if cnt_adjacent==1:
                return True
            else:
                cnt_adjacent=0
    print(cnt_adjacent)
    return cnt_adjacent==1


def increasing_only(num):
    s = str(num)
    for i in range(len(s)-1):
        if s[i]>s[i+1]:
            return False
    return True

range_val = [353096, 843212]
cnt=0
for num in range(range_val[0], range_val[1]+1):
    if two_adjacent_digits(num) and increasing_only(num) and exactly_two_adjacent_digits(num):
        cnt+=1
print(str(cnt) + ' passwords meet criteria')







