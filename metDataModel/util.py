'''
Place holder for now -
'''

import json
import yaml

def covert_json_to_yaml(jfile, yfile):
    '''
    Convert JSON file jfile to YAML file yfile.
    '''
    with open(jfile, 'rb') as O:
        jj = json.load(O)
    with open(yfile, 'w') as O:
        yaml.dump(jj, O)

class Compound_Methods:
    '''To calcuate MS-related properties here for each Compound
    '''

    # isotopes and adducts, both pos and neg precomputed
    adducts = {}

    def get_pos_ions(self):
        return {}

    def get_neg_ions(self):
        return {}

    def get_pos_MS2(self):
        return {}

    def get_neg_MS2(self):
        return {}
    
    def get_CCS(self):
        return {}

    def get_concentration_range(self):
        '''organism, tissue specific
        '''
        # concentration ranges given at HMDB etc.
        return {}

