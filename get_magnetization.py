
import os
import datetime
import sys
import argparse
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from create_data import generate_params


def get_magnetization(filename, temps, args):
    # pylint: disable=consider-using-enumerate
    # open the file
    spin_config_file = open(  # pylint: disable=unspecified-encoding
        filename, 'r')

    avg_magetizations = {}
    magetizations_err = {}

    for i in range(len(temps)):
        temp = float(temps[i])
        magetizations = []
        # read the spin configurations for the temperature
        for j in range(args.bin_size):
            spin_config = spin_config_file.readline().split()
            spin_config = [int(spin) for spin in spin_config]

            # calculate the magnetization
            magetization = np.square(
                np.sum(spin_config))/np.square(len(spin_config))
            magetizations.append(magetization)
            # print(magetization)
        # plot a histogram of the magnetizations
        # mean = np.mean(magetizations)
        # std_dev = np.std(magetizations)
        # # clear the figure
        # plt.clf()
        # plt.hist(magetizations, bins=50)
        # plt.xlabel('Magnetization')
        # plt.ylabel('Frequency')
        # plt.title('Magnetization Histogram for T = ' + str(temp) +
        #           ' mean = ' + str(mean) + ' std dev = ' + str(std_dev))
        # # save the histogram
        # plt.savefig('./magnetization_' + str(temp) + '.pdf', format='pdf')
        # calculate the average magnetization for the temperature
        avg_magetization = np.mean(magetizations)
        # print(avg_magetization)
        avg_magetizations[temp] = avg_magetization

        # calculate the error in the magnetization for the temperature
        magetization_err = np.std(magetizations)/np.sqrt(args.bin_size)
        # print(magetization_err)
        magetizations_err[temp] = magetization_err

    # close the file
    spin_config_file.close()

    return avg_magetizations, magetizations_err


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lattice_size', type=int, nargs='+', default=[
                        25, 25], help='Size of the lattice to generate spin configurations for')
    parser.add_argument('--min_temp', type=float, nargs='?',
                        default=1.0, help='Minimum temperature to generate data for')
    parser.add_argument('--max_temp', type=float, nargs='?',
                        default=5.0, help='Maximum temperature to generate data for')
    parser.add_argument('-b', '--bin_size', type=int, default=10,
                        help='Number of spin configurations to generate for each temperature')
    parser.add_argument('--increment', type=float, nargs='?', default=0.1,
                        help='Increment to use when generating temperatures')

    args = parser.parse_args()

    # get list of temperatures to generate data for from min_temp to max_temp
    temps = [args.min_temp + i*args.increment for i in range(
        int((args.max_temp - args.min_temp)/args.increment) + 1)]

    # generate a parameter file for the temperatures
    filename = 't' + str(temps[0]) + '-t' + str(temps[-1]) + \
        datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    param_file = generate_params(
        temps, filename, args.bin_size, args.lattice_size)

    # run the ON_Model to generate spin configurations
    print('Running ON_Model to generate spin configurations...')
    sys.stdout.flush()

    model_args = ['./on', filename]
    subprocess.run(model_args, cwd='./ON_Model/', check=True)
    print('Spin configurations generated.')
    sys.stdout.flush()

    # remove the parameter file
    os.remove(param_file)

    spin_config_file = './ON_Model/spinConfigs_' + filename + '.txt'

    # get the magnetization for each temperature
    avg_magetizations, magetizations_err = get_magnetization(
        spin_config_file, temps, args)
    # print(avg_magetizations)
    # print(magetizations_err)

    os.remove(spin_config_file)

    # plot the magnetization vs temperature
    fig, ax = plt.subplots()

    ax.errorbar(list(avg_magetizations.keys()), list(avg_magetizations.values(
    )), yerr=list(magetizations_err.values()), marker='o', color='black')
    #add a vertical line at T = 2.269
    ax.axvline(x=2.269, color='red', linestyle='--')
    #label the vertical line
    ax.text(2.269, 1, '{crit}'.format(crit=r'$T_C \approx2.269...J/k_B$'), verticalalignment='center')
    plt.xlabel('Temperature ({unit})'.format(unit=r'$k_BT/J$'))
    plt.ylabel('Magnetization ')

    matplotlib.rcParams['pdf.fonttype'] = 42

    fig.savefig('./magnetization.pdf', format='pdf')


if __name__ == '__main__':
    main()
