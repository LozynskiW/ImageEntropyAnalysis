from InformationGainAnalysis.Master import Master
from InformationGainAnalysis.Master import AnalysisMaster
from InformationGainAnalysis.image_processing import ready_to_use_systems as ready_systems

test = Master()
test.set_main_folder('D:/artykuly/wat_2/test_animations')
test.set_image_processing_blackbox(ready_systems.information_entropy_based_system)

verbose_mode = False
ready_systems.global_verbose_mode = verbose_mode

test.choose_object('deer')
datasets = ['h70m_r80m', 'h70m_r90m', 'h70m_r100m']

data_from_db = test.load_data().multiple_datasets_for_one_object(datasets=datasets, validation_type_for_all=None)

test.set_data_from_db(data_from_db)

test.analyze_dataset(save_to_db=False, verbose_mode=verbose_mode)

test.plot().with_respect_to_group_by_dataset(x='file', y='entropy_of_segmented_image',
                                             legend=True, translate_names_to_azimuthal_angle=True, mode='save')

"""
test.choose_data('animacje_testowe', 'h40m_r50m')
test.analyze_dataset(
    mode='void',
    dataset_validation=False)
"""
"""
for obj_class in ['deer', 'wild_boar', 'rabbit']:
    test.choose_object(obj_class)
    test.analyse_all_datasets_for_single_object(mode='mixed', dataset_validation=False, limit_of_img_per_dataset=3000)
"""

"""
test.choose_object('deer')
for folder in ['h70m_r80m', 'h70m_r90m', 'h70m_r100m',
               'h80m_r40m', 'h80m_r50m', 'h80m_r60m', 'h80m_r70m', 'h80m_r80m', 'h80m_r90m', 'h80m_100m',
               'h90m_r40m', 'h90m_r50m', 'h90m_r60m', 'h90m_r70m', 'h90m_r80m', 'h90m_r90m', 'h90m_100m',
               'h100m_r40m', 'h100m_r50m', 'h100m_r60m', 'h100m_r70m', 'h100m_r80m', 'h100m_r90m', 'h100m_100m']:
    test.choose_folder(folder)
    test.analyze_dataset(mode='mixed', dataset_validation=False, limit=3000)
"""