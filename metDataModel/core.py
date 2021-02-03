'''
General data models for metabolomics data.

For experimental data,
The hierarchy is Experiment -> empCpd -> Features -> Peaks

For theoretical data,
The hierarchy is Network/pathway -> reactions -> compounds

Not all concepts have to be explicitly modeled in a project (e.g. expt, peak, network).
Use derived/inherited classes for more explict or specialized data.

To learn about mass spectrometry concepts and pre-processing:
https://pyopenms.readthedocs.io/en/latest/datastructures.html
https://github.com/jorainer/metabolomics2018

To learn about genome scale metabolic models:
https://link.springer.com/article/10.1186/s13059-019-1730-3
https://link.springer.com/protocol/10.1007/978-1-0716-0239-3_19

'''

#
# Experimental concepts: experiment, peak, feature, empirical compound
# only considering mass spec data
#

class Experiment:
    '''
    An experiment of LC-MS, LC-MS/MS, GC-MS, LC-IMS, etc.
    This can be equivalent to XCMSnExp class in the XCMS R package, 
    or MSExperiment in the OpenMS software,
    but need not be so extensive when pre-processing is not the focus.
    '''
    id = ''
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
    
    @property
    def __init__(self, id):
        self.id = id
    


class Peak:
    '''
    Chromatographic peak, specific to a sample in an experiment.
    Preprocessing software extracts peaks per sample, then performs alignment/correspondence.
    For high-resolution data, m/z alignment isn't a major concern.
    Retention time alignment shifts the data values.
    For this class, pre-alignment data is preferred, 
    so that people can use different methods for their own alignment.
    
    When data tables come as post-alignment data, 
    which are accommodated in list_retention_time_corrected.

    '''
    ms_level = 1                    # MS levle - 1, 2. 3, etc.
    ionization = 'positive'
    corresponding_feature_id = ''   # belong to which feature after correspondence
    experiment_belonged = ''

    mz_peak_value = 0
    min_mz, max_mz = 0, 0
    # XIC and peak_shape are defined by intensity as teh the function of rtime
    list_retention_time = []
    list_intensity = []

    # if RT aligned/adjusted
    list_retention_time_corrected = []
    # 
    # collision_cross_section = 0     # reserved for IM data

    

class Feature:
    '''
    A feature is a set of peaks that are aligned across samples.
    So this is experiment specific.
    The default is LC-MS feature. Derivative classes include MS2feature, etc.

    '''
    ms_level = 1                    # MS levle - 1, 2. 3, etc.
    mz = 0
    retention_time = 0

    including_peaks = []

    # optional
    # collision_cross_section = 0     # reserved for IM data
    
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
        # after annotation, not ruling out an empCpd can be mixture (isomers, etc)
        self.identity = {
                  # compound(mixtures): probability
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
    A reaction is defined by reactants and products, each a list of compounds.
    There is directionality of a reaction. A forward reaction is different from reverse reaction.
    We can treat the reactions catalyzed by different enzymes as the same 


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

