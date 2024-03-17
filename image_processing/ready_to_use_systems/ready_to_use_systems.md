# Ready to use systems
This module stores predefined systems so that they can be used to process images. 

IMPORTANT
Every method is designed to process images that are in greyscale and are registered in thermovision

## luminance_threshold_based_system
```
Simple algorithm that will by default consider all pixels that have luminance greater or equal to 80 as target pixels 
and other as background. Target coordinates will be established by mean shift algorithm (in simplest terms target 
will be an area where there is the most white pixels after segmentation)
```

## information_entropy_based_system
```
Algorithm that will perform segmentation based on pixels information entropy (which will be slower due to histogram
calculation for each image) and canny contour detection. Target coordinates will be established by mean shift algorithm
```
