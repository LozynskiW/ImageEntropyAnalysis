# ImageEntropyAnalysis
Application allows for information entropy analysis of 2D image data. Analysis outcome can be stored in No-SQL database 
and then recovered and plotted for better understanding of underlying data. **Application is still under development.**

## Why was it created

Application was created as a tool to analyse statistical properties of black and white uint8 thermal images.

## What does it do?

Application as a whole can be used to process datasets consisting of 2D black and white images by one 
of defined processing tools in order to calculate some statistical (or other) measures of given image. 
These measures can them be saved as json document in NO-SQL database and read in order to plot and further
analyse outcomes. 

Furthermore, application allows to generate datasets in Blender 3D with possibility to calculate 
trajectories for objects in Blender (if someone wanted to simulate movement of camera or object).

## Overview of architecture

Application consists of modules. Some of them are separate small applications, some works like a modular monolith.

### **Quick start:**

### /examples

Scripts to quickly use application in use cases that I mostly needed

### **Standalone modules:**

### /blender3d_integration
Mostly standalone scripts used to integrate with Blender 3D

    -> blender_files
        Blender project that contains all objects used to generate datasets
    
    -> blender_python
        Scripts that can be used to build commands to script trajectory in Blender 3D
    
    -> blender_scripts
        Python scripts that can be used from inside Blender

    -> trajectories_api
        Python scripts used to generate trajectories for objects in Blender

### /consts
Just constant values to reuse in application

### /data_analysis
Utils to calculate statistical parameters

### /data_unification
Utils to be used when creating charts for multiple datasets when some mapping is needed

### /data_visualisation
Charts definitions and objects to plot data

### /legacy
Old version of application. Still left to compare new version.

### **Core**

### /application_management
Main scripts that allow to orchestrate whole application - facade for application.

### /data_management
Connection to database, CRUD operations

### /image_processing
All algorithms and tools to process image (processing - segmentation / target detection / validation etc.)
