import numpy

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

