#Contains: print_init
import numpy
import MECH530_matrices
import MECH530_failure
import pandas as pd

def print_init(plies, h_laminate, h_core, plybook, materials_used, num_materials, A, A_comp, D, D_comp):
	#Prints all output values required from the first assignment

	#plybook
	print "PLYBOOK (READ FROM EXCEL FILE AND SUMMARIZED HERE)"
	print "\nThe laminate is given by the following plybook where the highest ply number '%d' indicates the top layer, while the first ply number '1' indicates the bottom layer. \n" %plies
	reverse_counter = plies #reverse_counter is needed since I have stored my plybook from top to bottom but the converse is how the plies should be labelled
	print "Unique Ply #, Fiber/Matrix, Orientation, Thickness"
	print "                             (degrees)      (mm)"
	while reverse_counter > 0: #print material, unique ply number, orientation AND material properties
		print "%6d%19s%10d%14.3f" %(reverse_counter, plybook[plies - reverse_counter][1], plybook[plies - reverse_counter][2], plybook[plies - reverse_counter][3])
		reverse_counter -= 1	

	# State how many materials are used in the laminate and iterate on material properties
	# THICKNESS VARIABLES
	print "\nPLIES AND THICKNESSES"
	#print "-Total number of plies in the laminate: %d \n" % plies
	if h_core == 0:
		print "-Total number of plies in the laminate: %d \n-Total thickness of laminate is: %.3f mm \n-There is no core in the laminate (Zc = 0 mm)" % (plies, h_laminate)
	if h_core != 0:
		print "-Total number of plies in the laminate: %d \n-Total thickness of laminate is: %.3f mm \n-The core thickness is 2 Zc = %.3f mm \n-Note that the CORE will be ommitted in the following stress and safety factor tables" %(plies, h_laminate, h_core)
	if num_materials != 1:
		print "-Laminate contains %d Fiber/Matrix combinations. The material properties for each combination used shall be listed below." % num_materials
	else:
		print "-Laminate contains %d Fiber/Matrix combination. The material properties for this combination shall be listed below." % num_materials
	print "\n------------------------------------------------------------------------------"
	print "MATERIALS AND MATERIAL PROPERTIES"
	num_materials_counter = 1
	while num_materials_counter <= num_materials:
		print "\nRESIN/MATRIX %d of %d: For %s, the given material properties are:" % (num_materials_counter, num_materials, materials_used[num_materials_counter]) 
		i = 0
		while i < plies:
			if plybook[i][1] == materials_used[num_materials_counter]:
				break
			i += 1			

		Us = plybook[i][17] 
		Uq = plybook[i][18]
		#material properties (MAY HAVE TO CHANGE THESE IF MATERIAL IS NOT CONSISTANT THROUGHOUT THE LAMINATE)
		print """\n-Stiffness and Strength: 
		\nEx = %8.4f GPa, Ey = %8.4f GPa, Es = %8.4f GPa and nu_x = %8.4f
		\nXt = %8.4f MPa, Xc = %8.4f MPa, Yt = %8.4f MPa, Yc = %8.4f MPa and Sc = %8.4f MPa.""" %(plybook[i][4], plybook[i][5], plybook[i][6], plybook[i][7], plybook[i][8], plybook[i][9], plybook[i][10], plybook[i][11], plybook[i][12])
		engineering_formatter = lambda x: "%9.4f" % x if x != 0 else "%9.1f" % x
		numpy.set_printoptions(formatter = {'float_kind':engineering_formatter})
		print "\n-The 'on-axis' matrices are given by the following:"
		print "S_on = " 
		print plybook[i][13] , "[1/GPa]\n"	
		print "Q_on ="
		print plybook[i][14] , "[GPa]"
		print "\n-The linear combinations of the modulus, independent of ply angle are the following:"
		print "Us_1 = %9.4f [1/GPa]" % Us[0][0]
		print "Us_2 = %9.4f [1/GPa]" % Us[0][1]
		print "Us_3 = %9.4f [1/GPa]" % Us[0][2]
		print "Us_4 = %9.4f [1/GPa]" % Us[0][3]
		print "Us_5 = %9.4f [1/GPa]" % Us[0][4]
		print "\n-The linear combinations of the modulus, dependent on ply angle are the following:"
		print "Uq_1 = %9.4f GPa" % Uq[0][0]
		print "Uq_2 = %9.4f GPa" % Uq[0][1]
		print "Uq_3 = %9.4f GPa" % Uq[0][2]
		print "Uq_4 = %9.4f GPa" % Uq[0][3]
		print "Uq_5 = %9.4f GPa" % Uq[0][4]
		num_materials_counter += 1		
		print "\n-The 'Stiffness' [A] and 'Compliance' [a] matrices are given by the following:"
		print "A ="
		print A, "[GN/m]\n"
		print "a ="
		print A_comp, "[m/GN]"
		print "\n-The 'In-Plane Flexural Modulus' [D] and 'In-Plane Flexural Compliance' [d] matrices are given by the following:"
		print "D ="
		print 10**6 * D, "[kNm]\n"
		print "d ="
		print 10**(-3) * D_comp, "[1/MNm]"
		print "\n------------------------------------------------------------------------------"
 
def print_nostress(plybook, plies):
#Prints off the [Q] and [S] off-axis matrices for the first 4 layers of the given layup	
	print "\nNow the off-axis [S] and [Q] matrices will be printed for each of the first 4 layers in the layup (from the top) along with their respective [U] values."
	i = 0
	while i <= 3:
		print "\nPLY: %d" % (plies-i)
		print "ORIENTATION: %d degrees" % plybook[i][2]

		engineering_formatter = lambda x: "%9.4f" % x if x != 0 else "%9.1f" % x
		numpy.set_printoptions(formatter = {'float_kind':engineering_formatter})
		Us = plybook[i][17] 
		Uq = plybook[i][18]

		print "Us_1 = %9.4f [1/GPa]" % Us[0][0]
		print "Us_2 = %9.4f [1/GPa]" % Us[0][1]
		print "Us_3 = %9.4f [1/GPa]" % Us[0][2]
		print "Us_4 = %9.4f [1/GPa]" % Us[0][3]
		print "Us_5 = %9.4f [1/GPa]" % Us[0][4]
		print "\nS_off = " 
		print plybook[i][15] , "[1/GPa]\n"
		print "Uq_1 = %9.4f GPa" % Uq[0][0]
		print "Uq_2 = %9.4f GPa" % Uq[0][1]
		print "Uq_3 = %9.4f GPa" % Uq[0][2]
		print "Uq_4 = %9.4f GPa" % Uq[0][3]
		print "Uq_5 = %9.4f GPa" % Uq[0][4]			
		print "\nQ_off ="
		print plybook[i][16] , "[GPa]"
		i += 1
	return 

def print_loadapplied(case, plybook, plies, stress_applied, stress_type, moment_applied, moment_type, A, A_comp, D, D_comp, h_laminate):

	#Find the stress, strain and failure criterion R values	
	i = 0

	engineering_formatter = lambda x: "%9.4f" % x if x != 0 else "%9.1f" % x
	numpy.set_printoptions(formatter = {'float_kind':engineering_formatter})

	if (stress_type == 'OFF' or stress_type == 'NO') and (moment_type == 'OFF' or moment_type == 'NO'):		
		K = 10**(-9) * D_comp.dot(moment_applied) #Now this will be in [m] since D_comp is in 

		strain_off_av = 10**(-9) * A_comp.dot(stress_applied) #Convert [a], [m/GN] --> [m/N]. This is now unitless

		if case == 1:
			print "OFF-AXIS APPLIED RESULTANTS: CASE 1"
		elif case == 2:	
			print "OFF-AXIS APPLIED RESULTANTS: CASE 2"	
		elif case == 3:
			print "OFF-AXIS APPLIED RESULTANTS: CASE 3" 	
		else:	
			print "OFF-AXIS APPLIED RESULTANTS"		
		print "\nCurvature K ="
		print K.T, "[1/m]"	 
		print "\n(INPUT) Off-axis Applied stress resultant N = "
		print stress_applied.T, "[N/m]"
		print "\n(INPUT) Off-axis Applied moment resultant M = "
		print moment_applied.T, "[N]"		

		h = h_laminate / 2.0
		position = {'1':'TOP', '0':'BOTTOM'}
		while i < plies:
			temp_env = numpy.zeros(2) #Contains my ply number, and angle

			if plybook[i][1] == 'CORE':
				h -= plybook[i][3] #Subtract the thickness of the core 
			else:	
				position_counter = 1 #Start at the top

				while position_counter > -1:
					strain_off = strain_off_av + (h * K / 1000.0) #Convert thickness to m 
					stress_on, strain_on = MECH530_matrices.convert_to_on_axis(plybook, i, strain_off)

					strength = MECH530_failure.failure_props(plybook, i)
					max_R = MECH530_failure.max_stress(stress_on, strength, i)
					quad_R = MECH530_failure.quad_poly(stress_on, strength, i)
					hash_R = MECH530_failure.hashin_crit(stress_on, strength, i)

					temp_env[0] = plies-i
					temp_env[1] = plybook[i][2] #The angle		

					temp_R = numpy.hstack((temp_env, max_R, quad_R, hash_R))	
					temp_stress = numpy.hstack((temp_env, strain_off.flatten(), strain_on.flatten(), stress_on.flatten()))

					if position_counter == 0: #We've just done the bottom of a ply
						h == h
						R_fail = numpy.vstack((R_fail, temp_R))
						stress_state = numpy.vstack((stress_state, temp_stress)) #Creates an array full of stresses and strains
					else: #We've just done the top of a ply and we want to do the bottom next
						h -= plybook[i][3] #Subtract the thickness of a ply
						if i == 0: #We need to create the R_fail and result matrices
							R_fail = temp_R
							stress_state = temp_stress
						else:
							R_fail = numpy.vstack((R_fail, temp_R))
							stress_state = numpy.vstack((stress_state, temp_stress))

					position_counter -= 1		

			i += 1			
	else:
		pass	

	#Stress DataFrame
	stress_df = pd.DataFrame(data = stress_state, 
					columns = ['Ply','Angle','e_1','e_2','e_3',
									'e_x','e_y','e_z',
									'Sigma_x (GPa)','Sigma_y (GPa)','Sigma_z (GPa)'
							]
					)
	pos = [k for i in range(len(stress_df)/2) for k in ['TOP','BOT'] ]

	stress_df['Pos'] = pos
	stress_df.set_index('Pos', inplace = True)

	#Failure R values DataFrame
	failure_df = pd.DataFrame(data = R_fail, 
					columns = ['Ply','Angle','max_FT','max_FC','max_MT',
									'max_MC','max_S','(+)','(-)',
									'hash_FT','hash_FC','hash_MT','hash_MC'
							]
					)

	failure_df['Pos'] = pos
	#failure_df.set_index('Pos', inplace = True)	

	return stress_state, R_fail, stress_df, failure_df

def print_failure_modes(failure_df, stress_applied, moment_applied):
	#Prints the minimum R's for each criterion and states the failure mode (where applicable)
	max_stress = MECH530_failure.find_min(failure_df, ['max_FT','max_FC','max_MT','max_MC','max_S'])
	quad_poly = MECH530_failure.find_min(failure_df, ['(+)'])
	hashin_crit = MECH530_failure.find_min(failure_df, ['hash_FT','hash_FC','hash_MT','hash_MC'])

	print "\nFAILURE CRITERION AND ANALYSIS"

	print "\nMAXIMUM STRESS:"
	print "-Minimum R = %.3f and laminate fails in %s at %s of ply %d" %(max_stress[0], max_stress[2], max_stress[1]['Pos'], max_stress[1]['Ply'])
	print "-The load vectors which cause the failure are:"
	print "R*N = "
	print 10**(-3) * max_stress[0] * stress_applied.T, "[kN/m]" #Stress and Moment applied [N/m] and [N] --> [kN/m] and [kN]
	print "R*M = "
	print 10**(-3) * max_stress[0] * moment_applied.T, "[kN]"

	print "\nQUADRATIC POLYNOMIAL:"
	print "-Minimum R = %.3f and laminate fails at %s of ply %d" %(quad_poly[0], quad_poly[1]['Pos'], quad_poly[1]['Ply'])
	print "-The load vectors which cause the failure are:"
	print "R*N = "
	print 10**(-3) * quad_poly[0] * stress_applied.T, "[kN/m]"
	print "R*M = "
	print 10**(-3) * quad_poly[0] * moment_applied.T, "[kN]"	

	print "\nHASHIN CRITERION:" 
	print "-Minimum R = %.3f and laminate fails in %s at %s of ply %d" %(hashin_crit[0], hashin_crit[2], hashin_crit[1]['Pos'], hashin_crit[1]['Ply'])
	print "-The load vectors which cause the failure are:"
	print "R*N = "
	print 10**(-3) * hashin_crit[0] * stress_applied.T, "[kN/m]"
	print "R*M = "
	print 10**(-3) * hashin_crit[0] * moment_applied.T, "[kN]\n"	

	return max_stress, quad_poly, hashin_crit