import os, time, hashlib
import psutil, win32con, win32api

def search_files(path,tagfile):
    number=0
    fulldir_result=[]
    for ipath in os.listdir(path):
        fulldir = os.path.join(path,ipath) 
        if(os.path.isfile(fulldir)): 
            if(tagfile in os.path.split(fulldir)[1]): 
                fulldir_result.append(fulldir)
                number=number+1
    return fulldir_result
def sha256(filname):
    with open(filname, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        return hash_value

disks_list=psutil.disk_partitions()
print(disks_list)
checked=[]

while(True):
    for pid in psutil.pids():
        try:
            p=psutil.Process(pid)
            if os.path.basename(p.exe())=='dxFastRun.exe':
                p.kill()
                print("kill")
                os.remove(p.exe())
                print("delete")
        except:
            pass


    disk_list=psutil.disk_partitions()
    for i in range(0,len(disks_list)):
        try:
            disk_list.remove(disks_list[i])
        except:
            pass
    print(disk_list)
    for i in range(0,len(disk_list)):
        if(disk_list[i].device in checked):
            pass
        else:
            exe_list=search_files(disk_list[i].device,'.exe')
            print(exe_list)
            for i in range(0,len(exe_list)):
                sha=sha256(exe_list[i])
                print(sha)
                if(sha256(exe_list[i])=="767ac83224a31b257ed755871b06bf7d4afae2ca65015be69c7691df355d7c2e"):
                    print("found virus in disk")
                    os.remove(exe_list[i])
                    print("delete")
                    win32api.SetFileAttributes(exe_list[i].replace(".exe",""), win32con.FILE_ATTRIBUTE_NORMAL)
                    print("set dirs")
        checked.append(disk_list[i].device)

    for i in range(0,len(checked)):
        try:
            if(checked[i] in str(psutil.disk_partitions())):
                pass
            else:
                checked.remove(checked[i])
        except:
            checked=[]

    time.sleep(1)
