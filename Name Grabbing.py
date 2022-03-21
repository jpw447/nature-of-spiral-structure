import os
'''
This script is used to retrieve the filenames from a particular colour band
and then store the names without the file extension in a .txt file.

The paths can be changed according to where the files are stored.
'''
if __name__ == "__main__":
    band = input("Which band do you want to check: ").upper()
    
    # Path strings
    # laptop_path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure"
    computer_path = "C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure"
    image_path = computer_path + "\\OSU\\data\\survey\ByFilter\\{}_band".format(band)
    list_path = computer_path + "\\Galaxy Lists\\{}-band_galaxies.txt".format(band)
    
    # Retrieving full file names
    files = os.listdir('OSU\data\survey\ByFilter\{}_band'.format(band))
    # Removing '.fits' extension from each
    galaxies = [file[:-5] for file in files]
    
    # Writing the names to a .txt file
    with open(list_path, 'w') as file:
        for galaxy in galaxies:
            file.write(galaxy+"\n")    