# Basic module structure and each program functionality
Image is always processed in order showed here
## ImageValidation - Optional
> Tools to check if image is suitable for further processing based on specified criteria if not then 
> image is not further analysed

## ImagePreprocessing - Optional
> Tools to process image in order to enhance it's quality for further segmentation
> and target detection

## ImageSegmentation
> Algorithms to divide image into target pixels and background pixels. More than one may be selected, but 
> segmentation_fusion_method must also be used then to determine the way in which pixels are to be fused

## SegmentationFusion - Optional
> Tools to fuse segmentation output images (when more than one segmentation is used) into one based on some criteria

## InitialValidationAndPostprocessing - Optional
> Tools for validation or image processing (or both) after segmentation in order to make target detection easier or 
> determine that target detection is going to be impossible and stop further calculations

## TargetDetectionAlgorithms
> Just as written in module name, each algorithm outputs target coordinates and area
> covering all target pixels. May be used more than one, but TargetEstablishing will have to be used

## TargetEstablishing
> Tools establishing target coordinates in case user used more than one target detection
> algorithm

## TargetDetectionValidators
> Tools to determine if detected target is target or not

# Ready to use systems
> This module stores predefined systems so that they can be used to process images