#Contains: append_ON, get_on_off_matrices, append_U, append_OFF_matrices
from math import cos, sin, radians
from scipy.linalg import inv #To invert matrices 
import numpy
from sys import exit


def append_ON(A, B, C, D):
#Building S_on and Q_on matrices for the material(s) used
	ON_matrix = numpy.zeros((3,3))
	ON_matrix[0,0] = A
	ON_matrix[0,1] = B
	ON_matrix[1,0] = B
	ON_matrix[1,1] = C
	ON_matrix[2,2] = D
	return ON_matrix

def append_U(A, B, C, D, E):
#Appends values to U vectors
	Uvector = numpy.zeros((1,5))
	Uvector[0,0] = A
	Uvector[0,1] = B 
	Uvector[0,2] = C
	Uvector[0,3] = D
	Uvector[0,4] = E
	return Uvector

def append_OFF_matrix(v11, v22, v12, v66, v16, v26):
#Appends values to Q_off, S_off	
	OFF_matrix = numpy.zeros((3,3))
	OFF_matrix[0,0] = v11
	OFF_matrix[0,1] = v12
	OFF_matrix[1,0] = v12
	OFF_matrix[1,1] = v22
	OFF_matrix[2,2] = v66
	OFF_matrix[0,2] = v16
	OFF_matrix[2,0] = v16
	OFF_matrix[1,2] = v26
	OFF_matrix[2,1] = v26
	return OFF_matrix

def append_OFF(Qxx, Qyy, Qyx, Qss, theta, Sxx, Sxy, Syy, Sss):
#Building S_off, Q_off matrices

	#***********************Could speed up code by not storing/recalculating constant matrices in plybook
	u1_q = (1/8.0)*(3*(Qxx + Qyy) + 2*(Qyx + 2*Qss))
	u2_q = (1/2.0)*(Qxx - Qyy)
	u3_q = (1/8.0)*(Qxx + Qyy -2*(Qyx + 2*Qss))
	u4_q = (1/8.0)*(Qxx + Qyy + 6*Qyx - 4*Qss)
	u5_q = (1/8.0)*(Qxx + Qyy - 2*(Qyx - 2*Qss))
	Uq = append_U(u1_q, u2_q, u3_q, u4_q, u5_q)

	Q11 = u1_q + (u2_q * cos(2*theta)) + (u3_q * cos(4*theta))
	Q22 = u1_q + (u2_q * -1 * cos(2*theta)) + (u3_q * cos(4*theta))
	Q12 = u4_q + (u3_q * -1 * cos(4*theta))	
	Q66 = u5_q + (u3_q * -1 * cos(4*theta))
	Q16 = (u2_q * (1/2.0) * sin(2*theta)) + (u3_q * sin(4*theta))
	Q26 = (u2_q * (1/2.0) * sin(2*theta)) + (u3_q * -1 * sin(4*theta))		
	Q_off = append_OFF_matrix(Q11, Q22, Q12, Q66, Q16, Q26) 

	u1_s = (1/8.0)*(3*(Sxx + Syy) + 2*Sxy + Sss)
	u2_s = (1/2.0)*(Sxx - Syy)
	u3_s = (1/8.0)*(Sxx + Syy -2*Sxy - Sss)
	u4_s = (1/8.0)*(Sxx + Syy + 6*Sxy - Sss)
	u5_s = (1/2.0)*(Sxx + Syy - 2*Sxy + Sss)
	Us = append_U(u1_s, u2_s, u3_s, u4_s, u5_s)

	S11 = u1_s + (u2_s * cos(2*theta)) + (u3_s * cos(4*theta))
	S22 = u1_s + (u2_s * -1 * cos(2*theta)) + (u3_s * cos(4*theta))
	S12 = u4_s + (u3_s * -1 * cos(4*theta))	
	S66 = u5_s + (u3_s * -4 * cos(4*theta))
	S16 = (u2_s * sin(2*theta)) + (2 * u3_s * sin(4*theta))
	S26 = (u2_s * sin(2*theta)) + (u3_s * -2 * sin(4*theta))		
	S_off = append_OFF_matrix(S11, S22, S12, S66, S16, S26) 

	return S_off, Q_off, Us, Uq

def check_symmetry(plies, h_laminate, h_core):
	if h_core == 0 and plies % 2 == 0: #There is no core and we have an even number of plies, symmetric
		start = (plies/2) - 1 #Start is the position in plybook that we should begin at and work towards 0.
		plyfact = 1
		h0 = 0
		case = 'nocore_symmetric_even'
	elif h_core == 0 and plies % 2 != 0: #There is no core and we have an uneven number of plies
		start = (plies - 1)/2
		plyfact = 0.5 #We are going to use the center of the middle ply, so our first
		h0 = 0
		case = 'nocore_symmetric_uneven'
	elif h_core != 0 and (plies - 1) % 2 == 0: #There is a core and an even number of plies
		start = (plies - 1)/2 - 1 
		plyfact = 1
		h0 = h_core/2000.0 #Convert h0 to m
		case = 'core_symmetric_even'
	else: #There is a core and an uneven number of plies !! Give a warning!
		case = 'core_notsymmetric'
		print 'WARNING! System not symmetric!' + case
		exit()
	return start, plyfact, h0, case

def compute_A_D(plybook, plies, h_laminate, h_core):
	#May run into a problem here is my laminate contains a core
	i = 0

	U = plybook[i][18] #My U's are in GN/m^2 = GPa 
	U1 = U[0][0]
	U2 = U[0][1]
	U3 = U[0][2]
	U4 = U[0][3]
	U5 = U[0][4]
	V1a = 0
	V2a = 0
	V3a = 0
	V4a = 0

	while i < plies:
		if plybook[i][1] != 'CORE':
			theta = radians(plybook[i][2])
			V1a += (plybook[i][3]/1000.0)*cos(2*theta)
			V2a += (plybook[i][3]/1000.0)*cos(4*theta)
			V3a += (plybook[i][3]/1000.0)*sin(2*theta)
			V4a += (plybook[i][3]/1000.0)*sin(4*theta)
		i += 1	

	#Get A and A_comp=a matrices
	A11 = U1*((h_laminate - h_core)/1000.0) + U2*V1a + U3*V2a
	A22 = U1*((h_laminate - h_core)/1000.0) - U2*V1a + U3*V2a
	A12 = U4*((h_laminate - h_core)/1000.0) - U3*V2a
	A66 = U5*((h_laminate - h_core)/1000.0) - U3*V2a
	A16 = (1/2.0)*U2*V3a + U3*V4a
	A26 = (1/2.0)*U2*V3a - U3*V4a

	A = append_OFF_matrix(A11, A22, A12, A66, A16, A26)
	A_comp = inv(A)

	#Get D and D_comp=d matrices
	zc_star = h_core / h_laminate #h_core = 2*Zc, which is why I'm not multiplying by 2 as in Eq. 5.30
	h_star = (1 - zc_star**3)*((h_laminate/1000.0)**3) / 12.0 #in m now
	start, plyfact, h0, case = check_symmetry(plies, h_laminate, h_core)
	
	theta = radians(plybook[start][2]) #Initial starting position
	h = h0 + (plyfact * plybook[start][3] / 1000.0) #For the very first summation, we have a ply factor to account for when we have an uneven number of plies

	V1d = cos(2*theta) * (h**3 - h0**3)
	V2d = cos(4*theta) * (h**3 - h0**3)
	V3d = sin(2*theta) * (h**3 - h0**3)
	V4d = sin(4*theta) * (h**3 - h0**3)

	j = start - 1

	while j > -1:
		temp = h + (plybook[start][3] / 1000.0) #Convert thickness to m
		theta = radians(plybook[j][2])

		V1d += cos(2*theta) * (temp**3 - h**3)
		V2d += cos(4*theta) * (temp**3 - h**3)
		V3d += sin(2*theta) * (temp**3 - h**3)
		V4d += sin(4*theta) * (temp**3 - h**3)

		h = temp
		j -= 1 

	V1d = (2/3.0) * V1d
	V2d = (2/3.0) * V2d
	V3d = (2/3.0) * V3d
	V4d = (2/3.0) * V4d

	D11 = (h_star * U1) + (U2 * V1d) + (U3 * V2d)
	D22 = (h_star * U1) - (U2 * V1d) + (U3 * V2d)
	D12 = (h_star * U4) - (U3 * V2d)
	D66 = (h_star * U5) - (U3 * V2d)
	D16 = (1/2.0) * (U2 * V3d) + (U3 * V4d)
	D26 = (1/2.0) * (U2 * V3d) - (U3 * V4d)

	D = append_OFF_matrix(D11, D22, D12, D66, D16, D26) #[GNm]
	D_comp = inv(D) #1/GNm

	return A, A_comp, D, D_comp	

def get_on_off_matrices(plies, plybook, i):	
	#Calculates the S_on/off, Q_on/off, Us and Uq material property matrices/vectors in the generalized Hooke's law equations and outputs
	Sxx = 1/plybook[i][4]
	Sxy = -1*plybook[i][7]/plybook[i][4]
	Syy = 1/plybook[i][5]
	Sss = 1/plybook[i][6]
	plybook[i][13] = append_ON(Sxx, Sxy, Syy, Sss) #S_on

	m = 1/(1 - plybook[i][5] * (plybook[i][7])**2 / plybook[i][4])
	Qxx = m*plybook[i][4]
	Qyx = m*plybook[i][7]*plybook[i][5]
	Qyy = m*plybook[i][5]
	Qss = plybook[i][6]
	plybook[i][14] = append_ON(Qxx, Qyx, Qyy, Qss) #Q_on

	theta = radians(plybook[i][2]) #Orientation of the ply

	plybook[i][15], plybook[i][16], plybook[i][17], plybook[i][18] = append_OFF(Qxx, Qyy, Qyx, Qss, theta, Sxx, Sxy, Syy, Sss) #S_off, Q_off, Us, Uq

	return plybook

def get_off_axis_strain(plybook,i, stress_off):
	import numpy

	S_off = plybook[i][15]
	strain_off = numpy.dot(S_off, stress_off)

	return strain_off 	

def convert_to_on_axis(plybook, i, strain_off):
#Converts off-axis stress to on-axis quantities	
	from math import sin, cos, radians

	strain_1 = strain_off[0][0]
	strain_2 = strain_off[1][0]
	strain_6 = strain_off[2][0]	
 
	theta = radians(plybook[i][2])

	p = (1/2.0)*(strain_1 + strain_2)
	q = (1/2.0)*(strain_1 - strain_2)
	r = (1/2.0)*strain_6

	strain_x = p + q*cos(2*theta) + r*sin(2*theta)
	strain_y = p - q*cos(2*theta) - r*sin(2*theta)
	strain_s = 2*r*cos(2*theta) - 2*q*sin(2*theta)

	strain_on = numpy.zeros((3,1))
	strain_on[0][0] = strain_x
	strain_on[1][0] = strain_y
	strain_on[2][0] = strain_s

	Q_on = plybook[i][14]
	stress_on = numpy.dot(Q_on, strain_on)

	return stress_on, strain_on	

def convert_to_off_axis(plybook, i, stress_on):
#Converts on-axis strain to off-axis quantities 
	# from math import sin, cos, radians
	# from scipy.linalg import inv #To invert matrices 

	S_on = plybook[i][13]
	strain_on = numpy.dot(S_on, stress_on)

	stress_x = stress_on[0][0]
	stress_y = stress_on[1][0]
	stress_s = stress_on[2][0]	
 
 	p_bar = (1/2.0)*(stress_x + stress_y)
 	q_bar = (1/2.0)*(stress_x - stress_y)
 	r_bar = stress_s

	theta = -1*radians(plybook[i][2])

	stress_1 = p_bar + q_bar*cos(2*theta) + r_bar*sin(2*theta)
	stress_2 = p_bar - q_bar*cos(2*theta) - r_bar*sin(2*theta)
	stress_6 = r_bar*cos(2*theta) - q_bar*sin(2*theta)
	
	stress_off = numpy.zeros((3,1))
	stress_off[0][0] = stress_1
	stress_off[1][0] = stress_2
	stress_off[2][0] = stress_6

	S_off = plybook[i][15]
	strain_off = numpy.dot(S_off, stress_off)

	return strain_on, stress_off, strain_off	