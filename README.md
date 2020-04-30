# Azimuth-metabolomics

Data models for metabolomics


## Use

* import all models to mummichog

  mummichog no longer contains metabolic models, but depends on this package

* Serve community as Azimuth DB API?

* Support a web interface for people to browse and edit (with permited access)





## Structure (tentative)


### ./azimuth_metabolomics
    metabolicModel.py
        compound
        reaction
        pathway



    experimentalData.py
        contaminants (from ../spectrometry)
        empirical compound
        peaks

        spectra

        source experiment

    data/

        shipped metabolic models (Genome-scale)
        and metabolite properties

    utils/

To compile models from Azimuth DB


How to convert

downloaed JSON -> py models


download 
  contaminants.tsv
  references.tsv

How to build models

from EBI, etc.

### ./spectrometry

mass spec related data 
contaminants.tsv

### ./identifiers

Identifier mapping btw databases and metabolic models


