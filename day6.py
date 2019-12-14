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


