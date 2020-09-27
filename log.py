#  Copyright (c) 2020.
#  This code was designed and created by TH3R4VEN, its use is encouraged for academic and professional purposes.
#  I am not responsible for improper or illegal uses
# Follow me on GitHub: https://github.com/th3r4ven
from datetime import datetime


def readLogFile():
    with open("monitorLog.txt", 'rt') as arq:
        content = arq.read()
    arq.close()
    log = []
    for line in content.split("\n"):
        log.append(line)
    return log


def getData():
    now = datetime.now()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def createLog(hardware, thresholds, MachineUsage):
    log = readLogFile()
    log.append(
        "[*] Hardware:" + str(hardware) + " | Thresholds :" + str(thresholds) + " | Machine Usage: " + str(MachineUsage)
        + " | TIME: " + str(getData()))
    with open("monitorLog.txt", 'wt') as arq:
        for line in log:
            arq.write(line + "\n")
    arq.close()

