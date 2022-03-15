import os

band = input("Which band do you want to check: ").upper()

# Path strings
# laptop_path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure"
computer_path = "C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure"
image_path = computer_path + "\\OSU\\data\\survey\ByFilter\\{}_band".format(band)
list_path = computer_path + "\\Galaxy Lists\\{}-band_galaxies.txt".format(band)

files = os.listdir('OSU\data\survey\ByFilter\{}_band'.format(band))
galaxies = [file[:-5] for file in files]

with open(list_path, 'w') as file:
    for galaxy in galaxies:
        file.write(galaxy+"\n")    

#%%
x = []
with open(list_path, 'r') as file:
    data = file.readlines()