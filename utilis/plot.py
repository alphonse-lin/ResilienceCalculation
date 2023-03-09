import numpy as np
import matplotlib.pyplot as plt
import os

def show(data):
    plt.figure()
    plt.imshow(data)
    plt.show()

def save(data, path):
    plt.clf()
    plt.imshow(data)
    plt.savefig(path, bbox_inches='tight')

if __name__ == '__main__':
    asc_dir=r'data\output\asc'
    img_dir=r'data\output\image'

    files=os.listdir(asc_dir)
    plt.figure(figsize=(10,10),dpi=300)

    for file in files:
        if not os.path.isdir(file):
            if "h_" in file and file.endswith('asc'):
                asc_path=os.path.join(asc_dir, file)
                asc_data = np.loadtxt(asc_path, skiprows=6)
                
                file_name=file.split('.')[0]
                output_path=os.path.join(img_dir,file_name+".png")

                save(asc_data, output_path)
                print(file)
    