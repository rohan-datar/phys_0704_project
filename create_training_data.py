"""
This scrip creates training data for the neural network by running the ON_Model to generate spin configurations. 
The user can set the bin size, the lattice size, and the range of temperatures to generate data for.
-b, --bin_size: the number of spin configurations to generate for each temperature
-l --lattice_size: the size of the lattice to generate spin configurations for
--min_temp: the minimum temperature to generate data for
--max_temp: the maximum temperature to generate data for
--increment: the increment to use when generating temperatures

Default values are set for bin_size, lattice_size, min_temp, and max_temp.
The default values are:
--bin_size = 10
--lattice_size = [25, 25]
--increment = 0.1
--min_temp = 1.0
--max_temp = 5.0
"""

import sys
import argparse

CRITICAL_TEMP = 2.269

"""Generate a parameter file for the ON_Model"""
def generate_params(temps, bin_size, lattice_size):

    #unchange simulation parameters
    seed = 0
    num_warmup_sweeps = 1000
    num_sweeps = 200
    per_bin_measurements = 10
    num_bins = bin_size 
    spin_dim = 1
    print_spin_config = 1
    dim = len(lattice_size)
    J_param = 1
    h = 0
    
    #create a parameter file for the ON_Model
    param_file_name = 'params_t' + str(temps[0]) + '-t' + str(temps[-1]) + '.txt'
    param_file = open(param_file_name, 'w')

    #write the simulation parameters to the parameter file
    param_file.write('#	SIMULATION PARAMETERS\n           Temperature List = ' + str(temps) + '\n   Number of Warm-up Sweeps = ' + str(num_warmup_sweeps) + '\n     Sweeps per Measurement = ' + str(num_sweeps) + '\n       Measurements per Bin = ' + str(per_bin_measurements) + '\n             Number of Bins = ' + str(num_bins) + '\n         Dimension of Spins = ' + str(spin_dim) + '\n       Print Spins Configs? = '+ str(print_spin_config) + '\n\n          #	LATTICE PARAMETERS\n                D = ' + str(dim) + '\n                L = ' + str(lattice_size) + '\n\n           #	MODEL PARAMETERS\n                J = ' + str(J_param) + '\n                h = ' + str(h))

    param_file.close()

    return param_file_name


"""Run the ON_Model to generate spin configurations"""
def run_model(bin_size, 
              lattice_size, 
              min_temp, 
              max_temp, 
              increment):
    
    #get list of temperatures to generate data for from min_temp to max_temp
    temps = [min_temp + i*increment for i in range(int((max_temp - min_temp)/increment) + 1)]

    #generate a parameter file for the temperatures
    param_file = generate_params(temps, bin_size, lattice_size)

        


    

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bin_size', type=int, default=10, help='Number of spin configurations to generate for each temperature')
    parser.add_argument('-l', '--lattice_size', type=int, nargs='+', default=[25,25], help='Size of the lattice to generate spin configurations for')
    parser.add_argument('--increment', type=float, nargs='?', default=0.1, help='Increment to use when generating temperatures')
    parser.add_argument('--min_temp', type=float, nargs='?', default=1.0, help='Minimum temperature to generate data for')
    parser.add_argument('--max_temp', type=float, nargs='?', default=5.0, help='Maximum temperature to generate data for')
    args = parser.parse_args()

    # Run the ON_Model to generate spin configurations
    run_model(args.bin_size, args.lattice_size, args.min_temp, args.max_temp)


       
if __name__ == '__main__':
    main()
