## Common variables for the keccak(512](M || 01, 256
rate = 1088
capacity = 512
output_size = 256


## Generate initial input string of block size 1088 for 256 bit encryption purposes
plaintext = [1] * rate

## Generate 1600 bit initial state of zeros
state_array = [0] * (rate + capacity)

## Generate Keccak Function Matrix of size 5 x 5 x 64 (1600 bits initialized at zero)
state_matrix = [[[0] * 64] * 5] * 5

def sponge(plaintext, state_array, ):
	

def keccak():
	for i_rate in range(24):
		A 

def keccak_round():
	


def theta(A):
	C = [[] * 64] * 5
	D = [[] * 64] * 5
	A_out = [[[0] * 64] * 5] * 5
	for z in range(64):
		for x in range(5):
			C[x][z] = A[x][0][z] ^ A[x][1][z] ^ A[x][2][z] ^ A[x][3][z] ^ A[x][4][z]
	for z in range(64):
		for x in range(5):
			D[x][z] = C[(x - 1) % 5][z] ^ C[(x + 1) % 5][(z - 1) % 64]
	for z in range(64):
		for x in range(5):
			for y in range(5):
				A_out[x][y][z] = A[x][y][z] ^ A[x][z]
	return A_out

def rho(A):
	

def pi():
	

def chi():
	

def iota():
	


