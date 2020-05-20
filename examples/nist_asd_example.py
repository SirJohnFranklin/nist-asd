from nistasd import NISTLines, NISTASD
import matplotlib.pyplot as plt

if __name__ == '__main__':
    import pandas as pd

    nist = NISTLines(spectrum='N')
    energy_levels = nist.get_energy_level_data()
    print("energy_levels.keys() = ", energy_levels['N I'])
    for ion_stage in energy_levels:
        print("Number of energy levels: {0} for {1}".format(len(energy_levels[ion_stage]), ion_stage))
        df = pd.DataFrame(energy_levels[ion_stage])
        print(df)

        break

    nist = NISTLines(spectrum='Ar', lower_wavelength=8., upper_wavelength=20., order=1)

    # plotting lines to new window
    nist.plot_lines()

    # printing information
    nist = NISTLines(spectrum='O', lower_wavelength=0.1, upper_wavelength=600, order=1)
    lines = nist.get_lines()
    print("Number of lines: ", len(lines))


    lines_within_range = nist.get_lines_wavelength_range()
    print("Number of lines within range: ", len(lines_within_range))
    
    print("Line data within range:")
    nist.pprint()
    
    plt.show()