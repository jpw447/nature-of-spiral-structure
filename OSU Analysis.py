import ArmAnalysis as aa

if __name__ == "__main__":
    band = input("Which colour band do you want to look at?")
    filename = input("Which filename would you like to start with? (Do not include file extension)")
    
    # Going to need a .txt list of all the galaxy names too
    galaxy_name = "NGC 5054"
    
    path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure\\OSU\\data\\survey\ByFilter\\{}_band".format(band)
    aa.image_display(path, galaxy_name, band)