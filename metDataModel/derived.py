"""
Place holder for now -


compound example in mummichog 2: 
'formula': 'C45H70N7O18P3S', 'mw': 1121.3710887012, 'name': '3(S)-hydroxy-tetracosa-12,15,18,21-all-cis-tetraenoyl-CoA', 
'adducts': {'M+K[1+]': 1160.33386516797, 'M+Cl[-]': 1156.3399887012001, 'M+Br[-]': 1200.2893887012, 'M+H[1+]': 1122.37836516797, 'M+HCOOK[1+]': 1206.33966516797, 'M(C13)+3H[3+]': 375.13203936717, 'M+ACN-H[-]': 1161.39035723443, 'M+Cl37[-]': 1158.3369887012, 'M-H2O-H[-]': 1102.35321223443, 'M(S34)+H[1+]': 1124.37416516797, 'M+CH3COO[-]': 1180.3843837012, 'M[1+]': 1121.3710887012, 'M-HCOOH+H[1+]': 1076.37296516797, 'M+NaCl[1+]': 1180.33696516797, 'M+H+Na[2+]': 572.68382081737, 'M+H2O+H[1+]': 1140.3889651679701, 'M-H+O[-]': 1136.35872223443, 'M+K-2H[-]': 1157.31203576766, 'M+2H[2+]': 561.69282081737, 'M+Br81[-]': 1202.2873887012001, 'M-H2O+H[1+]': 1104.36776516797, 'M-C3H4O2+H[1+]': 1050.3572651679701, 'M-NH3+H[1+]': 1105.3518651679701, 'M+Na-2H[-]': 1141.33853576766, 'M-CO2+H[1+]': 1078.38856516797, 'M+Na[1+]': 1144.36036516797, 'M-2H[2-]': 559.67826788383, 'M-H4O2+H[1+]': 1086.3571651679702, 'M(C13)-H[-]': 1121.36721223443, 'M(C13)+2H[2+]': 562.1945208173701, 'M(S34)-H[-]': 1122.35961223443, 'M+HCOO[-]': 1166.3687337012, 'M-H[-]': 1120.36381223443, 'M+HCOONa[1+]': 1190.36576516797, 'M+3H[3+]': 374.79763936717, 'M(C13)+H[1+]': 1123.3817651679701, 'M-CO+H[1+]': 1094.3833651679702}









"""

class metaboliteSet(Pathway):
    self.members = []



class similarityGroup(Pathway):
    self.members = []



class annotatedCompound(EmpiricalCompound):
    '''
    library compound will use same class

    We will have a cumulative list of annotatedCompound

    libraryCompound = annotatedCompound


    '''
    self.observed_mass = 0.0000


class mzCompound(Compound):
    '''

    Ions are precomputed as a dictionary.
        Take into consideration of charge state; adjust adduct calculation based on charge

    '''
    'peaks': {
                'M+H[1+]': 0,
                'M[1+]': 0,
                'M+Na[1+]': 0,
                #
                'M-H[1-]': 0,
                'M-H2O-H[-]': 0,
                'M-2H[2-]': 0,
            },
    
    self.inferred_formula = ''
    self.class = ''  # refer to Classifire ontology or lipid ontology

