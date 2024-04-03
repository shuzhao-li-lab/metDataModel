"""
Classes derived from the basic classes, or constructed to extend functions.

They allow developers to use the core data structures as building blocks,
to serve customized applications.

For Further annotation models - see khipu

Note that examples are dataclasses; however, regular classes can inherit from dataclasses too.
"""

from metDataModel.core import Experiment, Compound, EmpiricalCompound, Feature, Spectrum, ArrayOfSpectra, serializable_primitive_type, serializable_type
from dataclasses import dataclass, field
from typing import Union

spectral_array_type = Union[list[Spectrum], ArrayOfSpectra]

@dataclass
class userData(Experiment):
    '''
    If no annotation is given, 
    the data should be list_of_features.
    list_of_empCpds is generated by annotation methods.
    '''
    metadata: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {})            # from Experiment attributes
    list_of_empCpds: list[EmpiricalCompound] = field(default_factory=lambda: [])   
    list_of_features: list[Feature] = field(default_factory=lambda: [])

@dataclass
class annotatedCompound(EmpiricalCompound):
    '''
    Class for annotated compounds, which can have annotation from authentic standards, MS^n or other information.
    library compound will use same class

    We will have a cumulative list of annotatedCompound
    libraryCompound = annotatedCompound
    '''
    observed_mass: float = 0.0000

@dataclass
class Compound_spectra(Compound):
    '''
    Compound with added spectra from spectral databases or in silico prediciton.
    Refer to how HMDB organizes spectra for metabolites.
    '''
    metadata: dict[serializable_primitive_type, serializable_type] = field(default_factory=lambda: {})            # from Experiment attributes
    MS1_ESI_pos : spectral_array_type = field(default_factory=lambda: [])
    MS1_ESI_neg : spectral_array_type = field(default_factory=lambda: [])
    MS1_EISA_pos : spectral_array_type = field(default_factory=lambda: [])
    MS1_EISA_neg : spectral_array_type = field(default_factory=lambda: [])
    MS1_GC_pos : spectral_array_type = field(default_factory=lambda: [])
    MS1_GC_neg : spectral_array_type = field(default_factory=lambda: [])
    MS2_CID_pos : spectral_array_type = field(default_factory=lambda: [])
    MS2_CID_neg : spectral_array_type = field(default_factory=lambda: [])

@dataclass
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
    possible_origin: str = ''
    type_of_contaminant: str = ''
    mass: float = 0
    good_name: str = ''
    name: str = ''
    formula: str = ''
    ion_form: str = ''
    references: list[str] = field(default_factory=lambda: [])

@dataclass
class xenobiotic_signature(EmpiricalCompound):
    '''
    A signature on a xenobiotic compound includes the parent compound and its biotransformation products.
    They can be organized on the template of EmpiricalCompound, e.g.
    { # parent compound
      "interim_id": 0,
      "neutral_formula_mass": null,
      "neutral_formula": null,
      "Database_referred": [],
      "identity": [],
      "MS1_pseudo_Spectra": [       # experimentally observed ions
        {
          "id_number": 315,
          "mz": 133.10523223876953,
          "ion_relation": "M+H+",
        },
        {
          "mz": 134.10852813720703,
          "id_number": "F97",
          "rtime": 121.099636272,
          "ion_relation": "M+H+",
        }
      ]
    }
    '''
    
    def score(self):
        '''
        Score the signature. Simplest method being count of matched ions.
        '''
        return 0