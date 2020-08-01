'''

General data model for mass spec data


For Converting Emory IROA library to Python module

Shuzhao, 2020-07-29


library = {
    'metadata': {},
    'compounds': [],
}

metadata = {
    'library': 'IROA ', # need be more specific 
    'instrument': 'Orbitrap QE', # need be more specific 
    'chromatography_column': 'C18', #  need be more specific
    'chromatography_time': '10 minutes',
    'ionization': 'ESI',
    'ionization_mode': 'negative',
    'expt_contact': 'Ken Liu',
    'expt_data_generated': '2017', # need be more specific 
    'data_processed_by': 'Shuzhao Li',
    
}

# based on azimuth_metabolomics
# class annotatedCompound

annCpd = {
    'name': '',
    'neutral_formula':'',  # not same as observed in MS
    'inchi': '',
    'SMILES': '',
    'neutral_base_mass': 0.0000,
    'observed_mz': 0.0000,
    'observed_rtime': 0,
    'observed_ion': '',
    'parent_CID': '',   
    
    # better data model for a later day
    'peaks': {
				'M+H[1+]': 0,
				'M[1+]': 0,
				'M+Na[1+]': 0,
				#
				'M-H[1-]': 0,
				'M-H2O-H[-]': 0,
				'M-2H[2-]': 0,
			},
    
}



'''

class Experiment:
	'''
	type can be LC-MS, LC-MS/MS, GC-MS, LC-IMS, etc.
	
	The hierarchy is Experiment -> Features -> Peaks
	
	'''
	id = 1000
	input_data_from = ''
	type = 'LCMS'
	instrument = ''
	instrument_parameters = {}
	chromatography = ''
	chromatography_parameters = []
	
	preprocess_software = ''
	preprocess_parameters = {}
	
	
	
class Peak:
	'''
	Specific to a sample in an experiment.
	Preprocessing software extracts peaks per sample, then performs alignment.
	The alignment shifts m/z, rt etc values.
	For this class, pre-alignment is preferred. 
	
	But almost all data tables we have are post-alignment, 
	which are accommodated here by setting aligned=True.
	
	'''
	ms_level = 1					# MS levle - 1, 2. 3, etc.
	aligned = False
	
	mz = 0
	retention_time = 0
	collision_cross_section = 0 	# reserved for IM data
	
	intensity = 0
	intensity_value_by = 'area' 	# or height, etc.
	
	peak_shape = '' 				# need a method to define this
	
	feature_belonged = ''
	experiment_belonged = ''


class Feature:
	'''
	A feature is a peak that is aligned across samples.
	So this is experiment specific.
	'''
	ms_level = 1					# MS levle - 1, 2. 3, etc.
	mz = 0
	retention_time = 0
	collision_cross_section = 0 	# reserved for IM data
	
	intensity_sample_mean = 0
	intensity_sample_std = 0
	intensity_sample_cv = 0
	intensity_replicate_cv = 0
	
	experiment_belonged = ''





class EmpiricalCompound:
    '''
    # from mummichog
    
    EmpiricalCompound is a computational unit to include 
    multiple ions that belong to the same metabolite,
    and isobaric/isomeric metabolites when not distinguished by the mass spec data.
    Thought to be a tentative metabolite. 
    Due to false matches, one Compound could have more EmpiricalCompounds
    
    Can be Experiment specific for this class.
	experiment_belonged = ''

    We will have a cumulative list of annotatedCompound

	libraryCompound = annotatedCompound


    
    '''
    
    def __init__(self):
		'''
		An empCpd has one and only one base neutral mass
		'''
		self.neutral_base_mass = 0.0000
        
		self.peaks = {
				'M+H[1+]': 0,
				'M[1+]': 0,
				'M+Na[1+]': 0,
				#
				'M-H[1-]': 0,
				'M-H2O-H[-]': 0,
				'M-2H[2-]': 0,
			},
		
		self.MS2_spectra = [
			# or list of spectra?
		]

		self.top_compound = ''
		self.probable_compounds = []
        
    
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


class annotatedCompound(EmpiricalCompound):
	'''
	library compound will use same class


	'''
	self.observed_mass = 0.0000






