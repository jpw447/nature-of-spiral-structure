import os
'''
This script is used to retrieve the filenames from a particular colour band
and then store the names without the file extension in a .txt file.

The paths can be changed according to where the files are stored.
If run, the file will throw errors unless the paths are changed and there
is a folder containing all of the images in the format:
    
    ngc2442b.jpg
'''
if __name__ == "__main__":
    band = input("Which band do you want to check: ").upper()
    
    # Path strings
    # laptop_path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure"
    computer_path = "C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure"
    image_path = computer_path + "\\Good images"
    list_path = computer_path + "\\Good List\\{}-band_galaxies.txt".format(band)
    
    # Retrieving full file names
    files = os.listdir(image_path)
    # Removing 'B.jpg' extension from each
    galaxies = [file[:-5] for file in files]
    
    # Writing the names to a .txt file
    with open(list_path, 'w') as file:
        for galaxy in galaxies:
            file.write(galaxy+"\n")    