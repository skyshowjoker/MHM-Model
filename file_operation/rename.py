import os

import xlrd


def rename():
        path = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\nii_list_Mar"
        label = r"C:\joey\master\resource\lymphoma\dataset\third_label_data\tag"
        fileList = os.listdir(path)
        fileList.sort()
        n = 0
        for file in fileList:
                # 设置旧文件名（就是路径+文件名）
                print(file)
                oldname1 = path + os.sep + file  # os.sep添加系统分隔符
                # oldname2 = label + os.sep + file  # os.sep添加系统分隔符
                code = "lymphoma_%03.0d" % int(file.split(".")[0])
                # code = "%d" % n
                newname1 = path + os.sep + code + "_0000.nii.gz"
                # newname2 = label + os.sep + code + ".nii.gz"
                # os.rename(newname1, oldname1)
                os.rename(oldname1, newname1)  # 用os模块中的rename方法对文件改名
                # os.rename(oldname2, newname2)
                print(oldname1, '======>', newname1)
                n += 1
def rename_dcm(path):
        fileList = os.listdir(path)

        for sublist in fileList:
                sublist = path + os.sep + sublist
                print(sublist)
                n = 0
                files = os.listdir(sublist)
                for file in files:
                        # 设置旧文件名（就是路径+文件名）
                        print(file)
                        oldname1 = sublist + os.sep + file # os.sep添加系统分隔符
                        # oldname2 = label + os.sep + file  # os.sep添加系统分隔符
                        # code = "lymphoma_%03.0d" % int(file.split(".")[0])
                        code = "%d" % n
                        newname1 = sublist + os.sep + code + ".dcm"
                        # newname2 = label + os.sep + code + ".nii.gz"
                        # os.rename(newname1, oldname1)
                        os.rename(oldname1, newname1)  # 用os模块中的rename方法对文件改名
                        # os.rename(oldname2, newname2)
                        print(oldname1, '======>', newname1)
                        n += 1
def rename_ng_zip_file_according_excel():
    excel = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\map_name_number_list(all_label--match_label_dicom).xlsx'
    label_dir = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\all_label'
    workbook = xlrd.open_workbook(excel)
    table = workbook.sheet_by_name('sheet1')
    rows = table.nrows

    files = os.listdir(label_dir)
    print(files)
    for file in files:
            for i in range(0, rows):
                    print(table.cell(i, 0).value)
                    if file.__contains__(table.cell(i, 0).value):
                    # if(file == str(table.cell(i, 1).value).split('.')[0]):
                        oldname = label_dir + os.sep + file
                        newname = label_dir + os.sep + str(int(table.cell(i, 1).value))
                        os.rename(oldname, newname)
                        print(oldname, '======>', newname)
                        continue
if __name__ == '__main__':
        path = r'C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\output_fold'
        rename_ng_zip_file_according_excel()