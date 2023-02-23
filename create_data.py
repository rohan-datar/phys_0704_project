"""
This scrip creates training data for the neural network by running the ON_Model to generate spin configurations. 
The user can set the bin size, the lattice size, and the range of temperatures to generate data for.
-b, --bin_size: the number of spin configurations to generate for each temperature
-l --lattice_size: the size of the lattice to generate spin configurations for
--min_temp: the minimum temperature to generate data for
--max_temp: the maximum temperature to generate data for
--increment: the increment to use when generating temperatures
--train: if this flag is set, the spin configurations will be moved to the training data directory by default the spin configurations will be moved to the training data directory
--test: if this flag is set, the spin configurations will be moved to the test data directory

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
import subprocess
import shutil
import os
import datetime

CRITICAL_TEMP = 2.269

"""Generate a parameter file for the ON_Model"""
def generate_params(temps, filename, bin_size, lattice_size):

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
    param_file_name = './ON_Model/params_' + filename + '.txt'
    param_file = open(param_file_name, 'w')

    #format the parameter file
    l1 = '#	SIMULATION PARAMETERS\n'
    l2 = '           Temperature List = ' + str(temps) + '\n'
    l3 = '                        Seed = ' + str(seed) +  '\n'
    l4 = '   Number of Warm-up Sweeps = ' + str(num_warmup_sweeps) + '\n'
    l5 = '     Sweeps per Measurement = ' + str(num_sweeps) + '\n'
    l6 = '       Measurements per Bin = ' + str(per_bin_measurements) + '\n'
    l7 = '             Number of Bins = ' + str(num_bins) + '\n'
    l8 = '         Dimension of Spins = ' + str(spin_dim) + '\n'
    l9 = '       Print Spins Configs? = '+ str(print_spin_config) + '\n\n'
    l10 = '# LATTICE PARAMETERS\n'
    l11 = '                D = ' + str(dim) + '\n'
    l12 = '                L = ' + str(lattice_size) + '\n\n'
    l13 = '# MODEL PARAMETERS\n'
    l14 = '                J = ' + str(J_param) + '\n'
    l15 = '                h = ' + str(h)

    #write the simulation parameters to the parameter file
    param_file.writelines([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15])

    param_file.close()

    return param_file_name

"""Add a label to each spin configuration"""
def label_spin_configs(data_dir, filename, temps):
    
        #open the spin configuration file
        spin_config_file = open(data_dir + '/spinConfigs_' + filename + '.txt', 'r')
    
        #create a new file to hold the spin configurations with labels
        spin_config_file_labeled = open(data_dir + '/spinConfigs_' + filename + '_labeled.txt', 'w')
    
        #get the number of spin configurations in the file

      


"""Run the ON_Model to generate spin configurations"""
def run_model(args):
    
    #get list of temperatures to generate data for from min_temp to max_temp
    temps = [args.min_temp + i*args.increment for i in range(int((args.max_temp - args.min_temp)/args.increment) + 1)]

    #generate a parameter file for the temperatures
    filename = 't' + str(temps[0]) + '-t' + str(temps[-1]) + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    param_file = generate_params(temps, filename, args.bin_size, args.lattice_size)

    #run the ON_Model to generate spin configurations
    print('Running ON_Model to generate spin configurations...')
    sys.stdout.flush()  

    model_args = ['./on', filename]
    subprocess.run(model_args, cwd='./ON_Model/')
    print('Spin configurations generated.')
    sys.stdout.flush()

    #remove the parameter file
    os.remove(param_file)

    #move the spin configurations to the data directory
    print('Moving spin configurations to data directory...')
    sys.stdout.flush()
    spin_config_file = './ON_Model/spinConfigs_' + filename + '.txt'
    shutil.copy(spin_config_file, args.data_dir)
    os.remove(spin_config_file)
    print('Spin configurations moved to data directory.')

    #add a label to each spin configuration
    print('Adding labels to spin configurations...')
    sys.stdout.flush()
    label_spin_configs(args.data_dir, filename, temps)


    

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bin_size', type=int, default=10, help='Number of spin configurations to generate for each temperature')
    parser.add_argument('-l', '--lattice_size', type=int, nargs='+', default=[25,25], help='Size of the lattice to generate spin configurations for')
    parser.add_argument('--increment', type=float, nargs='?', default=0.1, help='Increment to use when generating temperatures')
    parser.add_argument('--min_temp', type=float, nargs='?', default=1.0, help='Minimum temperature to generate data for')
    parser.add_argument('--max_temp', type=float, nargs='?', default=5.0, help='Maximum temperature to generate data for')
    parser.add_argument('--train', action='store_true', help='If this flag is set, the spin configurations will be moved to the training data directory by default the spin configurations will be moved to the training data directory')
    parser.add_argument('--test', action='store_true', help='If this flag is set, the spin configurations will be moved to the test data directory')
    args = parser.parse_args()

    # check whether the user has specified a test or training set
    if args.train and args.test:
        print('Error: Cannot specify both --train and --test')
        sys.exit(1)
    elif args.train:
        args.data_dir = './data/train/'
    elif args.test:
        args.data_dir = './data/test/'
    else:
        args.data_dir = './data/train/'

    # Run the ON_Model to generate spin configurations
    run_model(args)


       
if __name__ == '__main__':
    main()
