import numpy as np

f = open('input6.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]
txt = [item.split(')') for item in txt]


class Node(object):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        
def num_descendants(node):
    
    if len(node.children)==0:
        return 0
    else:
        cnt = len(node.children)
        for c in node.children:
            cnt += num_descendants(c)
        return cnt
        
    

    
tree_nodes = {}
# create a tree and put all nodes in a dictionary
for item in txt:
    if item[0] not in tree_nodes:
        tree_nodes[item[0]] = Node(item[0])
for item in txt:
    if item[1] not in tree_nodes:
        tree_nodes[item[1]] = Node(item[1])
        
for item in txt:
    tree_nodes[item[0]].add_child(tree_nodes[item[1]])

# the answer is the total number of descendants of all nodes in the tree
total = 0
for key in tree_nodes:
    total += num_descendants(tree_nodes[key])

print('total = ' + str(total))



# Part 2:

def find_parent(node_name):
    if node_name == 'COM':
        return None
    for key in tree_nodes:
        if tree_nodes[node_name] in tree_nodes[key].children:
            return tree_nodes[key].name
        

def is_anscestor(a, b):
    # find whether node a is an anscestor of b
    # and return the number of generations separating them
    if b.name == a.name:
        return False, 0
    cur_node_name = find_parent(b.name)
    if cur_node_name == None:
        return False, np.nan
    cur_node = tree_nodes[cur_node_name]
    cnt=1
    while True:
        if cur_node.name == a.name:
            return True, cnt
        cur_node_name = find_parent(cur_node.name)
        if cur_node_name == None:
            return False, np.nan
        cur_node = tree_nodes[cur_node_name]
        cnt+=1
        
def find_common_anscestor(a, b):
    # find closest common anscestor of node a and b
    # and return it's distance (in generations) for each
    found = False
    cur_parent_name = find_parent(a.name)
    dist_from_a = 0
    while not found:
        is_ans, dist_from_b = is_anscestor(tree_nodes[cur_parent_name], b)
        if is_ans:
            common_anscestor = tree_nodes[cur_parent_name]
            found = True
        cur_parent_name = find_parent(cur_parent_name)
        dist_from_a += 1
    return common_anscestor, dist_from_a, dist_from_b


        
you_parent = find_parent('YOU')
san_parent = find_parent('SAN')

#find_shortest_path(you_parent, san_parent)

_,dist1,dist2=find_common_anscestor(tree_nodes[you_parent], tree_nodes[san_parent])

print('shortest path = ' + str(dist1+dist2))