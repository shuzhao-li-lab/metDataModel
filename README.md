# metDataModel

Data models for metabolomics 
(renamed from Azimuth-metabolomics)


## Structure (tentative)

    metabolic model

        compound
        reaction
        pathway


    data model
        
        peak
        feature
        experiment
        empirical compound



## All annotation functions are in mass2chem package.

Change metDataModel -> mass2chem



## The mummichog suite include

* mummichog(3): core algorithm package for pathway/network analysis

* cloud-mummichog: server and worker (RESTful) implementations

* Azimuth DB: the chemical database for biology, including metabolic models

* metDataModel: data models for metabolomics, used by mummichog and Azimuth DB

* mass2chem: common utilities in interpreting mass spectrometry data, annotation

* massBrowser: visualization using js

