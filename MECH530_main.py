#Elaine Craigie - 260476434
#MECH 530 - Mechanics of Composite Materials
#Fall 2014 Ongoing Project

#Created by Elaine Craigie, Fall 2014
import MECH530_getplybook #Contains all functions related to reading and sorting raw plybook data to final plybook.
import MECH530_print #Contains all print statements
import MECH530_matrices #Contains all calculations related to Q, S, A and U matrix/vector properties
import MECH530_input #Contains all scripts related to input commands
import MECH530_failure #Contains all scripts related to failure analysis

#Existing modules/classes
import numpy #Allows me to create arrays that can be nicely formatted when printed

#Regular commands - outputs for every single assignment
plies, h_laminate, h_core, plybook = MECH530_getplybook.getplybook() #Get sorted plybook, total number of plies, thickness of core and laminate 
plybook = MECH530_getplybook.append_material_properties(plies, plybook) #Get newly appended plybook with material properties assigned to each ply
materials_used, num_materials = MECH530_getplybook.count_laminate_materials(plies, plybook) #Get dictionary of materials used and size of dictionary
A, A_comp, D, D_comp = MECH530_matrices.compute_A_D(plybook, plies, h_laminate, h_core)
MECH530_print.print_init(plies, h_laminate, h_core, plybook, materials_used, num_materials, A, A_comp, D, D_comp) #Prints all regular outputs require

# __________________________________ASSIGNMENT 6 - Nov 15______________________________________________
case = 1
stress_applied, stress_type, moment_applied, moment_type = MECH530_input.input_loads(case) #Contains applied stress and type (in [N] and [N/m])

if moment_type != "NO" or stress_type != "NO":
	#Get the stress and R values in table and array formats
	stress_state, R_fail, stress_df1, failure_df1 = MECH530_print.print_loadapplied(case, plybook, plies, stress_applied, stress_type, moment_applied, moment_type, A, A_comp, D, D_comp, h_laminate) #Will determine other components of stress and strain
	#Identify the minimum R's along with their corresponding failure modes
	max_stress_crit1, quad_poly_crit1, hashin_crit1 = MECH530_print.print_failure_modes(failure_df1, stress_applied, moment_applied)
print "------------------------------------------------------------------------------"

case = 2
stress_applied, stress_type, moment_applied, moment_type = MECH530_input.input_loads(case) #Contains applied stress and type (in [N] and [N/m])

if moment_type != "NO" or stress_type != "NO":
	#Get the stress and R values in table and array formats
	stress_state, R_fail, stress_df2, failure_df2 = MECH530_print.print_loadapplied(case, plybook, plies, stress_applied, stress_type, moment_applied, moment_type, A, A_comp, D, D_comp, h_laminate) #Will determine other components of stress and strain
	#Identify the minimum R's along with their corresponding failure modes
	max_stress_crit2, quad_poly_crit2, hashin_crit2 = MECH530_print.print_failure_modes(failure_df2, stress_applied, moment_applied)
print "------------------------------------------------------------------------------"			

# __________________________________ASSIGNMENT 4 - Oct 21______________________________________________
# stress_applied, stress_type, moment_applied, moment_type = MECH530_input.input_loads() #Contains applied stress and type

# if moment_type != "NO" or stress_type != "NO":
#  	max_strain_on_x = MECH530_print.print_loadapplied(plybook, plies, stress_applied, stress_type, moment_applied, moment_type, A, A_comp, D, D_comp, h_laminate) #Will determine other components of stress and strain

# print "CHECK DESIGN CRITERION:\n"
# #Check Design criterion in problem definition
# L = 0.52 #[m]
# b = 0.10 #[m]
# P = -225.0 * 9.81

# crit1 = -0.005 #[m], max deflection at midpoint of board
# crit2 = 0.002 #max strain on the fibers (ie: in the fiber direction) --> strain,x, this is validated using "check" = 0, means satisfied

# deflection = P * L**3 * 10**(-9) * D_comp[0][0] / (48.0 * b) #Convert D_comp from 1/GNm to 1/Nm

# print "The deflection at the midpoint is: %.4f mm" %(deflection*1000.0)
# print "The maximum strain along the fibers is: %.4f" %(max_strain_on_x)

# if abs(deflection) > abs(crit1) or max_strain_on_x > crit2:
# 	print "\nTherefore the design will NOT meet the requirements!\n"
# else:
# 	print "\nTherefore the design DOES meet the necessary requirements!\n"	
# print "------------------------------------------------------------------------------"	