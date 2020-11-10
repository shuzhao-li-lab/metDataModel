'''
General data models for metabolomics data

For experimental data,
The hierarchy is Experiment -> empCpd -> Features -> Peaks

For theoretical data,
The hierarchy is Network/pathway -> reactions -> compounds

Not all concepts have to be explicitly modeled in a project (e.g. expt, peak, network).

'''

#
# Experimental concepts: experiment, peak, feature, empirical compound
# only considering mass spec data
#

class Experiment:
    '''
    type can be LC-MS, LC-MS/MS, GC-MS, LC-IMS, etc.
    Can model after metTab in Metabolomics Workbench.
    
    '''
    id = 1000
    input_data_from = ''
    type = 'LC-MS'
    instrument = ''
    instrument_parameters = {}

    chromatography = ''
    chromatography_parameters = {
        'column_length': '',
        'column_diameter': '',
        'total_time': '300', # seconds
        'gradient': '',
        # etc.
    }
    
    preprocess_software = ''
    preprocess_parameters = {
        'version': '1.0',
        'SNR': 1.5,
        # etc.
    }
    
    
class Peak:
    '''
    Specific to a sample in an experiment.
    Preprocessing software extracts peaks per sample, then performs alignment.
    The alignment shifts m/z, rt etc values.
    For this class, pre-alignment is preferred. 
    
    But almost all data tables we have are post-alignment, 
    which are accommodated here by setting aligned=True.

    # indexing can be done from feature / expt
    feature_belonged = ''
    experiment_belonged = ''
    
    '''
    ms_level = 1                    # MS levle - 1, 2. 3, etc.
    aligned = False
    ionization = 'positive'
    
    mz = 0
    retention_time = 0
    collision_cross_section = 0     # reserved for IM data
    
    intensity = 0
    intensity_value_by = 'area'     # or height, etc.
    
    peak_shape = ''                 # need a method to define this
    


class Feature:
    '''
    A feature is a peak that is aligned across samples.
    So this is experiment specific.


    '''
    ms_level = 1                    # MS levle - 1, 2. 3, etc.
    mz = 0
    retention_time = 0

    intensities = []

    # optional
    collision_cross_section = 0     # reserved for IM data
    
    intensity_sample_mean = 0
    intensity_sample_std = 0
    intensity_sample_cv = 0
    intensity_replicate_cv = 0
    
    experiment_belonged = ''


class EmpiricalCompound:
    '''
    EmpiricalCompound is a computational unit to include 
    multiple ions that belong to the same metabolite,
    and isobaric/isomeric metabolites when not distinguished by the mass spec data.

    Considered to be a tentative metabolite (compound), 
    result of [computational] annotation.

    This should be equivalent to 'pseudo spectrum' in CAMERA,
    'feature group' in mz.Unit.

    '''
    
    def __init__(self):
        '''
        An empCpd has one and only one base neutral mass
        '''
        self.neutral_base_mass = 0.0000
        # this is list of MS1 features
        self.list_of_features = [
            {'feature': 'row23', 'ion': 'M+H[1+]', 'm/z': 169.0013, 'rtime': 55},
            {},
            # ...
        ]
        # after annotation
        self.identity = {
                  # compound(s): probability
                  (Compound x): 5,
                  (Compound y, Compound z): 5,
          }

        # Experiment specific.
        self.experiment_belonged = ''
        self.annotation_method = ''

        # data structure for MS2/MSn, while spectra are modeled in annotation
        self.fragment_tree = {}
            
        

#
# Theoretical concepts: compound, reaction, pathway, network
#

class Compound:
    def __init__(self):
        '''
        All metabolites are compounds, but the reverse is not true.
        Thus, compound is a basic class.

        Azimuth ID starts with `az`, 
        and incorporates HMDB ID (less ambiguous than KEGG) whereas possible.
        
        '''
        self.internal_id = ''
        self.name = ''          # common name
        self.db_ids = {
            'KEGG': '',
            'HMDB': '',
            'Azimuth': '',
            'PubChem': '',
            'MetaNetX': '',
            # etc.
            }
        self.neutral_formula = ''
        self.neutral_mono_mass = 0.0000

        self.SMILES = ''
        self.inchi = ''
        

class Reaction:
    '''
    Key info is reactants and products - each a list of compounds.

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
        self.ontologies = []

        self.species = ''
        self.compartments = []
        self.cell_types = []
        self.tissues = []
        

class Pathway:
    '''
    A pathway is defined by connected biochemical reactions, according to human definition.
    '''
    def __init__(self):
        self.azimuth_id = ''
        self.name = ''
        self.source = []
        self.list_of_reactions = []
        self.status = ''


class Network:
    '''
    Metabolic network 
    is defined by connected biochemical reactions.

    Network is mathematically identical to pathway, but not limited by pathway definition.
    Edges and nodes are computed based on reactions.

    All based on prior knowledge.
    This class does not include correlation networks and as such.
    '''
        self.azimuth_id = ''
        self.name = ''
        self.source = []
        self.list_of_reactions = []
        self.status = ''

