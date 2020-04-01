'''
Prototyping data models...


'''

class Compound:
    def __init__(self):
        '''
        Azimuth ID starts 
        '''
        self.azimuth_id = ''
        self.other_ids = {
            'KEGG': '',
            'HMDB': '',
            }
        self.formula = ''
        self.inchi = ''
        self.mono_mass = 0

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
        # concentration ranges given at HMDB etc.
        return {}



class Reaction:
    '''
    Reactions are species specific, 
    because genes are species specific.
    '''
    def __init__(self):
        self.azimuth_id = ''
        self.source = []
        self.version = ''
        # status, one of ['active', 'under review', 'obsolete']
        self.status = ''

        self.reactants = []
        self.products = []
        self.enzymes = []
        self.genes = []

        self.pathways = []

        self.species = ''
        self.compartments = []
        self.cell_types = []
        self.tissues = []
        




