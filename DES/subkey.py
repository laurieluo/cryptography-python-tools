import numpy as np
import random

def gen_rand_key():
    return ''.join([chr(random.randint(0, 1)+ord('0')) for i in range(64)])

class SubKey:
    PC_1 = [57,49,41,33,25,17, 9, 1,\
            58,50,42,34,26,18,10, 2,\
            59,51,43,35,27,19,11, 3,\
            60,52,44,36,63,55,47,39,\
            31,23,15, 7,62,54,46,38,\
            30,22,14, 6,61,53,45,37,\
            29,21,13, 5,28,20,12, 4]
    PC_2 = [14,17,11,24, 1, 5, 3,28,\
            15, 6,21,10,23,19,12, 4,\
            26, 8,16, 7,27,20,13, 2,\
            41,52,31,37,47,55,30,40,\
            51,45,33,48,44,49,39,56,\
            34,53,46,42,50,36,29,32]

    #parameter 'key' is a string as default
    def __init__(self, key):
        original_key_list = list(key)
        self.round_0 = [ord(original_key_list[i-1])-ord('0') for i in PC_1]

    #i index from 1 to 16
    def get_subkey(self, i):
        C0, D0, = self.round_0[:28], self.round_0[28:]
        move = [1,2,4,6,8,10,12,14,15,17,19,21,23,25,27,0]
        Ci = C0[move[i-1]:] + C0[:move[i-1]]
        Di = D0[move[i-1]:] + D0[:move[i-1]]
        sum = Ci + Di
        return [sum[i-1] for i in PC_2]

def bit_diff(num_DES):
    diff_num = []
    while num_DES:
        sub = SubKey(gen_rand_key())
        xor_list = [list(map(lambda x: x[0]^x[1], zip(x, y))).count(1) for x, y in list((sub.get_subkey(i), sub.get_subkey(i+1)) for i in range(1, 16))]
        diff_num += xor_list
        num_DES -= 1
    return np.mean(diff_num)

def bit_cover(num_DES=1):
    true_num = 0
    while num_DES:
        sub = SubKey(gen_rand_key())
        sub.round_0 = [i for i in range(56)]
        union = [set(sub.round_0) == set(x)|set(y) for x, y in list((sub.get_subkey(i), sub.get_subkey(i+1)) for i in range(1, 16))]
        true_num += union.count(True)
        num_DES -= 1
    return true_num
    
