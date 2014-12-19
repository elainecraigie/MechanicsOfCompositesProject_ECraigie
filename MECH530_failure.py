#Contains the following failure analysis methods:
#1. Maximum stress
#2. Quadratic polynomial
#3. Hashin Failure criteria
import numpy
from numpy import absolute

def solve_quadratic(a, b, c, i):
	#Used to solve the quadratic equations and check for special cases in the Hashin and Quadratic criterions
	if a == 0:
		if b == 0: #a=b=0, you have a constant function and there can be no solution
			raise ValueError("There can be no solution since a = b = 0, c = constant")
		else: #you have a linear function that will have one zero
			Rp = (-1.0 * c) / b
			Rm = (-1.0 * c) / b
			print "BEWARE: You only have one root here!!! Ply %d" %(i)
	else: #a != 0
		if b == 0: #You have a single quadratic term in your variable, you can directly take the root provided that c < 0
			delta = (-1.0 * c) / a
			if delta < 0:
				raise ValueError("Cannot take root of negative value")
			Rp = (delta)**(0.5)
			Rm = -1.0 * (delta)**(0.5)
		else: #You have a regular quadratic function that can  be solved using the quadratic formula
			delta = (b)**2 - 4 * a * c
			if delta < 0:
				raise ValueError("ERROR! Delta less than zero, imaginary root... Hashin")	
			Rp = (-1.0 * b + (delta)**(0.5)) / (2.0 * a)
			Rm = (-1.0 * b - (delta)**(0.5)) / (2.0 * a)

	return Rp, Rm

def failure_props(plybook,i):
	#The material strength properties	
	x_t = 10**(-3) * plybook[i][8] #Convert strength properties: [MPa] --> [GPa] so that this matches stress units [GPa]
	x_c = 10**(-3) * plybook[i][9]
 	y_t = 10**(-3) * plybook[i][10] 
	y_c = 10**(-3) * plybook[i][11]
 	s = 10**(-3) * plybook[i][12]
 
 	mydict = ['x_t', 'x_c', 'y_t', 'y_c', 's']
	values = [eval(k) for k in mydict]
	strength = {mydict[k]:values[k] for k in range(len(values))}

	return strength

def max_stress(stress, strength, i):
	#Determines the R values for the Max Stress Criterion
	R_max = numpy.zeros(5)

	if stress[0] > 0: #Stress_x
		R_max[0] = strength['x_t'] / stress[0]	
	else: 
		R_max[1] = strength['x_c'] / absolute(stress[0])
	if stress[1] > 0: #Stress_y
		R_max[2] = strength['y_t'] / stress[1] 
	else: 
		R_max[3] = strength['y_c'] / absolute(stress[1])
	R_max[4] = strength['s'] / absolute(stress[2])

	return R_max

def quad_poly(stress, strength, i):
	#Determines the R values for the Quadratic Criterion
	R_quad = numpy.zeros(2)

	Fxx = 1.0 / (strength['x_t'] * strength['x_c'])
	Fx = (1.0 / strength['x_t']) - (1.0 / strength['x_c'])
	Fyy = 1.0 / (strength['y_t'] * strength['y_c'])
	Fy = (1.0 / strength['y_t']) - (1.0 / strength['y_c'])
	Fss = 1.0 / (strength['s'])**2
	Fxy = (-1.0 / 2.0) * (Fxx * Fyy)**(0.5)

	#Quadratic coefficients
	a = Fxx * (stress[0])**2 + 2 * Fxy * stress[0] * stress[1] + Fyy * (stress[1])**2 + Fss * (stress[2])**2
	b = Fx * stress[0] + Fy * stress[1] 
	c = -1

	R_quad[0], R_quad[1] = solve_quadratic(a, b, c, i)

	return R_quad

def hashin_crit(stress, strength, i):
	#Determines the R values for the Hashin Criterion
	R_hash = numpy.zeros(4)

	if stress[0] > 0: #Stress_x
		R_hash[0] = (1/((stress[0]/strength['x_t'])**2 + (stress[2]/strength['s'])**2))**(0.5)	
	else: 
		R_hash[1] = strength['x_c'] / absolute(stress[0])
	
	if stress[1] > 0: #Stress_y
		R_hash[2] = (1/((stress[1]/strength['y_t'])**2 + (stress[2]/strength['s'])**2))**(0.5) 
	else: 
		a = (stress[1]/(2.0 * strength['s']))**2 + (stress[2]/strength['s'])**2
		b = (stress[1]/strength['y_c']) * ((strength['y_c']/(2.0 * strength['s']))**2 - 1)
		c = -1
		R_hash[3], dummy = solve_quadratic(a, b, c, i) #Negative root is not used in the Hashin Criterion  	

	return R_hash	

def find_min(dataframe, columns):
	#Find the minimum R values for each criteron and the failure modes
    plys = []; values = []; modes = []
    data_columns = dataframe[columns]
    nonzero_data = data_columns[data_columns != 0]

    for col in columns:
        one_col_data = nonzero_data[col]
        min_index = one_col_data.idxmin()
        try:
        	values.append(one_col_data.iloc[min_index])
        	plys.append(dataframe[['Ply','Angle','Pos']].iloc[min_index])
        	modes.append(col)
        except ValueError:
        	pass
        
        

    lowest_index = numpy.array(values).argmin()

    text_mode = failure_mode(modes[lowest_index])
    
    return values[lowest_index], plys[lowest_index], text_mode

def failure_mode(i):
	#Based on all of the possible failure modes, returns corresponding one	

	if i == 'max_FT' or i == 'hash_FT':
		x = 'Fiber Tension'
	elif i == 'max_FC' or i == 'hash_FC':
		x = 'Fiber Compression'
	elif i == 'max_MT' or i == 'hash_MT':
		x = 'Matrix Tension'
	elif i == 'max_MC' or i == 'hash_MC':
		x = 'Matrix Compression'
	elif i == '(+)' or i == '(-)':
		x = 'Quadratic cannot identify failure mode!'	
	else: #i = 'max_S'
		x = 'Shear'

	return x	  								