import numpy
from math import floor,sin

def inp_bin(inp):
	out = ''
	for x in inp:
		out = bin(ord(x))[2:].zfill(8) + out
	return out

def padding(inp):
	a = len(inp) 
	while a/512 != 0:
		a = a/512
	if a != 0 and a > 448:
		inp = inp + '1' + '0'*(511 - a)
	elif a != 0:
		pad =  bin(len(inp))[2:].zfill(64)
		inp = inp + '1' + '0'*(447 - a) + pad
	print '->', len(inp)
	return inp 

def f(X,Y,Z,i):
	if i < 16:
		o = (int(X,2) & int(Y,2)) | (~(int(X,2)) & int(Z,2))
	elif i < 32:
		o = (int(X,2) & int(Z,2)) | (int(Y,2) & ~(int(Z,2)))
	elif i < 48:
		o = int(X,2) ^ int(Y,2) ^ int(Z,2)
	elif i < 64:
		o = abs(int(Y,2) ^ (int(X,2) | ~(int(Z,2))))
	return bin(o)[2:].zfill(32)

def mod(a,b):
	s = int(a,2) + int(b,2)
	while  s > pow(2,32) - 1:
		s -= pow(2,32)
	return bin(s)[2:].zfill(32)

def rounds(Q,W,K):
	for i in range(64):
		Q[i+4] = mod(Q[i+3],bin(int((mod(Q[i],mod(f(Q[i+3],Q[i+2],Q[i+1],i),mod(W[i%16],K[i])))),2)<<(i%16))[2:].zfill(32))
	return Q

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