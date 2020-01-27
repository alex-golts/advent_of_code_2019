from itertools import cycle, islice, accumulate
import numpy as np
#from scipy.sparse import csr_matrix, lil_matrix

f = open('input16.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')[0]

input_signal = txt

    
def fft_last_half(input_signal, i, num_phases):
    cur_input = [int(item) for item in input_signal]
    for p in range(num_phases):
        output_signal = cur_input
        output_signal[i:] = list(np.cumsum(cur_input[::-1][0:len(cur_input)-i])[::-1]%10)
        cur_input = output_signal
        print('completed ' + str(p) + ' phases')
    return output_signal

def fft_efficient(input_signal, num_phases):
    cur_input = [int(item) for item in input_signal]
    for p in range(num_phases):
        output_signal = cur_input
        for i in range(len(cur_input)):
            cur_item = abs(list(accumulate([sum(cur_input[i+4*(i+1)*j:2*i+1+4*(i+1)*j]) for j in range(len(cur_input))]))[-1] \
                - list(accumulate([sum(cur_input[3*i+2+4*(i+1)*j:4*i+3+4*(i+1)*j]) for j in range(len(cur_input))]) )[-1])%10
            output_signal[i] = cur_item
        cur_input = output_signal
        print('completed ' + str(p) + ' phases')
    return output_signal
            
                
def fft(input_signal, base_pattern, num_phases):
    cur_input = [int(item) for item in input_signal]
    for p in range(num_phases):
        output_signal = []
        for i in range(len(cur_input)):
            # repeat values: 
            cur_pattern = [item for item in base_pattern for k in range(i+1)]
            # create cycle and offset by one:
            cur_pattern = list(islice(cycle(cur_pattern[1:] + [cur_pattern[0]]), len(input_signal)))
            # multiply element-wise, sum and take ones digit
            cur_item = abs(sum([a*b for a,b in zip(cur_input,cur_pattern)]))%10
            output_signal.append(cur_item)
        cur_input = output_signal.copy()
        print('completed ' + str(p) + ' phases')
    return output_signal


def fft_mat(input_signal, base_pattern, num_phases):
    base_pattern = np.array(base_pattern)
    input_signal = np.array([int(item) for item in input_signal])
    #M = lil_matrix((len(input_signal), len(input_signal)))
    M = np.zeros((len(input_signal), len(input_signal)))
    for i in range(len(input_signal)):
        # repeat values:
        cur_pattern = np.repeat(base_pattern, i+1)
        # create cycle and offset by one:
        if len(cur_pattern)<=len(input_signal):
            num_whole_reps = int(np.floor(len(input_signal)/len(cur_pattern)))
            num_left = len(input_signal) - num_whole_reps*len(cur_pattern)
            M[i, :-(num_left+1)] = np.tile(cur_pattern, num_whole_reps)[1:]
            M[i, len(input_signal)-(num_left+1):] = cur_pattern[0:num_left+1]
        else:
            M[i, :] = cur_pattern[1:][0:len(input_signal)]
    cur_input = input_signal

    for p in range(num_phases):
        #cur_input = (abs(M.dot(cur_input))%10).astype('int')
        cur_input = (abs(np.matmul(M,cur_input))%10).astype('int')
    return cur_input
        

# part 1 - slow:
#output_1 = fft(input_signal, [0, 1, 0, -1], 100)
#output_1 = fft_efficient(input_signal, 100) # this ended up slow


# part 1 - fast:
input_signal = input_signal
output_1 = fft_mat(input_signal, [0, 1, 0, -1], 100) # this is only feasible for small inputs
print('part 1 answer = ' + str(output_1[0:8]))

# part 2:
offset = int(input_signal[0:7])
input_signal = 10000*input_signal
output_2 = fft_last_half(input_signal, offset, 100)
print('part 2 answer = ' + str(output_2[offset:offset+8]))
