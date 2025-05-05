from image_processing.processing_results.application_actions import ProcessingAudit
from image_processing.processing_results.consts import BEFORE_IMG_PROCESSING, AFTER_IMG_PROCESSING
from image_processing.processing_results.processing_results_interfaces import Convertable
from image_processing.processing_results.statistical_results import StatisticalResults, EntropyMeasures


class ProcessingResults:
    __processing_audit: ProcessingAudit

    __statistical_parameters_before_processing: StatisticalResults
    __entropy_measures_before_processing: EntropyMeasures

    __statistical_parameters_after_processing: StatisticalResults
    __entropy_measures_after_processing: EntropyMeasures


    def add_operations_audit_data(self, processing_audit: ProcessingAudit):
        self.__processing_audit = processing_audit

    def add_statistical_parameters_before_processing(self, statistical_parameters: StatisticalResults):
        self.__statistical_parameters_before_processing = statistical_parameters

    def add_statistical_parameters_after_processing(self, statistical_parameters: StatisticalResults):
        self.__statistical_parameters_after_processing = statistical_parameters

    def add_entropy_measures_before_processing(self, entropy_measures: EntropyMeasures):
        self.__entropy_measures_before_processing = entropy_measures

    def add_entropy_measures_after_processing(self, entropy_measures: EntropyMeasures):
        self.__entropy_measures_after_processing = entropy_measures

    def toDict(self) -> dict:
        return {
            **ProcessingResults.__convert_obj(self.__processing_audit),
            **ProcessingResults.__convert_obj(self.__statistical_parameters_before_processing,
                                              lambda k: k + '_' + BEFORE_IMG_PROCESSING),

            **ProcessingResults.__convert_obj(self.__entropy_measures_before_processing,
                                              lambda k: k + '_' + BEFORE_IMG_PROCESSING),

            **ProcessingResults.__convert_obj(self.__statistical_parameters_after_processing,
                                              lambda k: k + '_' + AFTER_IMG_PROCESSING),

            **ProcessingResults.__convert_obj(self.__entropy_measures_after_processing,
                                              lambda k: k + '_' + AFTER_IMG_PROCESSING)
        }

    @staticmethod
    def __convert_obj(convertable_obj: Convertable, key_mapper=lambda k: k) -> dict:
        output_dict = {}

        for k, v in convertable_obj.to_dict():
            output_dict[key_mapper(k)] = v

        return output_dict
