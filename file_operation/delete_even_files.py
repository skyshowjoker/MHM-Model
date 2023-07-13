import os

def delete_even_files(dir):
    files = os.listdir(dir)
    count=1
    for file in files:
        if count % 2 == 0:
            os.remove(dir+"\\"+file)
            print(dir+"\\"+file)
        count+=1

if __name__ == '__main__':
    path=r"C:\joey\master\resource\lymphoma\dataset\third_label_data\t2_dicom3"
    dirs = os.listdir(path)
    for dir in dirs:
        files = os.listdir(path+os.sep+dir)
        if len(files) > 27:
            # delete_even_files(path+os.sep+dir)
            print(dir)

    # delete_even_files(path)