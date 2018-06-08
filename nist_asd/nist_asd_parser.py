from __future__ import print_function

import re, os, pickle, pathlib, time, sys

if sys.version_info[0] < 3:
    import urllib2 as urllib
else:
    import urllib

if sys.version_info[0] < 3:
    import HTMLParser
else:
    import html.parser as HTMLParser

import numpy as np
import matplotlib.pyplot as plt

from mpldatacursor import datacursor
from logzero import logger
from copy import copy
from math import isnan


__author__ = 'd.wilson'


def timeit(f):
    """
    use: @timeit to time functions...
    """
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        diff = te-ts
        unit = 'sec'
        if diff < 1:
            diff *= 1000.
            unit = ' msec'

        print('func:%r took: %2.4f %s' %(f.__name__, diff, unit))
        return result

    return timed


class NISTASD(object):
    # Taken from: http://intermittentshorts.blogspot.de/2012/12/nist-atomic-spectral-database-parser.html and modified.
    def __init__(self, spec='H', lowwl=0.1, uppwl=1000., order=1):
        self.spec = spec
        self.lowwl = lowwl
        self.uppwl = uppwl
        self.order = order

        self.get_asd()
        self.parse_asd()

    def get_asd(self):
        spec = self.spec
        lowwl = self.lowwl/self.order
        uppwl = self.uppwl/self.order
       
        # build the web request
        self.nist_URL = 'http://physics.nist.gov/cgi-bin/ASD/lines1.pl'
        spec_plus=spec.strip().replace(' ','+') # HTML post needs + instead of ' '
        self.post_data = ('encodedlist=XXT1XXR0q0qVqVIII' + '&' # some key to make it work?
                        + 'spectra=' + spec_plus + '&' # eg 'He' or 'He+I' or 'He+II', no spaces
                        + 'low_wl=' + str(lowwl) + '&'
                        + 'upp_wl=' + str(uppwl) + '&'
                        + 'unit=1' + '&' # wl unit 0=Angstroms, 1=nm, 2=um
                        + 'en_unit=1' + '&' # energy unit 0 cm^-1, 1 eV, 2 Rydberg
                        + 'low_wn=' + '&'
                        + 'upp_wn=' + '&'
                        + 'submit=Retrieve+Data' + '&'
                        + 'temp=' + '&'
                        + 'doppler=' + '&'
                        + 'eden=' + '&'
                        + 'iontemp=' + '&'
                        + 'java_window=3' + '&'
                        + 'java_mult=' + '&'
                        + 'tsb_value=0' + '&'
                        + 'format=1' + '&' # 0 HTML output, 1 ascii output
                        + 'remove_js=on' + '&' # cleans up output for easier parsing
                        + 'output=0' + '&' # 0 return all output, 1 return output in pages
                        + 'page_size=15' + '&'
                        + 'line_out=0' + '&' # 0 return all lines, 1 only w/trans probs, 2 only w/egy levl, 3 only w/obs wls
                        + 'order_out=0' + '&' # output ordering: 0 wavelength, 1 multiplet
                        + 'show_av=2' + '&' # show wl in Vacuum (<2000A) Air (2000-20000A) Vacuum (>20,000A)
                        + 'max_low_enrg=' + '&' # maximum lower level energy
                        + 'max_upp_enrg=' + '&' # maximum upper level energy
                        + 'min_str=' + '&' # minimum transition strength
                        + 'max_str=' + '&' # maximum transition strength
                        + 'min_accur=' + '&' # minimum line accuracy, eg AAA AA A B C
                        + 'min_intens=' + '&' # minimum relative intensity to return
                        + 'show_obs_wl=1' + '&' # show observed wavelength
                        + 'show_calc_wl=1' + '&' # show calculated (Ritz) wavelength
                        + 'A_out=0' + '&' # show $
                        + 'intens_out=on' + '&' # show relative intensity
                        + 'allowed_out=1' + '&' # show allowed transitions
                        + 'forbid_out=1' + '&' # show forbidden transitions
                        + 'conf_out=on' + '&' # show electron configuration
                        + 'term_out=on' + '&' # show terms
                        + 'enrg_out=on' + '&' # show transition energies
                        + 'J_out=on' + '&' # show J (total angular momentum)
                        + 'g_out=on' ) # show g (statistical weight?)

        # issue wget to pull the data from nist and use sed to split off the desired info
        #  -q 'quiet' suppresses wget messages
        #  -O - directs results to standard output
        self.full_URL = self.nist_URL + '?' + self.post_data # This issues as a GET instead of POST, but it works ok anyway

        self.cmd = ( 'wget -q -O - \'' + self.full_URL + '\' '
                   + '| sed -n \'/<pre*/,/<\/pre>/p\' ' # select lines between <pre> tags
                   + '| sed \'/<*pre>/d\' ' # remove <pre> lines
                   + '| iconv -f ISO-8859-1 -t ASCII' ) # convert the web encoding to something IDL can understand...
                   # '| sed \'/----*/d\'' # remove ---- lines
        #sys.spawnl(cmd)
        try:
            self.nist_read = urllib.request.urlopen(self.full_URL).readlines()
        except:
            try:
                self.nist_read = urllib.urlopen(self.full_URL).readlines()
            except AttributeError:
                print("")

        # select lines between <pre> tags as the asd_lines table
        self.asd_lines = []
        found_pre = False
        for ln in self.nist_read:
            if re.search('<.*?pre>',ln.decode('utf-8')) != None:
                found_pre = not found_pre
                continue
            if found_pre:
                # convert ISO-8859-1 to ASCII or UTF-8 or unicode or something...
                self.asd_lines.append(HTMLParser.HTMLParser().unescape(ln.decode('utf-8')) )
        if self.asd_lines == []:
            raise Exception('NoASDlines','No ASD lines were found.')


    # parse the imported asd_lines into data arrays
    def parse_asd(self):
        asd = copy(self.asd_lines)
        isec = -1
        self.header = []
        self.lines = []

        while len(asd) > 2:
            isec += 1
            self.parse_section(asd,isec)


    def parse_section(self,asd,isec = 0):
        # first do the header
        asd.pop(0)  # first line is a break...
        hd0 = [l.strip() for l in re.split(   '\|', asd[0])]
        hd0.pop()  # last value is a line break
        idx = [i.start() for i in re.finditer('\|', asd[0])] # indices for the dividers
        idx.insert(0,0)

        asd.pop(0)
        hd1 = [l.strip() for l in re.split(   '\|', asd[0])]
        hd1.pop()
        for i in range(0,len(hd0)):
            if hd0[i].find('level') == -1:
                hd0[i] += ' ' + hd1[i].strip()

        asd.pop(0)
        hd = []
        for i in range(0,len(hd0)):
            if hd0[i].find('level') == -1:
                a0 = asd[0][ idx[i]+1 : idx[i+1] ].strip()
                hd.append(hd0[i] + ' ' + a0)

            else:
                lvs = [l.strip() for l in asd[0][ idx[i]+1 : idx[i+1] ].split('|')]
                [hd.append(hd0[i] + ' ' + l) for l in lvs]
        hd = [h.strip() for h in hd]
        self.header.append(hd)

        # to identify if the first element is the Spectrum or not...
        ls = 1 if hd[0] == 'Spectrum' else 0

        # now parse associated data
        asd.pop(0)  # first line is a break...
        asd.pop(0)

        nan=float('nan')
        while re.search('-'*172, asd[0]) == None:
            l = [ l.strip() for l in re.split('\|', asd[0]) ]

            if l[0+ls] != '' or l[1+ls] != '':

                # special parsing for some fields
                str = l[2+ls]
                (ri,ric) = (str,'')
                for i in range(0,len(str)):
                    if not( str[i].isdigit() or str[i]=='(' or str[i] ==')' ):
                        (ri,ric) = (str[:i],str[i:])
                        break

                EiEk = [re.sub('[^0-9\.]','',x) for x in l[5+ls].split('-')] if l[5+ls] != '' else ['nan', 'nan']
                
                gigk = l[12+ls].split('-') if l[12+ls] != '' else [nan, nan]
                
                # parse all fields into the dictionary
                try:
                    rel_int = float(re.sub('[^0-9\.]', '', ri)) if ri != '' else nan  # non-numerics seen: \(\)
                except ValueError:
                    print(self.__class__.__name__, ": Could not convert -",re.sub('[^0-9\.]', '', ri), "- to float.")
                    rel_int = nan
                d = {'spectrum'      : l[0] if ls==1 else self.spec,
                     'wave_obs'  : float( re.sub('[^0-9\.]','',l[0+ls]) ) if l[0+ls] != '' else nan,
                     'wave_ritz' : float( re.sub('[^0-9\.]','',l[1+ls]) ) if l[1+ls] != '' else nan, # non-numerics seen: +
                     'rel_int'   : rel_int, # non-numerics seen: \(\)
                     'rel_int_com': ric,
                     'Aki'       : float( l[3+ls] ) if l[3+ls] != '' else nan,
                     'Acc'       : l[4+ls],
                     'Ei'        : float( EiEk[0] ),
                     'Ek'        : float( EiEk[1] ), # non-numerics seen: \[\]\?+xk
                     'lower_conf': l[6+ls],
                     'lower_term': l[7+ls],
                     'lower_J'   : l[8+ls],
                     'upper_conf': l[9+ls],
                     'upper_term': l[10+ls],
                     'upper_J'   : l[11+ls],
                     'gi'        : float( gigk[0] ) if gigk[0] != '' else nan,
                     'gk'        : float( gigk[1] ) if gigk[1] != '' else nan,
                     'type'      : l[14+ls],
                     'section'   : isec
                    }
                d['wave'] = d['wave_ritz'] if isnan(d['wave_obs']) else d['wave_obs']
                self.lines.append(d)

            else:
                pass # empty line

            asd.pop(0)

    def get_lines(self):
        return self.lines


class NISTLines(object):
    def __init__(self, spectrum='He', lower_wavelength=100, upper_wavelength=1000, order=1):
        super(NISTLines, self).__init__()
        self.spectrum = spectrum                    # Species
        self.lower_wavelength = lower_wavelength    # lower limit for get_lines()
        self.upper_wavelength = upper_wavelength    # upper limit for get_lines()
        self.order = order                          # wavelength scaling, 1 equals to nm as given by the NIST database
        self.lines = []                             # List of dictionaries with line information
        self.nistasd_obj = None                     # data fetcher

    def _check_download_conditions(self):
        if len(self.lines) == 0:  # no data loaded
            return True
        elif self.spectrum != self.lines[0]['spectrum'].split(' ')[0]:  # loaded data is different from current species
            return True
        else:
            return False
            

    def pprint(self):
        import pprint
        if self._check_download_conditions():
            self.get_lines()

        for line in self.lines:
            wl = line['wave']
            if wl > self.lower_wavelength and wl < self.upper_wavelength:
                pprint.pprint(line, width=1)
                print()

    @timeit
    def get_lines(self):
        # direc = str(pathlib.Path(__file__).resolve().parent) + '/NIST_data/'
        direc = os.path.expanduser("~") + '/nist-asd/'

        filename = 'nist_data_' + self.spectrum + '.pkl'
        print(self.__class__.__name__, ": searching for saved spectrum in ", direc)
        if not os.path.isfile(direc + filename):
            print(self.__class__.__name__, ": found no spectrum in ", direc, " for ", self.spectrum, ". Downloading spectra ...")
            tmp_nistasd = NISTASD(self.spectrum, 0.01, 10000., self.order)
            self.nistasd_obj = tmp_nistasd
            if not os.path.isdir(direc):
                os.makedirs(direc)
            pickle.dump(self.nistasd_obj, open(direc + filename, 'wb'), protocol=-1)
        else:
            print(self.__class__.__name__, ": found spectrum in ", direc)
            self.nistasd_obj = pickle.load(open(direc + filename, 'rb'))

        self.lines = self.nistasd_obj.lines
        return self.lines

    def get_lines_wavelength_range(self):
        lines = []
        for line in self.lines:
            wl = line['wave']
            if wl > self.lower_wavelength and wl < self.upper_wavelength:
                lines.append(line)
                
                
        return line

    def plot_nist_lines_to_axis(self, axis, normalize_max=None, legend=True):
        if self._check_download_conditions():
            self.get_lines()

        print(self.__class__.__name__, ": Plotting NIST lines")
        specs = np.array(list(set([l['spectrum'] for l in self.lines])))
        specs.sort()

        maxi = self._get_maximum_relative_intensity()

        lines = []
        lines_spec = list(np.zeros(len(specs)))

        for i in range(0,len(self.lines)):
            wl = self.lines[i]['wave']
            if wl > self.lower_wavelength and wl < self.upper_wavelength:
                ispc, = np.nonzero(np.ravel(specs == self.lines[i]['spectrum']))
                
                self.colr = plt.cm.get_cmap('tab20c_r')(float(ispc)/len(specs))

                if normalize_max == None:
                    ri = float(self.lines[i]['rel_int']) / maxi
                else:
                    ri = float(self.lines[i]['rel_int']) / maxi * normalize_max

                lines.append(axis.plot([wl, wl], [0., ri if not isnan(ri) else 1.e-6], '.-', color=self.colr, alpha=.99)[0])

                assert len(ispc) == 1  # dont know if correct, but working
                lines_spec[ispc[0]] = lines[-1]

        # datacursor(lines)
        print(self.__class__.__name__, ": plotting ", len(lines), " lines of ", len(self.lines), " in total for ", self.spectrum, " from ", self.lower_wavelength, " to ", self.upper_wavelength, " nm")
        datacursor(lines, formatter='{x} nm'.format)

        if legend:
            if len(specs) > 1:
                axis.legend(lines_spec, specs, loc=0)

    def _get_maximum_relative_intensity(self):
        maxi = 0
        for i in range(len(self.lines)):
            wl = self.lines[i]['wave']
            if wl > self.lower_wavelength and wl < self.upper_wavelength:
                if self.lines[i]['rel_int'] > maxi:
                    maxi = self.lines[i]['rel_int']

        return maxi

    def plot_lines(self):
        if self._check_download_conditions():
            self.get_lines()
        plt.figure()
        plt.grid()
        plt.xlabel('wavelength (nm)')
        plt.ylabel('relative intensity')
        self.plot_nist_lines_to_axis(plt.gca(), 1.)


if __name__ == '__main__':
    # Example 1
    nist = NISTLines(spectrum='Xe', lower_wavelength=2, upper_wavelength=20, order=1)
    nist.get_lines()
    nist.pprint()

    # Example 2
    nist = NISTLines()
    nist.spectrum = 'Kr'
    nist.lower_wavelength = 5.
    nist.upper_wavelength = 30.

    nist.get_lines()
    plt.figure()
    ax = plt.gca()
    nist.plot_nist_lines_to_axis(ax)
    plt.grid()
    plt.show()

