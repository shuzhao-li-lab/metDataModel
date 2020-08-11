'''
Place holder for now -

Import from serialized Python objects.
(A server version will use or a central database)

metabolicModels = {
    human_model_default: [
        ListOfCompounds: [Compound: {ID, name, mw, formula, AdductsAndDerivatives,
                                    }, ...],
        Pathway
        MetabolicNetwork
    
        ],
    
    ...,
}

@author: Shuzhao Li
'''
from .JSON_metabolicModels import metabolicModels
import numpy as np
import networkx as nx


class metabolicPathway:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.rxns = []
        self.ecs = []
        self.ec_num = 0
        self.cpds = []
        self.cpd_num = 0
        
        self.selected_features = []
        self.combined_pvalue = 0    # -log10()
        
    def str_import(self, s):
        '''
        function to import pathway from plain text;
        excluding currency metabolites.
        Not used for now.
        '''
        a = s.rstrip().split('\t')
        self.id = a[0]
        self.name = a[1]
        self.rxns = a[2].split(';')
        self.ecs = a[3].split(';')
        self.ec_num = int(a[4])
        cpds = a[5].split(';')
        self.cpds = [x for x in cpds if x not in currency]
        self.cpd_num = len(self.cpds)
        
    def json_import(self, j):
        '''
        function to import pathway from JSON format.
        '''
        self.id = j['id']
        self.name = j['name']
        self.rxns = j['rxns']
        self.ecs = j['ecs']
        self.ec_num = len(j['ecs'])
        self.cpds = j['cpds']
        self.cpd_num = len(j['cpds'])


class metabolicNetwork:
    '''
    Metabolite-centric metabolic model 
    Theoretical model, not containing user data
    '''
    def __init__(self, MetabolicModel):
        '''
        Initiation of metabolic network model.
        Building Compound index.
        Parsing input files.
        Matching m/z - Compound.
        
        MetabolicModel['Compounds'] are subset of cpds in network/pathways with mw.
        Not all in total_cpd_list has mw.
        '''
        #print_and_loginfo( "Loading metabolic network %s..." %MetabolicModel.version ) # version from metabolic model
        
        self.MetabolicModel = MetabolicModel
        self.network = self.build_network(MetabolicModel['cpd_edges'])
        
        self.version = MetabolicModel['version']
        self.Compounds = MetabolicModel['Compounds']
        self.metabolic_pathways = MetabolicModel['metabolic_pathways']
        self.dict_cpds_def = MetabolicModel['dict_cpds_def']
        self.cpd2pathways = MetabolicModel['cpd2pathways']
        self.edge2enzyme = MetabolicModel['edge2enzyme']
        self.total_cpd_list = self.network.nodes()
        
        
    def build_network(self, edges):
        return nx.from_edgelist( edges )
        

    def get_pathways(self):
        pass
 


class Compound_Methods:
    '''To calcuate MS-related properties here for each Compound
    '''

    # isotopes and adducts, both pos and neg precomputed
    self.adducts = {}

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




#
# Full metabolic models can be built based on compounds and reactions
#


def build_full_model:
    pass

def build_mummichog_model:
    pass


class mummichog_empCpd(EmpiricalCompound):
    
    def mummichog_methods(self, listOfFeatures)
        '''
        Initiation using 
        listOfFeatures = [[retention_time, row_number, ion, mass, compoundID], ...]
        This will be merged and split later to get final set of EmpCpds.
        '''
        self.listOfFeatures = listOfFeatures
        self.listOfFeatures.sort(key=lambda x: x[1])
        self.str_row_ion = self.__make_str_row_ion__()          # also a unique ID
        self.__unpack_listOfFeatures__()
        
        self.EID = ''
        self.chosen_compounds = []
        self.face_compound = ''
        
        self.evidence_score = 0
        self.primary_ion_present = False
        self.statistic = 0

    def export_json(self):
        return {}




