import numpy

def create_appliedvector(x1, x2, x6, mult):
	x = numpy.zeros((1,3))

	x[0,0] = x1*mult 
	x[0,1] = x2*mult 
	x[0,2] = x6*mult	

	return x.T

def input_loads(case):
	#print "INPUTS:\n"

	##______For use if you don't want to input the load while debugging!
	# #N1 = 4545.4545 #Ass5
	# N1 = 0.025*10**(6) #Ass 6 q1
	# N2 = 0.05*10**(6)
	# #N2 = 0 #Ass5
	# N6 = 0
	
	# #M1 = -1159.0909 #Ass5
	# M1 = 0 #Ass 6 q1
	# M2 = 0
	# M6 = 0

	#Rough dimensions of the platform: L x W (m)
	W = 225.0 / 1000.0 #Where width is in the 1 direction (m)
	H = 190.0 / 1000.0 #The height of the steering wheel
	a = 77.5 / 1000.0 #The distance from one end to the aluminum housing (70mm wide)
	if case == 1: #The Radial case
		M1 = 0
		M2 = 0
		M6 = 0
		N1 = -660 / H #We consider compression in both directions
		N2 = -660 / W
		N6 = 0

		# M1 = -1000
		# M2 = -100
		# M6 = -100
		# N1 = -22400
		# N2 = -3000
		# N6 = -2000
		mult = 1
		stress_type = 'OFF'
		moment_type = 'OFF'
		stress = create_appliedvector(N1, N2, N6, mult)
		moment = create_appliedvector(M1, M2, M6, mult)
	# elif case == 2: #The Torque case (NEGLECTED)
	# 	M1 = 0
	# 	M2 = 0
	# 	M6 = 0
	# 	N1 = 0
	# 	N2 = 0
	# 	N6 = 135 / 

	# 	# M1 = -980
	# 	# M2 = -98
	# 	# M6 = -110
	# 	# N1 = -20800
	# 	# N2 = -280
	# 	# N6 = -2200
	# 	mult = 1
	# 	stress_type = 'OFF'
	# 	moment_type = 'OFF'
	# 	stress = create_appliedvector(N1, N2, N6, mult)
	# 	moment = create_appliedvector(M1, M2, M6, mult)
	elif case == 2: #The Axial case is tensile bending in the 1 direction
		M1 = (370.0 / 4.0) * (W + 2*a) / H
		M2 = 0
		M6 = 0
		N1 = 0
		N2 = 0
		N6 = 0

		# M1 = -980
		# M2 = -98
		# M6 = -110
		# N1 = -20800
		# N2 = -280
		# N6 = -2200
		mult = 1
		stress_type = 'OFF'
		moment_type = 'OFF'
		stress = create_appliedvector(N1, N2, N6, mult)
		moment = create_appliedvector(M1, M2, M6, mult)		
	else:
		stress_type = raw_input("Would you like to input a resultant applied stress? ON/OFF/NO \n")
		
		if stress_type != "NO":
			print "Enter the applied stress resultant vector [N1, N2, N6] [N/m]."
			N1 = float(raw_input("N1 = "))
			N2 = float(raw_input("N2 = "))
			N6 = float(raw_input("N6 = "))

			mult = 1 #Input in N/m, but values are in GPa

			stress = create_appliedvector(N1, N2, N6, mult)
		else:
			stress = numpy.zeros((1,3)).T

		moment_type = raw_input("Would you like to input a resultant applied moment? ON/OFF/NO \n")
		if moment_type != "NO":
			print "Enter the applied moment resultant vector [M1, M2, M6] [N]."
			M1 = float(raw_input("M1 = "))
			M2 = float(raw_input("M2 = "))
			M6 = float(raw_input("M6 = "))

			mult = 1

			moment = create_appliedvector(M1, M2, M6, mult)
		else:
			moment = numpy.zeros((1,3)).T	

	#print "\n------------------------------------------------------------------------------"	
	return stress, stress_type, moment, moment_type		