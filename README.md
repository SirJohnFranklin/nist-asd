# nist-asd
Basically a class which parses the NIST Atomic Spectra Database and saves the data to a dictionary on HDD. 

- You can pass an matplotlib.axis, and the emissions lines will be plotted with an optional normalization factor
- You can plot the data directly
- You can print the atomic data and access it

Example usage:

```python
>>> pip install nist-asd

from nist_asd import NISTLines
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
```

Results in:
```
NISTLines : searching for saved spectrum in nist_asd/NIST_data/
NISTLines : found spectrum in ist_asd/NIST_data/
Number of lines:  5829
Number of lines within range:  20
Line data within range:
{'Acc': 'B',
 'Aki': 29400000000.0,
 'Ei': 0.0,
 'Ek': 72.01311,
 'gi': 1.0,
 'gk': 3.0,
 'lower_J': '0',
 'lower_conf': '1s2.2s2',
 'lower_term': '1S',
 'rel_int': 450.0,
 'rel_int_com': '',
 'section': 0,
 'spectrum': 'O '
             'V',
 'type': '',
 'upper_J': '1',
 'upper_conf': '1s2.2s.3p',
 'upper_term': '1P*',
 'wave': 17.2169,
 'wave_obs': 17.2169,
 'wave_ritz': 17.2169}

{'Acc': 'A',
 'Aki': 73300000000.0,
 'Ei': 11.94898,
 'Ek': 83.64293,
 'gi': 2.0,
 'gk': 4.0,
 'lower_J': '1/2',
 'lower_conf': '1s2.2p',
 'lower_term': '2P*',
 'rel_int': nan,
 'rel_int_com': '',
 'section': 0,
 'spectrum': 'O '
             'VI',
 'type': '',
 'upper_J': '3/2',
 'upper_conf': '1s2.3d',
 'upper_term': '2D',
 'wave': 17.2935,
 'wave_obs': nan,
 'wave_ritz': 17.2935}

{'Acc': 'A',
 'Aki': 87800000000.0,
 'Ei': 12.015,
 'Ek': 83.64926,
 'gi': 4.0,
 'gk': 6.0,
 'lower_J': '3/2',
 'lower_conf': '1s2.2p',
 'lower_term': '2P*',
 'rel_int': nan,
 'rel_int_com': '',
 'section': 0,
 'spectrum': 'O '
             'VI',
 'type': '',
 'upper_J': '5/2',
 'upper_conf': '1s2.3d',
 'upper_term': '2D',
 'wave': 17.3079,
 'wave_obs': nan,
 'wave_ritz': 17.3079}

{'Acc': 'A',
 'Aki': 14600000000.0,
 'Ei': 12.015,
 'Ek': 83.64293,
 'gi': 4.0,
 'gk': 4.0,
 'lower_J': '3/2',
 'lower_conf': '1s2.2p',
 'lower_term': '2P*',
 'rel_int': nan,
 'rel_int_com': '',
 'section': 0,
 'spectrum': 'O '
             'VI',
 'type': '',
 'upper_J': '3/2',
 'upper_conf': '1s2.3d',
 'upper_term': '2D',
 'wave': 17.3095,
 'wave_obs': nan,
 'wave_ritz': 17.3095}

{'Acc': 'D',
 'Aki': 8050000.0,
 'Ei': 28.72979,
 'Ek': 100.2929,
 'gi': 5.0,
 'gk': 7.0,
 'lower_J': '2',
 'lower_conf': '1s2.2p2',
 'lower_term': '1D',
 'rel_int': nan,
 'rel_int_com': '',
 'section': 0,
 'spectrum': 'O '
             'V',
 'type': '',
 'upper_J': '3',
 'upper_conf': '1s2.2s.5f',
 'upper_term': '1F*',
 'wave': 17.3252,
 'wave_obs': nan,
 'wave_ritz': 17.3252}
```
