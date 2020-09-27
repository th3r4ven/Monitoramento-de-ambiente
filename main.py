#  Copyright (c) 2020.
#  This code was designed and created by TH3R4VEN, its use is encouraged for academic and professional purposes.
#  I am not responsible for improper or illegal uses
# Follow me on GitHub: https://github.com/th3r4ven
import psutil
import sys
from subprocess import call as command
from psutil._common import bytes2human
from time import sleep
from log import createLog
import mysql.connector
import pickle


def menu():
    count = 1
    print("[+]\tSystem Monitor created by mtorres\n")
    print("[*]\tCPU Info:")
    print("[**]\t\tCPUs Available: " + str(psutil.cpu_count(logical=True)))
    for use in CPUUsageSepPercent():
        print("[**]\t\tUsage Percent CPU " + str(count) + ": " + str(use) + "%")
        count += 1
    print("[**]\t\tUsage Percent (Total): " + str(CPUUsagePercent()) + "%")
    print("\n[*]\tRAM Info:")
    print("[**]\t\tTotal: " + str(totalRAM()))
    print("[**]\t\tUsage Percent: " + str(RAMUsagePercent()) + "%")
    print("\n[*]\tDisk Info (MountPoint /):")
    print("[**]\t\tTotal:" + str(DiskTotal()))
    print("[**]\t\tUsage Percent:" + str(DiskUsagePercent()) + "%")
    configurations()


def configurations():
    print("\n[+] Set yours thresholds [*]")
    thresholds = []

    try:
        thresholds.append(float(input("CPU percent usage thresholds: ")))
        thresholds.append(float(input("RAM percent usage thresholds: ")))
        thresholds.append(float(input("Disk percent usage thresholds: ")))

        Monitor(thresholds, input("Root Database password: "))
    except TypeError and ValueError:
        main()


def Monitor(thresholds, dbpassword):
    CPUthresholds = thresholds[0]
    RAMthresholds = thresholds[1]
    Diskthresholds = thresholds[2]
    while True:
        TotalCPUUsagePercent = CPUUsagePercent()
        SepCPUUsagePercent = CPUUsageSepPercent()

        TotalRAMUsagePercent = RAMUsagePercent()
        TotalDiskUsagePercent = DiskUsagePercent()

        command(['clear'])
        count = 1
        print("[+]\tSystem Monitor created by mtorres\n")
        print("[*]\tCPU Info:")
        print("[**]\t\tCPUs Available: " + str(psutil.cpu_count(logical=True)))
        for use in SepCPUUsagePercent:
            print("[**]\t\tUsage Percent CPU " + str(count) + ": " + str(use) + "%")
            count += 1
        print("[**]\t\tUsage Percent (Total): " + str(TotalCPUUsagePercent) + "%")
        print("\n[*]\tRAM Info:")
        print("[**]\t\tTotal: " + str(totalRAM()))
        print("[**]\t\tUsage Percent: " + str(TotalRAMUsagePercent) + "%")
        print("\n[*]\tDisk Info (MountPoint /):")
        print("[**]\t\tTotal:" + str(DiskTotal()))
        print("[**]\t\tUsage Percent:" + str(TotalDiskUsagePercent) + "%")

        if TotalCPUUsagePercent >= CPUthresholds:
            createLog("Total CPU", CPUthresholds, TotalCPUUsagePercent)
        count = 1
        for usage in SepCPUUsagePercent:
            if usage >= CPUthresholds:
                createLog("CPU " + str(count), CPUthresholds, usage)
                count += 1

        if TotalRAMUsagePercent >= RAMthresholds:
            createLog("RAM", RAMthresholds, TotalRAMUsagePercent)

        if TotalDiskUsagePercent >= Diskthresholds:
            createLog("Disk", Diskthresholds, TotalDiskUsagePercent)

        # Start monitoring database processlist

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=dbpassword
        )
        db = mydb.cursor()
        db.execute("show processlist")
        result = db.fetchall()
        dblog = {}
        count = 0
        for output in result:
            dblog[count] = {
                "id": output[0],
                "user": output[1],
                "host": output[2],
                "db": output[3],
                "command": output[4],
                "time": output[5],
                "state": output[6],
                "info": output[7],
                "progress": output[8],
            }
            count += 1

        with open('dblog.txt', 'wb') as arq:
            pickle.dump(dblog, arq)
        arq.close()
        db.close()


def CPUUsageSepPercent():
    return psutil.cpu_percent(interval=1, percpu=True)


def CPUUsagePercent():
    return psutil.cpu_percent(interval=1)


def DiskTotal():
    diskinfo = psutil.disk_usage('/')
    for name in diskinfo._fields:
        if name == 'total':
            value = getattr(diskinfo, name)
            return bytes2human(value)


def DiskUsagePercent():
    diskinfo = psutil.disk_usage('/')
    for name in diskinfo._fields:
        if name == 'percent':
            value = getattr(diskinfo, name)
            return float(value)


def totalRAM():
    memory = psutil.virtual_memory()

    for name in memory._fields:
        if name == 'total':
            value = getattr(memory, name)
            return bytes2human(value)


def RAMUsagePercent():
    raminfo = psutil.virtual_memory()
    for name in raminfo._fields:
        if name == 'percent':
            return getattr(raminfo, name)


def main():
    command(['clear'])
    menu()


if __name__ == '__main__':

    try:
        mode = sys.argv[1].lower()
    except IndexError:
        mode = "normal"

    try:
        if mode == "silence":
            dbpassword = ""
            thresholds = [70, 80, 60]
            Monitor(thresholds, dbpassword)
        else:
            main()
    except KeyboardInterrupt:
        command(['clear'])
        exit()


#
# while True:
#     print(psutil.cpu_percent(interval=1))
#     print(psutil.virtual_memory())
