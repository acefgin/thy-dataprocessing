import os, csv, shutil, sys
 
def nameMapLkUp(filename):
    
    LkUp = {}
    with open(filename,'r') as csvfile:
        items = csv.reader(csvfile, delimiter=',')
        idx = 0
        for row in items:
            if idx == 0:
                idx += 1
                continue
            #print(row)
            LkUp[row[1]] = row[0]
    return LkUp
 
# Driver Code
if __name__ == '__main__':
     
    nameMapLkUpFile = "nameMap_lookup.csv"
    nameMapIDTb = nameMapLkUp(nameMapLkUpFile)
    cwd = os.path.dirname(__file__)

    dropFolder = sys.argv[1]
    folder = os.path.splitext(os.path.basename(dropFolder))[0]
    for count, filename in enumerate(os.listdir(folder)):
        
        if "EV" in filename or "report" in filename:
            continue
        nameTxt, extension = os.path.splitext(filename)
        info = nameTxt.split("-")
        
        barcode = info[1]
        
        if barcode not in nameMapIDTb:
            continue
        dstName = nameMapIDTb[barcode]
        
        dst = "{}{}".format(dstName,extension)
        print(filename + "  ==>  "+ dst)
        src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        if not os.path.isdir(f"{folder}/nameMapped"):
            os.mkdir(f"{folder}/nameMapped")
        dst =f"{folder}/nameMapped/{dst}"
        
        shutil.copyfile(src, dst)
