'''
General data models for metabolomics.
Simple is good, and complex and specialized classes can be derived from these.

A mass spectrum is a list of masses. 
MS1 is direct scan of ions to generate intensity values.
MS^2 and MS^n refers to spectrum to measure fragmentation products of a precursor ion from lower MS level.

LC-MS is a composite of many spectra, each being a scan at a specific elution time. 
A peak can refer to either peak on the m/z axis, or peak on the LC axis.
The former is less common now as high-resolution mass spectrometry data 
require little attention in identifying (centroiding) the m/z peaks.
A peak on the LC axis is a chromatographic peak (elution peak) in LC-MS, 
but people may use 3-D detection or higher dimension e.g. IM-LC-MS.

Empirical compound is a key concept proposed by Shuzhao Li lab to connect 
experimental measurements and database records, including metabolic models.

Not all concepts have to be explicitly modeled in a project (e.g. expt, peak, network).
Use derived/inherited classes for more explict or specialized data.

We try to be explicit in source code, and Python supports introspection.
Therefore, getters and setters are avoided.
A serialize function is made available for easy JSON export. 
For simple cases, these classes can be simplified as Python NamedTuples, 
which allow easy access to attributes but have no additional methods.
'''

#
# Experimental concepts: experiment, peak, feature, empirical compound; massTrace, MSnSpectrum
# only considering mass spec not NMR data here
#
from __future__ import annotations
from typing import Union
import abc
import pandas as pd
import inspect
from dataclasses import dataclass, field

# this is a master list of serializable primitives, i.e., not iterable.
serializable_primitive_type = Union[str, float, int, tuple]

# this is a datastructure to handle nested, up to depth 1, of serializable primitives in dicts and lists
serializable_type = Union[serializable_primitive_type, dict[serializable_primitive_type, serializable_primitive_type], list[serializable_primitive_type]]


class metDataMember(abc.ABC):
    """metDataMember

    This is an abstract baseclass from which all metDataMembers should inherit.
    An abstract base class allows for the easy implementation of methods that 
    need to be shared among all subclasses. 

    This should NEVER be insantiatable 
    """

    @staticmethod
    def __recursive_serialize(to_serialize) -> dict:
        """
        This method converts a dictionary consisting of various fields and values
        into a dictionary suitable for serialization using JSON / YAML or other
        similar markup-like specification. 

        This is achieved by recursing through the dictionary by field, and setting
        key, value pairs in the dictionary appropriately. Simple primitives of 
        types str, float, and int require no processing. Iterables are iterated over
        and checked for serializable-ness. Values that define a serialize method, will
        have that method called upon them, thus enabling the nesting of metDataModel 
        instances. 

        Args:
            to_serialize (_type_): a dictionary containing data members of a metDataObject

        Returns:
            dict: a dictionary representation of to_serialize that is JSON/YAML friendly.
        """        
        if isinstance(to_serialize, (str, float, int)):
            return to_serialize
        elif isinstance(to_serialize, dict):
            return {metDataMember.__recursive_serialize(key): metDataMember.__recursive_serialize(value) for key, value in to_serialize.items()}
        elif isinstance(to_serialize, (list, tuple)):
            return [metDataMember.__recursive_serialize(x) for x in to_serialize]
        elif inspect.isclass(to_serialize) and issubclass(to_serialize, metDataMember) and not isinstance(to_serialize, abc.ABC) and hasattr(to_serialize, "serialize"):
            return to_serialize.serialize()
        else:
            pass

    def serialize(self) -> dict:
        """
        Given a metDataModel object return a dictionary that is JSON/YAML friendly of its datamembers

        Returns:
            dict: a dictionary representation of the object that is JSON/YAML friendly.
        """        
        to_serialize = {x: getattr(self, x) for x in vars(self) if not x.startswith("_")}
        return metDataMember.__recursive_serialize(to_serialize)

@dataclass
class Study(metDataMember):
    '''
    A study can include multiple experiments and datasets by different methods.
    '''
    id: str = ''
    url: str = ''
    time_retrieval: str = ''


@dataclass
class Experiment(metDataMember):
    '''
    An experiment of LC-MS, LC-MS/MS, GC-MS, LC-IMS, etc.
    An experiment can include multiple methods and various types of samples,
    which may require separate data processing.

    The XCMSnExp class in the XCMS R package, or MSExperiment in the OpenMS software,
    may refer to a subset of experiment by the same method.
    We can use `monoExperiment` to refer a subset of experiment by the same method.
    Then the `Experiment` contains multiple monoExperiments.

    `Method` has its own class only if needed.
    In most cases, it's simpler to have some str references in `Experiment` or `monoExperiment`.

    Measurement data are attached to an Experiment, 
    in the form of a list of features and 
    a list of empCpds (the latter generated by annotation).
    Flexibility is given by any type of data can be attached.
    No need to be extensive when pre-processing is not the focus.

    For LC-MS, the feature-level data is a DataFrame,
    features in rows and observations (samples) in columns, similar to gene express data matrix.
    On disk, the data can follow the convention of ANNdata and HiCoNet,
    the 3-file-society Data Strucutre: DataMatrix, FeatureAnnotation and ObservationAnnotation. 
    The DataMatrix in file format uses a single row for observation IDs and a single column for feature IDs.
    Ref: https://github.com/shuzhao-li/hiconet

    The empCpd-level data can be in JSON or other formats.
    '''
    id: str = ''
    parent_study: str = ''
    number_samples: int = None
    species: str = ''
    tissue: str = ''
    provenance: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'generated_time': '',
        'generated_by': '',
        'input_filename': '',
        'preprocess_software': '',
        'preprocess_parameters': {}
    })

    chromatography: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'type': '',
        'total_time': '',
        'method_file': '',
        'column_model': '',
        'column_length': ''
    })
    instrumentation: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'type': '',
        'spectrometer': '',
        'method_file': '',
        'ionization': ''
    })
    ObservationAnnotation: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'sample_list': [],
        'file_sample_mapper': {}
    })
    feature_DataFrame: pd.DataFrame = pd.DataFrame()
    ordered_samples: list[str, Sample] = field(default_factory=list)
    List_of_empCpds: list[dict, EmpiricalCompound] = field(default_factory=list)

@dataclass
class Method(metDataMember):
    '''
    A study can include multiple experiments and datasets by different methods.
    '''
    id: str = ''
    url: str = ''
    citation: str = ''
    chromatography: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'type': '',
        'total_time': '',
        'method_file': '',
        'column_model': '',
        'column_length': ''
    })
    instrumentation: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'type': '',
        'spectrometer': '',
        'method_file': '',
        'ionization': ''
    })

@dataclass
class Sample(metDataMember):
    '''
    This is an analytical sample subjected to a single metabolomic method and associated with a single data file.
    Elution peaks are defined at sample level. A feature is defined at experiment level.
    One can extend to many attributes via registry dictionary, e.g.
        self.data_location = registry['data_location']
        self.track_mzs = registry['track_mzs']
        self.max_scan_number = registry['max_scan_number']
        self.anchor_mz_pairs = registry['anchor_mz_pairs']
        self.rt_numbers = registry['list_scan_numbers']
    '''
    experiment: Union[str, Experiment] = ''
    mode: str = ''
    sample_type: str = ''

    input_file: str = ''
    name: str = ''
    id: str = ''
    list_retention_time: list[str, float] = field(default_factory=dict)
    list_MassTracks: list[str] = field(default_factory=list)
    list_peaks: list[str, Peak] = field(default_factory=list)

@dataclass
class Spectrum(metDataMember):
    '''
    A list of values on a property in analytical chemistry.
    A mass spectrum is a list of m/z values with corresponding intensity values. 
    The "Spectrum" here is generic enough for LC-MS, GC-MS, LC-IMS-MS, etc. 
    It can be used for NMR and other technologies with minor modifications. 
    
    Mass Spectrum provide data points as measured on instrument, 
    This can be MS level 1, 2 or n.
    
    Example of a MS2 spectrum from MONA:
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
    id: str = field(default='')
    ms_level: int = field(default=2)
    ionization: str = field(default=None)
    precursor_ion: float = field(default=None)
    precursor_ion_mz: float = field(default=None)
    retention_time: float = field(default=None)
    rtime: float = field(default=None)


@dataclass
class ArrayOfSpectra(metDataMember):
    '''
    Metabolomic experiments usually employ some chromatography as separation technique. 
    Therefore, analysis of a "Sample" by a "Method" generates a series of spectra.
    The "Array of Spectra" is composed by linking separation parameters with spectra.
    '''
    id: str = field(default='')
    sample: str = field(default=None)
    parameters: dict[serializable_primitive_type, serializable_type] = field(default_factory=dict)
    list_values: list[str, float, int] = field(default_factory=list)

@dataclass
class Peak(metDataMember):
    '''
    This refers to an elution peak in chromatography.
    The m/z peaks are handled by centroiding algorithms these days and are not part of this.

    Most software, e.g. XCMS, MZmine, OpenMS, does peak detection per sample then align them.
    Asari detects peaks on composite signals not on individual samples.

    Example peak in asari:    
        {"apex": 315,
        "peak_area": 3456351,
        "height": 471023,
        "left_base": 311,
        "right_base": 323,
        "cSelectivity": 1.0,
        "parent_masstrack_id": 902,
        "mz": 134.10852813720703,
        "snr": 74,
        "goodness_fitting": 0.8357564804888509,
        "id_number": "F97",
        "rtime": 121.099636272,
        "rtime_left_base": 119.5951254229998,
        "rtime_right_base": 124.12197382300019,}
    '''
    id : str = field(default='')
    ms_level : int = field(default=1)
    mode : str = field(default='pos')
    sample : str = field(default='')
    list_mz : list[float] = field(default_factory=list)
    list_retention_time : list[str, float] = field(default_factory=list)
    list_intensity: list[float] = field(default_factory=list)
    
    #if RT aligned / adjusted
    list_retention_time_corrected : list[float, str] = field(default_factory=list)

    #if pre-annotated
    ion_relation: str = ''

    #derivative of XIC
    mz: float = field(default=None)
    min_mz: float = field(default=None)
    max_mz: float = field(default=None)
    rtime: Union[float, str] = field(default=None)
    min_ritme: Union[float, str]  = field(default=None)
    max_rtime: Union[float, str]  = field(default=None)


@dataclass
class MassTrack(metDataMember):
    '''
    Same as extracted ion chromatogram. This is used in place of EIC (or XIC, mass trace), 
    defined by m/z, list_retention_time, list_intensity.
    Computationally equivalent to EIC for LC-MS data, but spanning for full RT range in asari.
    See https://github.com/shuzhao-li/asari for application in data preprocessing.
    '''
    id: str = field(default='')
    mz: float = field(default=None)
    list_retention_time: list[str, float, int] = field(default_factory=list)
    list_intensity : list[str, float, int] = field(default_factory=list)


@dataclass
class Feature(metDataMember):
    '''
    A feature is a set of peaks that are aligned across samples.
    This is experiment specific.
    The m/z and retention_time of a feature is summarized on the member peaks.
    The variation between samples is reflected in data at peak level.

    Selectivity is defined in asari (https://github.com/shuzhao-li/asari):
        mSelectivity, how distinct are m/z measurements
        cSelectivity, how distinct are chromatograhic elution peaks
        dSelectivity, how distinct are database records

    The default is LC-MS feature. Derivative classes can be MS2feature, etc.
    '''

    id: str = ''
    ms_level: int = 1
    mz: float = 0
    parent_masstrack_id: str = None
    rtime: float = 0
    left_base: float = None
    right_base: float = None
    height: float = 0
    peak_area: float = 0
    goodness_fitting: float = 0
    snr: float = 0
    mSelectivity: float = 0
    cSelectivity: float = 0
    dSelectivity: float = 0
    list_peaks: list[str, Peak] = field(default_factory=list)
    including_peaks: list[str, Peak] = field(default_factory=list)
    experiment_belonged: str = ''
    annotation: dict[serializable_primitive_type] = field(default_factory=dict)
    statistics: dict[serializable_primitive_type] = field(default_factory=dict)

@dataclass
class EmpiricalCompound(metDataMember):
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

    An empCpd is the result of annotation.
    It has one and only one base neutral mass.
    Many attributes are optional.

    In a specific Experiment, an EmpiricalCompound consists of a set of features across a set of samples.
    They can be list of MS1 features, either using pointers to Features in the database.
    Features can include MS1 and MSn data.
    How to group Features into empCpd depends on annotation method, e.g. Annotation, AnnotationResult from mass2chem
    After annotation, not ruling out an empCpd can be mixture (isomers, etc)
    '''
    
    id: str = ''
    interim_id: str = ''

    experiment_belonged: str = ''
    annotation_method: str = ''

    neutral_base_mass: float = None
    neutral_formula_mass: float = None

    neutral_formula: str = ''
    charge: int = None
    charged_formula: str = ''
    Database_referred: list = field(default_factory=list)

    MS1_pseudo_Spectra: list[str, Peak] = field(default_factory=list)
    list_features: list[str, Feature] = field(default_factory=list)
    MS2_Spectra: list[str, Spectrum] = field(default_factory=list)
    identity: list[str] = field(default_factory=list)
    annotation: list[str] = field(default_factory=list)

    identity_probability_mummichog: list[float] = field(default_factory=list)

    @staticmethod
    def read_json_model(jmodel):
    #    '''Modify as needed
    #    '''
        return EmpiricalCompound(
            id = jmodel['id'],
            interim_id = jmodel['interim_id'],
            neutral_formula_mass = jmodel['neutral_formula_mass'],
            neutral_formula = jmodel['neutral_formula'],
            Database_referred = jmodel['Database_referred'],
            identity = jmodel['identity'],
            MS1_pseudo_Spectra  = jmodel['MS1_pseudo_Spectra'],
            MS2_Spectra = jmodel['MS2_Spectra']
        )

    def get_intensities(self):
    #    ''' Representative intensity values, can base on the MS1 feature of highest intensity
    #    self.intensities = { "sample1": 0, "sample2": 0, ... }
    #    # more efficient version of self.intensities
    #    self.intensities_by_ordered_samples = []
    #    '''
        pass

    def mummichog_annotation(self):
        '''
        Updated identity table by mummichog
        '''
        self.identity_probability_mummichog = [
            # updated probability after mummichog analysis
        ]

#
# Theoretical concepts (metabolic model): compound, reaction, pathway, network; enzyme, gene
#

@dataclass
class Compound(metDataMember):

    internal_id: str = ''
    id: str = ''
    name: str = ''
    db_ids: list[str] = field(default_factory=list)
    neutral_formula: str = ''
    neutral_mono_mass: float = None
    charge: int = None
    charged_formula: str = ''
    SMILES: str = ''
    inchi: str = ''

@dataclass
class Reaction(metDataMember):
    '''
    A reaction is defined by reactants and products, each a list of compounds.
    There is directionality of a reaction. A forward reaction is different from reverse reaction.
    We can treat the reactions catalyzed by different enzymes as the same reactions.

    Reactions are species specific, 
    because genes are species specific.
    '''
    azimuth_id: str = ''
    id: str = ''
    name: str = ''
    source: list[str] = field(default_factory=list)
    version: str = ''
    status: str = ''
    reactants: list[str, Compound] = field(default_factory=list)
    products: list[str, Compound] = field(default_factory=list)
    enzymes: list[str, Enzyme] = field(default_factory=list)
    genes: list[str, Gene] = field(default_factory=list)
    pathways: list[str, Pathway] = field(default_factory=list)
    ontologies: list[str] = field(default_factory=list)
    species: str = ''
    compartments: list[str] = field(default_factory=list)
    cell_types: list[str] = field(default_factory=list)
    tissues: list[str] = field(default_factory=list)

@dataclass
class Pathway(metDataMember):
    '''
    A pathway is defined by connected biochemical reactions, according to human definition.
    '''

    azimuth_id: str = ''
    id: str = ''
    name: str = ''
    source: list[str] = field(default_factory=list)
    list_of_reactions: list[str, Reaction] = field(default_factory=list)
    status: str = ''

@dataclass
class Network(metDataMember):
    '''
    This refers to a metabolic network, defined by connected biochemical reactions.

    Network is mathematically identical to pathway, but not limited by pathway definition.
    Edges and nodes are computed based on reactions.

    Based on prior knowledge. This class does not include correlation networks etc.
    '''

    azimuth_id: str = ''
    id: str = ''
    name: str = ''
    source: list[str] = field(default_factory=list)
    list_of_reactions: list[str, Reaction] = field(default_factory=list)
    status: str = ''

@dataclass
class MetabolicModel(metDataMember):
    '''
    A metabolic model, minimal information is list_of_reactions.
    Pathway definition isn't always available.
    Compounds are union of all reactants and products in reactions.
    Genes and proteins correspond to enzymes in reactions.
    The JMS package (https://github.com/shuzhao-li/JMS) handles the conversion of genome scale metabolic models.
    '''
    id: str = ''
    meta_data: dict = field(default_factory=dict)
    list_of_reactions: list[str, Reaction] = field(default_factory=list)
    list_of_pathways: list[str, Pathway] = field(default_factory=list)
    list_of_compounds: list[str, Compound] = field(default_factory=list)
    metadata: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {
        'species': '',
        'version': '',
        'sources': [],
        'status': '',
        'last_update': ''
    })


# ---------------------------------------------------------
# To extend later
#

@dataclass
class Enzyme(metDataMember):
    '''
    An enzyme is a protein that catalyzes biochemical reactions.
    '''
    id: str = ''
    name: str = ''
    ec_num: str = ''
    url: str = ''
    genes: list[str, Gene] = field(default_factory=list)
    reactions: list[str, Reaction] = field(default_factory=list)

@dataclass
class Gene(metDataMember):
    '''
    A gene is defined by polynucleotide sequence in a genome.
    Not a detailed model fo gene structure here. Main objective is to link to enzyme and biochemistry.
    '''

    id: str = ''
    name: str = ''
    symbol: str = ''
    ensembl_id: str = ''
    description: str = ''
    proteins: list[str, Enzyme] = field(default_factory=list)# can be enzymes
    linked_metabolites: list[str, Compound] = field(default_factory=list)
    linked_diseases: list[str] = field(default_factory=list)
