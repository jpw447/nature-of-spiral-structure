import os

while True:
    band = input("Which band do you want to check: ").upper()
    
    files = os.listdir('OSU\data\survey\ByFilter\{}_band'.format(band))
    galaxies = [file[:-5] for file in files]
    
    with open("Galaxy Lists\\{}-band_galaxies.txt".format(band), 'w') as file:
        for galaxy in galaxies:
            file.write(galaxy+"\n")
    