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

    metabolic model

        compound
        reaction
        pathway
        network

    data model
        
        peak
        feature
        experiment
        empirical compound

Try to keep the core models minimal. 
Leave index functions in util or applications.

## empCpd format (JSON)
 
    {"neutral_base_mass": 0, 
      "list_of_features": [
                # feature, ion, [m/z, rtime, mean_intensity]
                {'feature': '', 'ion': 'M-H[1-]', 'm/z': 169.0013, 'rtime': 55},
                {},
                # ...
            ],
      "identity": {
                # compound(mixtures): probability
                (compound x): 0.6,
                (compound y, compound z): 0.2,
        }
    }


## The mummichog suite 

This package is used in mummichog 3.

* mummichog(3): core algorithm package for pathway/network analysis

* cloud-mummichog: server and worker (RESTful) implementations

* Azimuth DB: the chemical database for biology, including metabolic models

* metDataModel: data models for metabolomics, used by mummichog and Azimuth DB

* mass2chem: common utilities in interpreting mass spectrometry data, annotation

* massBrowser: visualization using js


## For developers

Python code is used as example, but this should be language neutral.

Need better use of operators (getters, setters) in Python code

Minimal JSON formats should be used for mummichog project.

YAML should be equivalent to JSON.

Use Wiki pages for detailed discussions.


### Related community resources
While we focus on the application of mass spectrometry data, 
many mass spectrometry data structures are defined in various software projects that focus on "pre-processing", e.g.

- openMS (https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Documentation/nightly/html/index.html) and (https://pyopenms.readthedocs.io/en/latest/datastructures.html)

- MSnBase (used by XCMS, https://github.com/lgatto/MSnbase)


## History

This repo was renamed from Azimuth-metabolomics. All annotation functions are moved to mass2chem package.