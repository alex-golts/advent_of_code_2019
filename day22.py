import re
f = open('input22.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]

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


