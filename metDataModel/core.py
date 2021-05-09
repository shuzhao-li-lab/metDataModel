'''
General data models for metabolomics data.
These try to be simple so that complex and specialized classes can be derived from these.

For experimental data,
The hierarchy is Experiment -> empCpd -> Features -> Peaks

For theoretical data,
The hierarchy is Network/pathway -> reactions -> compounds

Not all concepts have to be explicitly modeled in a project (e.g. expt, peak, network).
Use derived/inherited classes for more explict or specialized data.

Spectrum is derived from Peak.

We try be explicit in source code, and Python supports introspection.
Therefore, getters and setters are voided.
A serialize function is made available for easy JSON export. 

To learn about mass spectrometry concepts and pre-processing:
https://pyopenms.readthedocs.io/en/latest/datastructures.html
https://github.com/jorainer/metabolomics2018

To learn about genome scale metabolic models:
https://link.springer.com/article/10.1186/s13059-019-1730-3
https://link.springer.com/protocol/10.1007/978-1-0716-0239-3_19

'''

#
# Experimental concepts: experiment, peak, spectrum, feature, empirical compound
# only considering mass spec data here
#

class Experiment:
    '''
    An experiment of LC-MS, LC-MS/MS, GC-MS, LC-IMS, etc.
    This can be equivalent to XCMSnExp class in the XCMS R package, 
    or MSExperiment in the OpenMS software,
    but need not be so extensive when pre-processing is not the focus.

    Measurement data are attached to an Experiment, 
    in the form of a list of features and 
    a list of empCpds (the latter generated by annotation).
    Flexibility is given by any type of data can be attached.

    For LC-MS, the feature-level data is a DataFrame,
    features in rows and observations (samples) in columns, similar to gene express data matrix.
    On disk, the data can follow the convention of ANNdata and HiCoNet,
    the 3-file-society Data Strucutre: DataMatrix, FeatureAnnotation and ObservationAnnotation. 
    The DataMatrix in file format uses a single row for observation IDs and a single column for feature IDs.
    Ref: https://github.com/shuzhao-li/hiconet

    The empCpd-level data can be in JSON or other formats.
    '''
    def __init__(self, id=''):
        '''
        Try to use long str to be unique in the world.
        Additional fields can be added to the dictionaries.
        '''
        self.id = id                    # e.g. 'EXP00001234'
        self.provenance = {
            'generated_time': '',       # day of experiment
            'generated_by': '',         # operator of experiment
            'input_filename': '',
            'preprocess_software': '',
            'preprocess_parameters': {
                'version': '0.0',
                'ppm': 1,
                'SNR': 1.5,
            },
        }
        self.instrumentation = {
            'type': 'LC-MS',
            'spectrometer': '',         # mass spectrometer model
            'method_file': '',          # method file used
        }
        self.chromatography = {
            'system': '',               # LC model
            'total_time': 300,          # seconds
            'method_file': '',
            'column_model': '',
            'column_length': '',
        }
        
        # data 
        self.feature_DataFrame = None
        self.FeatureAnnotation = {} 
        self.ObservationAnnotation = {
            'sample_list': [],
            'file_sample_mapper': {}
        }
        # immutable ordered version of sample_list
        self.ordered_samples = ()

        # EmpiricalCompounds, after annotation
        self.List_of_empCpds = []

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'provenance': self.provenance,
                'instrumentation': self.instrumentation,
                'chromatography': self.chromatography,
                }
        


class Peak:
    '''
    The default is a chromatographic peak (called EIC or XIC) in LC-MS, 
    specific to a sample in an experiment.
    This can be extended to other type of peaks, and include more detailed data as needed.

    Preprocessing software extracts peaks per sample, then performs alignment/correspondence.
    For high-resolution data, m/z alignment isn't a major concern.
    Retention time alignment shifts the data values.
    For this class, pre-alignment data is preferred, 
    so that people can use different methods for their own alignment.
    
    When data tables come as post-alignment data, 
    which are accommodated in list_retention_time_corrected.
    '''    
    
    def __init__(self, id=''):
        self.id = id
        self.ms_level = 1                    # MS levle - 1, 2. 3, etc.
        self.ionization = 'positive'
        # XIC and peak_shape are defined by intensity as the the function of rtime.
        # If mz is of little variation, it's not always necesssary to show list_mz.
        self.list_mz = []
        self.list_retention_time = []
        self.list_intensity = []
        # if RT aligned/adjusted
        self.list_retention_time_corrected = []

        # derivative to XIC
        self.mz, self.min_mz, self.max_mz = 0, 0, 0
        self.rtime, self.min_rtime, self.max_rtime = 0, 0, 0

        # other attributes of interest
        # e.g. for IM data
        # collision_cross_section = 0

        # optional as this can be reverse indexed
        self.corresponding_feature_id = ''   # belong to which feature after correspondence
        self.experiment_belonged = ''

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'mz': self.mz, 
                'rtime': self.rtime, 
                'ms_level': self.ms_level,
                'ionization': self.ionization,
                'list_mz': self.list_mz,
                'list_retention_time': self.list_retention_time,
                'list_retention_time_corrected': self.list_retention_time_corrected,
                'list_intensity': self.list_intensity,
                }


class Spectrum(Peak):
    '''
    Spectrum provide data points as measured on instrument, 
    to support the concept of Peak.
    This can be MS level 1, 2 or n.
    
    templated on MONA JSON
            {"instrument": "",
            "precursor type": "M+H[1+]",
            "precursor m/z": 169,
            "collision energy": "30V",
            "score": 5.5,
            "spectrum": "59.000:0.615142 72.600:0.031546 74.600:0.015773 78.900:0.086751 85.200:1.490536 150.500:0.055205 166.000:0.055205 167.200:100.000000",
            },
            {},
            {}
    '''
    def __init__(self, id=''):
        self.id = id
        self.ms_level = 2
        self.precursor_ion = self.precursor_ion_mz = 0

        self.list_mz = []
        self.list_intensity = []
        self.retention_time = self.rtime = 0

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'precursor_ion': self.precursor_ion, 
                'rtime': self.rtime, 
                'ms_level': self.ms_level,
                'ionization': self.ionization,
                'list_intensity': self.list_intensity,
                }


class Feature:
    '''
    A feature is a set of peaks that are aligned across samples.
    So this is experiment specific.
    The m/z and retention_time of a feature is summarized on the member peaks.
    The variation between samples is reflected in data at peak level.

    The default is LC-MS feature. Derivative classes include MS2feature, etc.
    '''

    def __init__(self, id=''):
        self.id = id                # e.g. 'F00001234'
        self.ms_level = 1           # MS levle - 1, 2. 3, etc.
        self.mz = 0
        self.rtime = 0

        # other attributes of interest
        self.list_peaks = self.including_peaks = []
        self.experiment_belonged = ''

        # place holder. Will have separate annotation class/method
        self.annotation = {
        }

        # statistics across samples
        self.statistics = {
            'intensity_sample_mean': None,
            'intensity_sample_std': None,
            'intensity_sample_cv': None,
            'intensity_replicate_cv': None,
            # statistic_score and p_value depend on the statistical test
            'statistic_score': None,
            'p_value': None,
        }

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'mz': self.mz, 
                'rtime': self.rtime, 
                'list_peaks': self.list_peaks,
                }


class EmpiricalCompound:
    '''
    EmpiricalCompound is a tentative compound/metabolite,
    a computational unit to represent the result of annotation on mass spec experiment.
    It should have reference to multiple ions (isotopes/adducts) that belong to the same metabolite,
    and can be a mixture of isobaric/isomeric metabolites when they are not distinguished by the mass spec data.

    This is used because the identification of compounds is not definitve at many stages of a project, 
    and this allows probablistic annotation on experimental data. 
    The probablity ranges between [0, 1]. 
    This unit then enables approaches to factor the probablistic models into biological interpretation (e.g. mummichog). 
    If an annotation method only provides scores (e.g. from MS2 search), mummichog will use them.

    EmpiricalCompound is experiment specific,
    and can combine multiple methods, including pos and neg ESI, MS^n.

    Similar concepts are 'pseudo spectrum' in CAMERA, and 'feature group' in mz.Unity.
    '''

    def __init__(self, id=''):
        '''
        An empCpd is the result of annotation.
        It has one and only one base neutral mass.
        Many attributes are optional.

        In a specific Experiment, an EmpiricalCompound consists of a set of features across a set of samples.
        They can be list of MS1 features, either using pointers to Features in the database.
        Features can include MS1 and MSn data.
        How to group Features into empCpd depends on annotation method.
        '''
        self.id = id                            # e.g. 'E00001234'
        self.neutral_base_mass = 0.0000

        # Experiment specific.
        self.experiment_belonged = ''
        self.annotation_method = ''

        # after annotation, not ruling out an empCpd can be mixture (isomers, etc)
        # neutral formulae
        self.candidate_formulae = []

        self.list_features = []
        # place holder. Will have separate annotation class/method, 
        # e.g. Annotation, AnnotationResult from mass2chem
        self.annotation = {
            #e.g. 'feature_row23': 'M+H[1+]'
        }

        #
        # Scores or probabilities is expected after annotation
        # How to assign probability depends on annotation method
        # Using list not dictionary, as these are tables not easy keys 
        #
        self.identity_table_value = 'score' # or 'probability'
        self.identity_table = [
                  # score or probability, (compound or mixtures)
                  [0.0, ('Compound x')],
                  [0.0, ('Compound y', 'Compound z')],
          ]

        # short-hand notions of identity_table
        self.identity_probability = []
        self.identity_scores = []

    def get_intensities(self):
        # Representative intensity values, can base on the MS1 feature of highest intensity
        self.intensities = {
            "sample1": 0, "sample2": 0, # etc
        }
        # more efficient version of self.intensities
        self.intensities_by_ordered_samples = []

    def mummichog_annotation(self):
        '''
        Updated identity table by mummichog
        '''
        self.identity_probability_mummichog = [
            # updated probability after mummichog analysis
        ]

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'neutral_base_mass': self.neutral_base_mass,
                'experiment_belonged': self.experiment_belonged,
                'candidate_formulae': self.candidate_formulae,
                'identity_table_value': self.identity_table_value,
                'identity_table': self.identity_table,
                'list_features': self.list_features,
                # to add spectra when needed
                }



#
# Theoretical concepts (metabolic model): compound, reaction, pathway, network
#

class Compound:
    def __init__(self):
        '''
        All metabolites are compounds, but the reverse is not true.
        Thus, compound is a basic class.

        Azimuth ID starts with `az`, 
        and incorporates HMDB ID (less ambiguous than KEGG) whereas possible.
        
        '''
        self.internal_id = self.id = ''
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

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'name': self.name, 
                'identifiers': self.db_ids,
                'neutral_formula': self.neutral_formula,
                'neutral_mono_mass': self.neutral_mono_mass,
                'SMILES': self.SMILES,
                'inchi': self.inchi,
                }


class Reaction:
    '''
    A reaction is defined by reactants and products, each a list of compounds.
    There is directionality of a reaction. A forward reaction is different from reverse reaction.
    We can treat the reactions catalyzed by different enzymes as the same reactions.

    Reactions are species specific, 
    because genes are species specific.
    '''
    def __init__(self):
        self.azimuth_id = self.id = ''
        self.source = []
        self.version = ''
        # status, one of ['active', 'under review', 'obsolete']
        self.status = ''

        self.reactants = []
        self.products = []

        # below this line are optional
        self.enzymes = []
        self.genes = []

        # belong to
        self.pathways = []
        # still looking for good ontology for reactions. Maybe notes like "Glucuronidation" for now.
        self.ontologies = []

        self.species = ''
        self.compartments = []
        self.cell_types = []
        self.tissues = []

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'reactants': self.reactants, 
                'products': self.products, 
                }


class Pathway:
    '''
    A pathway is defined by connected biochemical reactions, according to human definition.
    '''
    def __init__(self):
        self.azimuth_id = self.id = ''
        self.name = ''
        self.source = []
        self.list_of_reactions = []
        self.status = ''

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'name': self.name, 
                'list_of_reactions': self.list_of_reactions, 
                }


class Network:
    '''
    Metabolic network 
    is defined by connected biochemical reactions.

    Network is mathematically identical to pathway, but not limited by pathway definition.
    Edges and nodes are computed based on reactions.

    All based on prior knowledge.
    This class does not include correlation networks and as such.
    '''
    def __init__(self):
        self.azimuth_id = self.id = ''
        self.name = ''
        self.source = []
        self.list_of_reactions = []
        self.status = ''

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'list_of_reactions': self.list_of_reactions, 
                }


class metabolicModel:
    '''
    A metabolic model, minimal information is list_of_reactions.
    Pathway definition isn't always available.
    Compounds are union of all reactants and products in reactions.
    Genes and proteins correspond to enzymes in reactions.
    '''
    def __init__(self):
        self.id = ''
        self.meta_data = {
            'species': '',
            'version': '',
            'sources': [],
            'status': '',
            'last_update': '',
        }
        self.list_of_reactions = []
        self.list_of_pathways = []

    def serialize(self):
        '''
        return dictionary of key variables.
        '''
        return {'id': self.id, 
                'list_of_reactions': self.list_of_reactions, 
                'meta_data': self.meta_data,
                }
