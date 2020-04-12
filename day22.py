import re
import numpy as np

f = open('input22.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]

# example:
#deck = [i for i in range(10)]
deck = [i for i in range(10007)]

def deal_into_new_stack(deck):
    return deck[::-1]

def cut_cards(deck, N):
    if N>0:
        return deck[N:] + deck[0:N]
    elif N<0:
        return deck[N:] + deck[0:len(deck)+N]
    else: 
        return deck
    
def deal_with_increment(deck, N):
    new_deck = [0 for i in range(len(deck))]
    for i in range(len(deck)):
        new_deck[i*N%len(deck)] = deck[i]
    return new_deck


# part 1:
for line in txt:
    if line.startswith('deal into new stack'):  
        deck = deal_into_new_stack(deck)
    else:
        N = [int(d) for d in re.findall(r'-?\d+', line)][0]
        if line.startswith('cut'):
            deck = cut_cards(deck, N)
        elif line.startswith('deal with increment'):
            deck = deal_with_increment(deck, N)

print(f'part 1 answer = {deck.index(2019)}')

# given deck length and position in the resulting deck, 
# return position in the original deck for the 3 shuffle operations:

def reverse_deal_into_new_stack(pos, length):
    return length-pos

def reverse_cut_cards(pos, length, N):
    if N>0:
        if pos<length-N:
            return N+pos
        else: 
            return pos - (length-N)
    elif N<0:
        if pos<-N:
            return length+N+pos
        else:
            return pos+N
    
def reverse_deal_with_increment(pos, length, N):
    if pos%N==0:
        return pos//N
    else:
        return (N-pos%N)*length//N+pos//N+1



# part 2:
length = 119315717514047
iters = 101741582076661

def shuffle_pos_backwards(pos, length):
    for line in txt[::-1]:
        if line.startswith('deal into new stack'):  
            pos = reverse_deal_into_new_stack(pos, length)
        else:
            N = [int(d) for d in re.findall(r'-?\d+', line)][0]
            if line.startswith('cut'):
                pos = reverse_cut_cards(pos, length, N)
            elif line.startswith('deal with increment'):
                pos = reverse_deal_with_increment(pos, length, N)
    return pos
    
final_pos = 2020
cnt = 0

# run once:
# pos = shuffle_pos_backwards(final_pos, length)
# new_pos = pos+1 # just initialize it to something different
# # find how many iterations it takes for the position to come back the same:

# cnt=1
# cur_pos = pos
# positions = []
# dups = []
# while len(dups) == 0:
#     new_pos = shuffle_pos_backwards(cur_pos, length)
#     positions.append(new_pos)
#     cur_pos = new_pos
#     cnt+=1
#     dups = [item for item, count in collections.Counter(positions).items() if count > 1]
#     print(f'new pos = {new_pos}, cnt={cnt}')
    

# print(f'It took {cnt} iterations to return to the same position')

###############################################################
# after the above approach failed, I resorted to this tutorial:
# https://codeforces.com/blog/entry/72593
# Let's reimplement part 1 using it:
# assume each transformation is represented as f(x)=ax+b mod m


def total_transformation(txt, length):
    # initialize transformation:
    a_total = 1
    b_total = 0
    for line in txt:
        if line.startswith('deal into new stack'):  
            a_cur = -1
            b_cur = -1
            
        else:
            N = [int(d) for d in re.findall(r'-?\d+', line)][0]
            if line.startswith('cut'):
                a_cur = 1
                b_cur = -N
                
            elif line.startswith('deal with increment'):
                a_cur = N
                b_cur = 0
        # compose the new transform and the total existing one so far:
        a_total = (a_total*a_cur)%length
        b_total = (b_total*a_cur+b_cur)%length
    return a_total, b_total

def compose_trans(f, g, m):
    # compose two transformations g(f(x))
    # f(x) = ax+b, g(x) = cx+d
    # f and g are tuples containing (a,b) and (c,d) respectively
    a = f[0]
    b = f[1]
    c = g[0]
    d = g[1]
    return ((a*c)%m, (b*c+d)%m)

# apply total transform:
a_total, b_total = total_transformation(txt, len(deck))

deck = [i for i in range(len(deck))]
new_deck = [0 for i in range(len(deck))]
for i in range(len(deck)):
    new_deck[(a_total*i+b_total)%len(deck)] = deck[i]

print(f'part 1 answer (2nd implementation) = {new_deck.index(2019)}')

# part 2:
a_total, b_total = total_transformation(txt, length)

# exponentiation by squaring:
# see https://codeforces.com/blog/entry/72527 for explanation
def pow_square(x, n):
    if n == 0: 
        return 1
    t = pow_square(x, int(np.floor(n/2)))
    if n%2 == 0:
        return t*t
    else:
        return t*t*x
    
def pow_mod_iter(x, n, m):
    y = 1
    while n > 0:
        if n%2==1:
            y = (y*x)%m
        n = int(np.floor(n/2))
        x = (x*x)%m
    return y

# adapt for transformations:
def pow_compose_trans(f, n, m):
    g = (1, 0)
    while n > 0:
        if n%2 == 1:
            g = compose_trans(g, f, m)
        n = int(np.floor(n/2))
        f = compose_trans(f, f, m)
    return g
# apply exponentiation to the power of iter to the total transformation:
g = pow_compose_trans((a_total, b_total), iters, length)
a_final = g[0]
b_final = g[1]

# invert the transformation to find the item at position x:
#f^-1 = (x-b)/a mod m
# assuming iters is prime, and according to fermat little theorem:
a_final_inverse = pow_mod_iter(a_final,length-2,length)

# and:
b_final_inverse = (-b_final*a_final_inverse)

# therefore the result should be:
res =  (2020*a_final_inverse +b_final_inverse)%length
print(f'part 2 result = {res}')

# check that indeed an inverse function is calculated
x = (a_final*res+b_final)%length
print(f'x={x}')

