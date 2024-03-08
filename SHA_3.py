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

## Rho array for rho step
rho_array = [[0, 1, 190, 28, 91], [36, 300, 6, 55, 276], [3, 10, 171, 153, 231], [105, 45, 15, 21, 136], [210, 66, 253, 120, 78]]

def sponge(plaintext, state_array, ):
	

def keccak():
	for i_rate in range(24):
		A 

def keccak_round():
	


def theta(A):
	C = [[] * 64] * 5
	D = [[] * 64] * 5
	A_out = [[[] * 64] * 5] * 5
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

def rho(A, rho_array):
	A_out = [[[] * 64] * 5] * 5
	for z in range(64):
		for x in range(5):
			for y in range(5):
				z_out = rho_array[x][y] % 64
				A_out[x][y][z_out] = A[x][y][z]
	return A_out

def pi(A):
	A_out = [[[] * 64] * 5] * 5
	for z in range(64):
		for x in range(5):
			for y in range(5):
				A_out[x][y][z] = A[(x + (3 * y)) % 5][x][z]
	return A_out

def chi(A):
	A_out = [[[] * 64] * 5] * 5
	for x in range(5):
		for y in range(5):
			A_out[x][y][z] = A[x][y][z] ^ ((not A[(x + 1) % 5][y][z]) and A[(x + 2) % 5][y][z])
	return A_out

def iota(A, RC):
	A_out = [[[] * 64] * 5] * 5
	for z in range(64):
		for x in range(5):
			for y in range(5):
				A_out[x][y][z] = A[x][y][z] ^ RC
