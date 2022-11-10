# metDataModel, data models for mass spectrometry based metabolomics

Our goal is to define a minimal set of data models to promote interoperability in computational metabolomics.
This package will lay out the basic concepts and data structures, then we can import them to other projects, and extend to more specialized classes via inheritance. 

There's been extensive software development in related areas. 
The XCMS ecosystem (https://www.bioconductor.org/packages/release/bioc/html/xcms.html) is a leading example of data preprocessing.
The modeling of metabolism is exemplified by the Escher project (https://github.com/zakandrewking/escher).
The advancing of science relies on the close interaction of experimental measurements and theoretical modeling, and the two should feed on each other. However, a clear gap exists between the two in metabolomics. E.g., the elemental mass table in Escher (retrieved on version 1.7.3) are of average mass, but mass spectrometers measure isotopic mass. 
Many software programs already have excellent data models and data structures. But the reuse of data models is much easier to start from basics, hence this project, where complexity is an option.


## Core data Structure

![Core data Structure](docs/datastru.png)

    Metabolic model:
        Compound (metabolite is a compound)
        Reaction
        Pathway
        Network
        Enzyme
        Gene
    Experimental data:
        Experiment
        EIC or XIC, i.e. massTrace or massTrack in LC-MS data
        Peak (Elution peak)
        Feature
        Empirical compound
        MSn spectra: MS^n data to annotate peak or feature

Try to keep the core models minimal. 
Leave index and query functions in applications.

Peaks are extracted from massTrace. A peak is specific to a sample, while a feature is specific to an experiment. 
A spectrum is a list of masses.
LC-MS is a composite of many spectra. MS^n is spectrum as product of a precursor, which is a peak.
After peaks are asigned to a feature or an empCpd, the annotation is transferred to the latter.

Internal structures of each class are not meant to be final. 
As long as a workflow is adhered to these core concepts, interoperability is easy to achieve.

## Serialized empCpd format (in JSON and can be implemented in any language)
 
    empCpd = {
    "neutral_formula_mass": 268.08077, 
    "neutral_formula": C10H12N4O5,
    "alternative_formulas": [],
    "interim_id": C10H12N4O5_268.08077,
    "identity": [
            {'compounds': ['HMDB0000195'], 'names': ['Inosine'], 
                    'score': 0.6, 'probability': null},
            {'compounds': ['HMDB0000195', 'HMDB0000481'], 'names': ['Inosine', 'Allopurinol riboside'], 
                    'score': 0.1, 'probability': null},
            {'compounds': ['HMDB0000481'], 'names': ['Allopurinol riboside'], 
                    'score': 0.1, 'probability': null},
            {'compounds': ['HMDB0003040''], 'names': ['Arabinosylhypoxanthine'], 
                    'score': 0.05, 'probability': null},
            ],
    "MS1_pseudo_Spectra": [
            {'feature_id': 'FT1705', 'mz': 269.0878, 'rtime': 99.90, 
                    'isotope': 'M0', 'modification': '+H', 'charged_formula': '', 'ion_relation': 'M+H[1+]'},
            {'feature_id': 'FT1876', 'mz': 291.0697, 'rtime': 99.53, 
                    'isotope': 'M0', 'modification': '+Na', 'charged_formula': '', 'ion_relation': 'M+Na[1+]'},
            {'feature_id': 'FT1721', 'mz': 270.0912, 'rtime': 99.91, 
                    'isotope': '13C', 'modification': '+H', 'charged_formula': '', 'ion_relation': 'M(C13)+H[1+]'},
            {'feature_id': 'FT1993', 'mz': 307.0436, 'rtime': 99.79, 
                    'isotope': 'M0', 'modification': '+K', 'charged_formula': '', 'ion_relation': 'M+K[1+]'},
            ],
    "MS2_Spectra": [
            'AZ0000711', 'AZ0002101'
            ],
    "Database_referred": ["Azimuth", "HMDB", "MONA"],
    }

An empCpd can be constructed without knowing the formula, by grouping features based on mass differences.
The "identity" can be a single compound or a mixture of compounds. 
How to compute the score or probability will be dependent on external algorithms to combine information from different annotation approaches.
Additional fields can be added as needed.


## This package is used in asari and mummichog 3.

* asari: Trackable and scalable metabolomics data preprocessing - https://github.com/shuzhao-li/asari

* mummichog3: core algorithm package for pathway/network analysis

* mummichog3-api: server and worker (RESTful) implementations

* mass2chem: common utilities in interpreting mass spectrometry data, annotation



## For developers

The data structures should be language neutral. 

We edit primarily in the Python code, as JSON and YAML can be exported automatically.
Each Python class has a serialization function to export JSON, which is selective.
I.e., concise information for users' need is exported, but not all class details.

Adaptation/update/extension is encouraged in other languages. 

We strive for the right level of abstraction.
For the core classes, it's more important to have transparent, extensible structure.
Therefore, it's a design decision not to have getter or setter functions. 
Shallow data structures are more portable.
MetDataModel provides a template, and application projects can extend it to fit their specific needs.

Please feel free to submit issues, and write Wiki pages for discussions.


### Related community resources
While we focus on the application of mass spectrometry data, 
many mass spectrometry data structures are defined in various software projects that focus on "pre-processing", e.g.

- openMS (https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Documentation/nightly/html/index.html) 

- MSnBase (used by XCMS, https://github.com/lgatto/MSnbase)

To learn about mass spectrometry concepts and pre-processing:

- Data structure described for (py)openMS (https://pyopenms.readthedocs.io/en/latest/datastructures.html)

- XCMS tutorial by Johannes Rainer (https://github.com/jorainer/metabolomics2018)

To learn about genome scale metabolic models:

- review by Gu et al, 2019 (https://link.springer.com/article/10.1186/s13059-019-1730-3)

- our book chapter to explain metabolic models in the context of metabolomic pathway analysis (https://link.springer.com/protocol/10.1007/978-1-0716-0239-3_19)


## History

This repo was renamed from Azimuth-metabolomics. All annotation functions are moved to mass2chem package.

