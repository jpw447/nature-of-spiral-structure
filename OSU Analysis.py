import ArmAnalysis as aa

'''
This script calls functions from ArmAnalysis.py to display, analyse and save
images. The path strings can be changed depending on where the fits files
and .txt name lists are stored.
'''

if __name__ == "__main__":
    band = input("Which colour band do you want to look at? ").upper()
    
    # Path strings
    # laptop_path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure"
    computer_path = "C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure"
    image_path = computer_path + "\\OSU\\data\\survey\ByFilter\\{}_band".format(band)
    list_path = computer_path + "\\Galaxy Lists\\{}-band_galaxies.txt".format(band)
    save_path = computer_path + "\\Images"
    
    # Grabbing the list of galaxy na6mes and storing them
    with open(list_path, 'r') as file:
        file_list = file.readlines()
        
    # Calls image_display for a test
    # aa.image_display(image_path, save_path, 'ngc5054b', band)
        
    # Calls arm_drawing for a test
    aa.arm_drawing(image_path, save_path, 'ngc5054b', band, percentage=0.01)
    
    ### This block of code will cycle through every file in file_list using image_display
    '''
    # Removing "\n" delimiter
    file_list = [file[:-1] for file in file_list]
    
    # Cycling through all the galaxies in a given band to look at
    for galaxy_name in file_list:
        aa.image_display(image_path, save_path, galaxy_name, band)
    '''