'''
Simple namedtuples when full classes are not needed.

tuples are immutable.

Dictionary formats are used in asari too.

'''

from collections import namedtuple

massTrace = namedtuple('massTrace', ['id_number', 'mz', 'rt_scan_numbers', 'intensity', 'number_peaks'])

# (parent_mass_trace_index, mz, apex, height, left, right)
elutionPeak = namedtuple('elutionPeak', ['id_number', 'mz', 'apex', 'left_base', 'right_base', 'height', 
                                         'parent_masstrace_id', 'rtime', 'peak_area', 'goodness_fitting'])

# Different anchors for pos or neg empCpd
empCpd = namedtuple('empCpd', ['mz_anchors', 'ions', 'list_peaks'])

# ions = ['M[1+]', 'M+H[1+]', '(13C)M+H[1+]', 'M+Na[1+]', 'M+H2O+H[1+]', ...]
# mz_deltas = [-1.0073, 0, 1.0034, 21.9820, 18.0106]