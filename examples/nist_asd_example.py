from nistasd import NISTLines
import matplotlib.pyplot as plt

if __name__ == '__main__':
    nist = NISTLines(spectrum='O', lower_wavelength=2., upper_wavelength=50., order=1)

    # plotting to existing axis with scaling parameter
    plt.figure()
    ax = plt.gca()
    nist.plot_nist_lines_to_axis(ax, normalize_max=10.)
    plt.grid()
    
    # plotting lines to new window
    nist.plot_lines()
    plt.savefig('nist-asd-example-plot.pdf')
    plt.show()

    # printing information
    nist = NISTLines(spectrum='O', lower_wavelength=17.20, upper_wavelength=17.35, order=1)
    lines = nist.get_lines()
    print("Number of lines: ", len(lines))
    
    lines_within_range = nist.get_lines_wavelength_range()
    print("Number of lines within range: ", len(lines_within_range))
    
    print("Line data within range:")
    nist.pprint()