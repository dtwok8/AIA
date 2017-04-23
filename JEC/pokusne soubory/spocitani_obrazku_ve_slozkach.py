import os, os.path

path = "/home/kate/NetBeansProjects/bakalarka/Data/iaprtc12/images/"
# simple version for working with CWD
count_images=0
count_directory = 0

for i in os.listdir(path):
    if(os.path.isdir(os.path.join(path, i))):
        count_directory = count_directory + 1
        for y in os.listdir(os.path.join(path, i)):
            if(os.path.isfile(os.path.join(path, i, y))):
                count_images = count_images + 1

print "{} obrazku ve {} slozkach".format(count_images, count_directory)

#print len([name for name in os.listdir(folder) if os.path.isfile(name)])
#print len([name for name in os.listdir('.') if os.path.isfile(name)])

# path joining version for other paths
#DIR = '/tmp'
#print len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])