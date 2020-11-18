import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fftfreq, fft
import numpy as np

file_locations = {'small_disk': r'C:\Users\cande\Desktop\Uni\4thYear\Masters\simulations\MultipleSTNO\synchronising disks\proper sync\195nm_14.5nm_thick.out',
                  'large_disk': r'C:\Users\cande\Desktop\Uni\4thYear\Masters\simulations\MultipleSTNO\synchronising disks\proper sync\large_disk_200nm.out',
                  'sync_disk': '200x15_195x14_100.out'}

data_small_indiv = pd.read_csv('{}/test_table.csv'.format(file_locations['small_disk']))[4000:]
data_large_indiv = pd.read_csv('{}/test_table.csv'.format(file_locations['large_disk']))[4000:]

data = pd.read_csv('table.txt')
data.to_csv('test_table.csv')

data_sync = pd.read_csv('test_table.csv', sep='\t')[4000:]

## Data from running STNO's on ther own
t_small = data_small_indiv.iloc[:, 1]
t_large = data_large_indiv.iloc[:, 1]
mx_small = data_small_indiv.iloc[:, 2]
mx_large = data_large_indiv.iloc[:, 2]

t_sync = data_sync.iloc[:, 1]
mx_small_sync = data_sync.iloc[:, 8]
mx_large_sync = data_sync.iloc[:, 5]
mx_sync = data_sync.iloc[:, 2]


def plot_peaks_and_overall():
    ## Carry out FFT

    f_ss = len(mx_small) / t_small.iloc[-1]
    f_sl = len(mx_large) / t_large.iloc[-1]
    f_sc = len(mx_sync) / t_sync.iloc[-1]

    xs = fft(list(mx_small))
    xl = fft(list(mx_large))
    xc = fft(list(mx_sync))

    freqs = fftfreq(len(mx_small)) * f_ss
    freql = fftfreq(len(mx_large)) * f_sl
    freqc = fftfreq(len(mx_sync)) * f_sc

    ## Plot each on the same figure

    # plt.xlim(left=4.9e8, right=7.5e8)

    plt.scatter(freqs, np.abs(xs), label='Small')
    plt.scatter(freql, np.abs(xl), label='Large')
    plt.scatter(freqc, np.abs(xc), label='Syncronised')

    plt.legend()

    plt.title('STNO individual frequencies against overall synchronised')
    plt.xlabel('Frequency (100 MHz)')

    plt.savefig('indiv_vs_overall.png')
    plt.show()

    return


def plot_peak_with_shift():
    ## FFT the disks

    f_ss = len(mx_small) / t_small.iloc[-1]
    f_sl = len(mx_large) / t_large.iloc[-1]
    f_sc = len(mx_small_sync) / t_sync.iloc[-1]

    xs = fft(list(mx_small))
    xl = fft(list(mx_large))
    xss = fft(list(mx_small_sync))
    xls = fft(list(mx_large_sync))

    freqs = fftfreq(len(mx_small)) * f_ss
    freql = fftfreq(len(mx_large)) * f_sl
    freqss = fftfreq(len(mx_small_sync)) * f_sc
    freqls = fftfreq(len(mx_large_sync)) * f_sc

    ## Plot the small disk

    # plt.xlim(left=4.9e8, right=7.5e8)

    plt.scatter(freqs, np.abs(xs), label='Individual')
    plt.scatter(freqss, np.abs(xss), label='Synchronised')

    plt.legend()

    plt.title('195nm diam / 14.5nm thick disk individual vs with other')
    plt.xlabel('Frequency (100 MHz)')

    plt.savefig('smallindiv_vs_withother.png')
    plt.show()
    ## Plot large disk

    plt.xlim(left=4.9e8, right=7.5e8)

    plt.scatter(freql, np.abs(xl), label='Individual')
    plt.scatter(freqls, np.abs(xls), label='Synchronised')

    plt.legend()

    plt.title('200nm diam / 15nm thick disk individual vs with other')
    plt.xlabel('Frequency (100 MHz)')

    plt.savefig('largeindiv_vs_withother.png')
    plt.show()

    return


def plot_all_synced():
    ## FFT

    f_sc = len(mx_small_sync) / t_sync.iloc[-1]

    xss = fft(list(mx_small_sync))
    xls = fft(list(mx_large_sync))
    xsync = fft(list(mx_sync))

    freqss = fftfreq(len(mx_small_sync)) * f_sc
    freqls = fftfreq(len(mx_large_sync)) * f_sc  # These are probably redundant after the first
    freqs = fftfreq(len(mx_sync)) * f_sc

    ## PLot All on the same plot

    plt.xlim(left=4.9e8, right=7.5e8)

    plt.scatter(freqls, np.abs(xls), label='Large')
    plt.scatter(freqss, np.abs(xss), label='Small')
    plt.scatter(freqs, np.abs(xsync), label='Total')

    plt.legend()

    plt.title('Individual and total frequencies of synced disks')
    plt.xlabel('Frequency (100 MHz)')

    plt.savefig('all_synced.png')
    plt.show()

    return


def plot_magnetisation():
    fig, axs = plt.subplots(3, sharex=True, sharey=True)

    axs[2].plot(t_sync, mx_sync)
    axs[1].plot(t_sync, mx_large_sync)
    axs[0].plot(t_sync, mx_small_sync)

    plt.savefig('magnetisation.png')

    return


if __name__ == '__main__':
    plot_peaks_and_overall()
    plot_peak_with_shift()
    plot_all_synced()
    plot_magnetisation()
