from InformationGainAnalysis.Master import Master

test = Master()
test.set_main_folder('D:/artykuly/wat_2/test_animations/const_h')
"""
test.choose_data('animacje_testowe', 'h40m_r50m')
test.analyze_dataset(
    mode='void',
    dataset_validation=False)
"""
test.choose_object('deer')

#test.analyse_all_datasets_for_single_object(mode='mixed', dataset_validation=False, limit_of_img_per_dataset=1000)

data_from_db = test.load_data().all_data_for_object_from_db(scope='object', validation='full')

test.set_data_from_db(data_from_db)

test.plot().with_respect_to_group_by_dataset(x='file', y='entropy_of_segmented_image', translate_names_to_deg=True)
test.plot().scatter_plot_3d()

"""
test.analyse_histogram_of_all_dataset(limit=5)
test.load_data_from_db()
test.plot_data_with_respect_to('scatter', "distance_to_object", "entropy_of_segmented_image")

#test.complete_analysis_of_whole_dataset(object='daniel', limit_of_img_per_dataset=2000)
#test.complete_analysis_of_whole_dataset(object='zajac', limit_of_img_per_dataset=2000)
#test.complete_analysis_of_whole_dataset(object='dzik', limit_of_img_per_dataset=2000)
#test.complete_analysis_of_whole_dataset(object='sarna', limit_of_img_per_dataset=1500)


test.choose_object('dzik')
test.load_data_from_db(scope='object',
                       validation='none')
test.plot_data_with_respect_to_group_by_dataset('scatter',
                                                "time",
                                                "entropy_of_segmented_image")

"""

"""dzik, 2021-02-23T235735"""
"""sarna, 2021-02-04T204006"""

"""test.choose_data('dzik', '2021-02-23T235735')

test.analyze_dataset_with_flight_parameters_from_log_file(
        mode='mixed',
        limit=20)"""

"""
test.analyse_histogram_of_all_dataset(limit=5)
test.load_data_from_db()
test.plot_data_with_respect_to('scatter', "distance_to_object", "entropy_of_segmented_image")
"""
# test.complete_analysis_of_whole_dataset(object='sarna', mode='mixed', limit_of_img_per_dataset=400)
#test.choose_object('sarna')
# test.choose_data('sarna', '2021-02-04T182803')
# test.analyse_histogram_of_all_dataset()

"""test.choose_object('sarna')
test.load_data_from_db(scope='object',
                       validation='full')

test.plot_data_with_respect_to_group_by_dataset("scatter", "horizontal_angle_of_view", "vertical_angle_of_view")"""
#test.save_figures_for_whole_dataset()

#test.analyse_histogram_of_all_dataset()
"""
test.choose_object('dzik')
dzik1_histogram = test.get_data_from_db({"object": "dzik", "file": "2021 02 23 23 57 56 005.tiff"})
dzik2_histogram = test.get_data_from_db({"object": "dzik", "file": "2021 02 04 23 37 15 249.tif"})
test.choose_object('zajac')
zajac1_histogram = test.get_data_from_db({"object": "zajac", "file": "2021 02 02 20 04 27 501.tif"})
zajac2_histogram = test.get_data_from_db({"object": "zajac", "file": "2021 02 04 05 32 32 226.tif"})
test.choose_object('daniel')
daniel1_histogram = test.get_data_from_db({"object": "daniel", "file": "2021 02 05 00 46 25 807.tif"})
daniel2_histogram = test.get_data_from_db({"object": "daniel", "file": "2021 02 02 20 40 50 798.tif"})
test.choose_object('sarna')
sarna1_histogram = test.get_data_from_db({"object": "sarna", "file": "2021 02 04 18 28 03 883.tif"})
sarna2_histogram = test.get_data_from_db({"object": "sarna", "file": "2021 02 04 23 25 42 075.tif"})

test.match_img_with_pattern(img=None, target_histogram=dzik1_histogram)
test.match_img_with_pattern(img=None, target_histogram=dzik2_histogram)
test.match_img_with_pattern(img=None, target_histogram=zajac1_histogram)
test.match_img_with_pattern(img=None, target_histogram=zajac2_histogram)
test.match_img_with_pattern(img=None, target_histogram=daniel1_histogram)
test.match_img_with_pattern(img=None, target_histogram=daniel2_histogram)
test.match_img_with_pattern(img=None, target_histogram=sarna1_histogram)
test.match_img_with_pattern(img=None, target_histogram=sarna2_histogram)


test.load_all_classes_of_objects_data('detected')
test.plot_data_comparing_all_classes_of_object(oy="distance_to_object")
"""

"""
test.plot_data_with_respect_to_group_by_dataset('scatter',
                                                "time",
                                                "entropy_of_segmented_image")
                                                
test.plot_data_with_respect_to_group_by_dataset('scatter', "pitch", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "roll", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "yaw", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "distance_to_object", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "barometric_height", "entropy_of_segmented_image")


test.plot_data_with_respect_to_group_by_dataset('scatter', "horizontal_angle_of_view", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "vertical_angle_of_view", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "mean", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "entropy_of_image", "entropy_of_segmented_image")"""
