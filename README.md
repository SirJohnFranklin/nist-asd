# nist-asd
Basically a class which parses the NIST Atomic Spectra Database for energy levels and lines and saves the data to a dictionary on HDD. 

- You can pass a matplotlib.axis, and the emission lines will be plotted with an optional normalization factor
- You can plot the data directly
- You can print the emission line data and access it
- You can print the energy level data and access it

Example usage:

```python
>>> pip install nist-asd

from nistasd import NISTLines, NISTASD
import matplotlib.pyplot as plt

if __name__ == '__main__':
    import pandas as pd
    
    nist = NISTLines(spectrum='N')
    energy_levels = nist.get_energy_levels()
    
    for ion_stage in energy_levels:
        print("Number of levels: {0} for {1}".format(len(energy_levels[ion_stage]), ion_stage))
        df = pd.DataFrame(energy_levels[ion_stage])
        print(df)
        
        break
    
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
[Plot result](examples/nist-asd-example-plot.pdf)


```
Number of energy levels: 366 for N I
       J  configuration        ...         term  uncertainty (eV)
0    1.5         2s22p3        ...          4S°               NaN
1    2.5         2s22p3        ...          2D°               NaN
2    1.5         2s22p3        ...          2D°               NaN
3    0.5         2s22p3        ...          2P°               NaN
4    1.5         2s22p3        ...          2P°               NaN
5    0.5   2s22p2(3P)3s        ...           4P               NaN
6    1.5   2s22p2(3P)3s        ...           4P               NaN
7    2.5   2s22p2(3P)3s        ...           4P               NaN
8    0.5   2s22p2(3P)3s        ...           2P               NaN
9    1.5   2s22p2(3P)3s        ...           2P               NaN
10   2.5          2s2p4        ...           4P               NaN
11   1.5          2s2p4        ...           4P               NaN
12   0.5          2s2p4        ...           4P               NaN
13   0.5   2s22p2(3P)3p        ...          2S°               NaN
14   0.5   2s22p2(3P)3p        ...          4D°               NaN
15   1.5   2s22p2(3P)3p        ...          4D°               NaN
16   2.5   2s22p2(3P)3p        ...          4D°               NaN
17   3.5   2s22p2(3P)3p        ...          4D°               NaN
18   0.5   2s22p2(3P)3p        ...          4P°               NaN
19   1.5   2s22p2(3P)3p        ...          4P°               NaN
20   2.5   2s22p2(3P)3p        ...          4P°               NaN
21   1.5   2s22p2(3P)3p        ...          4S°               NaN
22   1.5   2s22p2(3P)3p        ...          2D°               NaN
23   2.5   2s22p2(3P)3p        ...          2D°               NaN
24   0.5   2s22p2(3P)3p        ...          2P°               NaN
25   1.5   2s22p2(3P)3p        ...          2P°               NaN
26   2.5   2s22p2(1D)3s        ...           2D               NaN
27   1.5   2s22p2(1D)3s        ...           2D               NaN
28   0.5   2s22p2(3P)4s        ...           4P               NaN
29   1.5   2s22p2(3P)4s        ...           4P               NaN
..   ...            ...        ...          ...               ...
336  0.5   2s2p3(5S°)5p        ...           4P               NaN
337  1.5   2s2p3(5S°)5p        ...           4P               NaN
338  2.5   2s2p3(5S°)5p        ...           4P               NaN
339  0.5   2s2p3(5S°)6p        ...           4P               NaN
340  1.5   2s2p3(5S°)6p        ...           4P               NaN
341  2.5   2s2p3(5S°)6p        ...           4P               NaN
342  0.5   2s2p3(5S°)7p        ...           4P             0.012
343  1.5   2s2p3(5S°)7p        ...           4P             0.012
344  2.5   2s2p3(5S°)7p        ...           4P             0.012
345  0.5   2s2p3(5S°)8p        ...           4P               NaN
346  1.5   2s2p3(5S°)8p        ...           4P               NaN
347  2.5   2s2p3(5S°)8p        ...           4P               NaN
348  0.5   2s2p3(5S°)9p        ...           4P               NaN
349  1.5   2s2p3(5S°)9p        ...           4P               NaN
350  2.5   2s2p3(5S°)9p        ...           4P               NaN
351  0.5  2s2p3(5S°)10p        ...           4P             0.012
352  1.5  2s2p3(5S°)10p        ...           4P             0.012
353  2.5  2s2p3(5S°)10p        ...           4P             0.012
354  0.5  2s2p3(5S°)11p        ...           4P               NaN
355  1.5  2s2p3(5S°)11p        ...           4P               NaN
356  2.5  2s2p3(5S°)11p        ...           4P               NaN
357  0.5  2s2p3(5S°)12p        ...           4P               NaN
358  1.5  2s2p3(5S°)12p        ...           4P               NaN
359  2.5  2s2p3(5S°)12p        ...           4P               NaN
360  0.5  2s2p3(5S°)13p        ...           4P               NaN
361  1.5  2s2p3(5S°)13p        ...           4P               NaN
362  2.5  2s2p3(5S°)13p        ...           4P               NaN
363  0.5  2s2p3(5S°)14p        ...           4P               NaN
364  1.5  2s2p3(5S°)14p        ...           4P               NaN
365  2.5  2s2p3(5S°)14p        ...           4P               NaN

[366 rows x 7 columns]



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
```
