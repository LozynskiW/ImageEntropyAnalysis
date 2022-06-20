# Basic module structure and each program functionality

## ImageValidation
> Tools to check if image is suitable for further processing based on criteria specified
> in tool and user

## ImagePreprocessing
> Tools to process image in order to enhance it's quality for further segmentation
> and target detection

## ImageSegmentation
> Algorithms to divide image into target pixels and background

## SegmentationFusion
> Tools to fuse segmentation output images into one based on some criteria if user decided
> to use more than one image segmentation algorithm

## InitialValidationAndPostprocessing
> Tools to validate or process (or both) segmented image in order to make target
> detection easier

## TargetDetectionAlgorithms
> Just as written in module name, each algorithm outputs target coordinates and area
> covering all target pixels

## TargetEstablishing
> Tools establishing target coordinates in case user used more than one target detection
> algorithm