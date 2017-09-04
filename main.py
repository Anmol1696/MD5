import numpy
from math import floor,sin
from md5 import * 

def main(inp):
	A = bin(0x67452301)[2:].zfill(32)
	B = bin(0xEFCDAB89)[2:].zfill(32)
	C = bin(0x98BADCFE)[2:].zfill(32)
	D = bin(0x10325476)[2:].zfill(32)

	K = [bin(int(floor(abs(sin(i+1)*(pow(2,32))))))[2:].zfill(32) for i in range(64)]

	msg = padding(inp_bin(inp))
	for u in range(len(msg)/512):
		
		Q = ['' for x in range(68)]
		(Q[0],Q[1],Q[2],Q[3]) = (A,D,C,B)
		
		W = ['' for x in range(16)]
		for i in range(16):
			for p in range(32):
				W[i] += msg[p + (512*u) + (i*32)]
		
		Q = rounds(Q,W,K)
		(A,B,C,D) = (mod(Q[64],Q[0]),mod(Q[67],Q[3]),mod(Q[66],Q[2]),mod(Q[65],Q[1]))
	out = hex(int(A,2))[2:].zfill(8) + hex(int(B,2))[2:].zfill(8) + hex(int(C,2))[2:].zfill(8) + hex(int(D,2))[2:].zfill(8)
	return out

if __name__ == '__main__':
	inp = raw_input('Enter the msg ->')
	print 'MD-5 Hash ->\n',main(inp)