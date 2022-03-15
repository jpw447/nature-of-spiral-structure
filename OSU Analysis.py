import ArmAnalysis as aa

if __name__ == "__main__":
    band = input("Which colour band do you want to look at? ").upper()
    
    # Path strings
    # laptop_path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure"
    computer_path = "C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure"
    image_path = computer_path + "\\OSU\\data\\survey\ByFilter\\{}_band".format(band)
    list_path = computer_path + "\\Galaxy Lists\\{}-band_galaxies.txt".format(band)
    
    # Grabbing the list of galaxy names
    with open(list_path, 'r') as file:
        file_list = file.readlines()
        
    file_list = [file[:-1] for file in file_list]
    
    # Cycling through all the galaxies in a given band to look at
    for galaxy_name in file_list:
        aa.image_display(image_path, galaxy_name, band)