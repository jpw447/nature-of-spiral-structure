# nature-of-spiral-structure

A project produced by Joe Williams and Palvinder Sall for the Third Year Physics Project PHYS3003 "Nature of Spiral Structure". The following text is repeated in the online diary under "Github Guide".

In ArmAnalysis, Drawing on Images, Name Grabbing and OSU Analysis, the directory will need to be edited in multiple places within the files for the code to be run. This is explained specifically in each file.

## ArmAnalysis.py
The key file containing the functions which convert images from FITS to JPEGs, and then allows the user to analyse the data for pitch angle, for any number of spiral arms, given a galactic centre the user has picked out. The plots can then be saved.

## Drawing on Images.py
Used to develop a method to draw on images and retrieve the co-ordinates for analysis, using OpenCV.

## Logarithmic Spirals.py
A runnable script that will produce a logarithmic spiral in polar and Cartesian form. Then calculates the pitch angle, plots it, and compares it against the theoretical value for any spiral.

## Name Grabbing.py
A temporary file used to retrieve a list of all the galaxy images in the dataset. Prevents the need for us to manually write down the names.

## OSU Analysis.py
A file used to import and utilise ArmAnalysis to convert images from FITS to JPEGs and then perform the actual pitch angle analysis.

## Redundant Files
Old files used for development that did not produce anything relevant to the final project, and whose files were only used for testing and practice code.
