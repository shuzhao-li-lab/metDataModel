"""
Classes derived from the basic classes.

# not necessary, simple lists will do:
class metaboliteSet:
    self.members = []
class similarityGroup:
    self.members = []

compound example in mummichog 2: 
'formula': 'C45H70N7O18P3S', 'mw': 1121.3710887012, 'name': '3(S)-hydroxy-tetracosa-12,15,18,21-all-cis-tetraenoyl-CoA', 
'adducts': {'M+K[1+]': 1160.33386516797, 'M+Cl[-]': 1156.3399887012001, 'M+Br[-]': 1200.2893887012, 
'M+H[1+]': 1122.37836516797, 'M+HCOOK[1+]': 1206.33966516797, 'M(C13)+3H[3+]': 375.13203936717, 
'M+ACN-H[-]': 1161.39035723443, 'M+Cl37[-]': 1158.3369887012, 'M-H2O-H[-]': 1102.35321223443, 
'M(S34)+H[1+]': 1124.37416516797, 'M+CH3COO[-]': 1180.3843837012, 'M[1+]': 1121.3710887012, 
'M-HCOOH+H[1+]': 1076.37296516797, 'M+NaCl[1+]': 1180.33696516797, 'M+H+Na[2+]': 572.68382081737, 
'M+H2O+H[1+]': 1140.3889651679701, 'M-H+O[-]': 1136.35872223443, 'M+K-2H[-]': 1157.31203576766, 
'M+2H[2+]': 561.69282081737, 'M+Br81[-]': 1202.2873887012001, 'M-H2O+H[1+]': 1104.36776516797, 
'M-C3H4O2+H[1+]': 1050.3572651679701, 'M-NH3+H[1+]': 1105.3518651679701, 'M+Na-2H[-]': 1141.33853576766, 
'M-CO2+H[1+]': 1078.38856516797, 'M+Na[1+]': 1144.36036516797, 'M-2H[2-]': 559.67826788383, 
'M-H4O2+H[1+]': 1086.3571651679702, 'M(C13)-H[-]': 1121.36721223443, 'M(C13)+2H[2+]': 562.1945208173701, 
'M(S34)-H[-]': 1122.35961223443, 'M+HCOO[-]': 1166.3687337012, 'M-H[-]': 1120.36381223443, 
'M+HCOONa[1+]': 1190.36576516797, 'M+3H[3+]': 374.79763936717, 'M(C13)+H[1+]': 1123.3817651679701, 
'M-CO+H[1+]': 1094.3833651679702}

Isotopes:
    '39K', 38.963706487, 
    '41K', 40.961825258,        # 39K ~ 93.3%, 41K ~ 6.7%
    (1.99812, 'M(41K', 0, 0.2),
    ...
34S and 37Cl are close, but should have diff ratios and are formula dependent
More detailed modeling of epdTree will be useful.


from itertools import combinations

for x,y in combinations(ETS, 2):
    print( (x[0]+y[0], x[1] +','+ y[1], 0, 1) )

ETS = [
    (1.003355, 'M(13C)', 0, 0.8),      # 13C-12C, 12C~99%, 13C ~ 1%
    (0.997035, 'M(15N)', 0, 0.2),     # 15N-14N, 14N ~ 99.64%, 15N ~ 0.36%
    (2.004245, 'M(18O)', 0, 0.2),      # 18O-16O, 16O ~ 99.76, 16O ~ 0.2%
    (1.995796, 'M(34S)', 0, 0.4),      # 32S (95.02%), 33S (0.75%), 34S (4.21%)
    (0.999388, 'M(33S)', 0, 0.1), 
    (-0.0005, 'M[1+]', 0, 1),
    (1.0073, 'M+H[1+]', 0, 1),
    (19.0179, 'M+H2O+H[1+]', 0, 1),
    (22.9893, 'M+Na', 0, 1),
]

    (2.00039, 'M(13C),M(15N)', 0, 1)
    (3.0076, 'M(13C),M(18O)', 0, 1)
    (2.999151, 'M(13C),M(34S)', 0, 1)
    (2.002743, 'M(13C),M(33S)', 0, 1)
    (1.002855, 'M(13C),M[1+]', 0, 1)
    (2.010655, 'M(13C),M+H[1+]', 0, 1)
    (20.021255, 'M(13C),M+H2O+H[1+]', 0, 1)
    (23.992655, 'M(13C),M+Na', 0, 1)
    (3.00128, 'M(15N),M(18O)', 0, 1)
    (2.992831, 'M(15N),M(34S)', 0, 1)
    (1.996423, 'M(15N),M(33S)', 0, 1)
    (0.9965350000000001, 'M(15N),M[1+]', 0, 1)
    (2.004335, 'M(15N),M+H[1+]', 0, 1)
    (20.014935, 'M(15N),M+H2O+H[1+]', 0, 1)
    (23.986335, 'M(15N),M+Na', 0, 1)
    (4.0000409999999995, 'M(18O),M(34S)', 0, 1)
    (3.003633, 'M(18O),M(33S)', 0, 1)
    (2.003745, 'M(18O),M[1+]', 0, 1)
    (3.011545, 'M(18O),M+H[1+]', 0, 1)
    (21.022145000000002, 'M(18O),M+H2O+H[1+]', 0, 1)
    (24.993545, 'M(18O),M+Na', 0, 1)
    (2.995184, 'M(34S),M(33S)', 0, 1)
    (1.995296, 'M(34S),M[1+]', 0, 1)
    (3.003096, 'M(34S),M+H[1+]', 0, 1)
    (21.013696, 'M(34S),M+H2O+H[1+]', 0, 1)
    (24.985096, 'M(34S),M+Na', 0, 1)
    (0.9988880000000001, 'M(33S),M[1+]', 0, 1)
    (2.006688, 'M(33S),M+H[1+]', 0, 1)
    (20.017288, 'M(33S),M+H2O+H[1+]', 0, 1)
    (23.988688, 'M(33S),M+Na', 0, 1)
    (1.0068000000000001, 'M[1+],M+H[1+]', 0, 1)
    (19.017400000000002, 'M[1+],M+H2O+H[1+]', 0, 1)
    (22.9888, 'M[1+],M+Na', 0, 1)
    (20.0252, 'M+H[1+],M+H2O+H[1+]', 0, 1)
    (23.9966, 'M+H[1+],M+Na', 0, 1)
    (42.0072, 'M+H2O+H[1+],M+Na', 0, 1)


"""

from metDataModel.core import Experiment, Compound, EmpiricalCompound


isotopic_patterns = [
    # (mz difference, notion, ratio low limit, ratio high limit), relative to an anchor ion
    (1.003355, 'M(13C)', 0, 0.8),      # 13C-12C, 12C~99%, 13C ~ 1%
    (0.997035, 'M(15N)', 0, 0.2),     # 15N-14N, 14N ~ 99.64%, 15N ~ 0.36%
    (2.004245, 'M(18O)', 0, 0.2),      # 18O-16O, 16O ~ 99.76, 16O ~ 0.2%
    (1.995796, 'M(34S)', 0, 0.4),      # 32S (95.02%), 33S (0.75%), 34S (4.21%)
    (0.999388, 'M(33S)', 0, 0.1), 
    ]

# ratio in adducts is not used now, but future possible.
primary_pos_adducts = [
    (-0.0005, 'M[1+]', 0, 1),
    (1.0073, 'M+H[1+]', 0, 1),
    (19.0179, 'M+H2O+H[1+]', 0, 1),
    (22.9893, 'M+Na', 0, 1),
    ]

primary_neg_adducts = [
    (0.0005, 'M[-]', 0, 1),
    (-1.0073, 'M-H[-]', 0, 1),
    (-19.0179, 'M-H2O-H[-]', 0, 1),
    (34.9689, 'M+Cl[-]', 0, 1),
    (36.9664, 'M+Cl37[-]', 0, 1),       # 35Cl (75.77%) and 37Cl (24.23%).
    ]

isotopic_patterns_double_charged = [
    # double charged, 
    (0.5017, 'double charged with C13', 0, 0.8),
    (0.4985, 'double charged with N15', 0, 0.2),
]

#-------------------------------------------------

mzdiff_pos_signature = [
    (1.003355, 'M(13C)', 0, 0.8),      # 13C-12C, 12C~99%, 13C ~ 1%
    (0.997035, 'M(15N)', 0, 0.2),     # 15N-14N, 14N ~ 99.64%, 15N ~ 0.36%
    (2.004245, 'M(18O)', 0, 0.2),      # 18O-16O, 16O ~ 99.76, 16O ~ 0.2%
    (1.995796, 'M(34S)', 0, 0.4),      # 32S (95.02%), 33S (0.75%), 34S (4.21%)
    (0.999388, 'M(33S)', 0, 0.1), 
    (-0.0005, 'M[1+]', 0, 1),
    (1.0073, 'M+H[1+]', 0, 1),
    (19.0179, 'M+H2O+H[1+]', 0, 1),
    (22.9893, 'M+Na', 0, 1),
    (2.010655, 'M(13C),M+H[1+]', 0, 1),
    (20.021255, 'M(13C),M+H2O+H[1+]', 0, 1),
    (23.992655, 'M(13C),M+Na', 0, 1),
    (2.00039, 'M(13C),M(15N)', 0, 1),
    (2.999151, 'M(13C),M(34S)', 0, 1),
    (2.004335, 'M(15N),M+H[1+]', 0, 1),
    (20.014935, 'M(15N),M+H2O+H[1+]', 0, 1),
    (23.986335, 'M(15N),M+Na', 0, 1),
    (0.5017, 'double charged with C13', 0, 0.8),
    (0.4985, 'double charged with N15', 0, 0.2),
]

#-------------------------------------------------

class epdTree:
    '''
    An epdTree is a representation of how an empirical compound is observed in MS1 data,
    a list of isotopic peaks, each of possible adducts.
    This is used in both directions:
    1) for a known compound, probable peaks are calculated;
    2) from experimental MS1 data, paired mass differences (e.g. 12C/13C) can be used as a signature to organize empCpds. 
    '''

    def __init__(self, mode='pos', charge=1):
        '''
        For unknown compound, base formula (neutral chemical formula with most abundant isotopes) may be unknown.
        But mz signature may help infer the base formula.
        '''
        self.base_mass = None
        self.base_formula = None
        self.tree = {}
        self.signature = mzdiff_pos_signature
    
    def get_extended_adducts(self):
        pass




#
# in progress
#

class userData(Experiment):
    '''
    If no annotation is given, 
    the data should be list_of_features.
    list_of_empCpds is generated by annotation methods.
    '''
    meta_data = {}              # from Experiment attributes
    list_of_empCpds = []
    list_of_features = []


class annotatedCompound(EmpiricalCompound):
    '''
    Class for annotated compounds, which can have annotation from authentic standards, MS^n or other information.
    library compound will use same class

    We will have a cumulative list of annotatedCompound
    libraryCompound = annotatedCompound
    '''
    observed_mass = 0.0000


class Compound_spectra(Compound):
    '''
    Compound with added spectra from spectral databases or in silico prediciton.
    Refer to how HMDB organizes spectra for metabolites.
    '''
    meta = {}
    MS1_ESI_pos = []
    MS1_ESI_neg = []
    MS1_EISA_pos = []
    MS1_EISA_neg = []
    MS1_GC_pos = []
    MS1_GC_neg = []
    MS2_CID_pos = []
    MS2_CID_neg = []


class Contaminant:
    '''
    # mass, good_name, name, formula, ion_form, possible origin
    contaminants_pos = [
        [537.8790134, 'C2H4O2_[M6-H6+Fe3+O]+_537.879013', 'Acetic Acid', 'C2H4O2', '[M6-H6+Fe3+O]+', 'Solvent'], 
        [555.8895784, 'C2H4O2_[M6-H6+H2O+Fe3+O]+_555.889578', 'Acetic Acid', 'C2H4O2', '[M6-H6+H2O+Fe3+O]+', 'Solvent'], 
        [597.9001434, 'C2H4O2_[M7-H6+Fe3+O]+_597.900143', 'Acetic Acid', 'C2H4O2', '[M7-H6+Fe3+O]+', 'Solvent'], 
        [102.0549554, 'C4H7NO2_[M+H]+_102.054955', 'Acetonitrile.1.Acetic acid.1', 'C4H7NO2', '[M+H]+', 'Solvent'],...
    ]
    '''
    possible_origin = type_of_contaminant = ''
    mass = 0
    good_name = ''
    name = ''
    formula = ''
    ion_form = ''
    references = []

