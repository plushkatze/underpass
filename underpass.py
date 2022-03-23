import socket
import time
import multiprocessing

def sockbounce(s,target, host, port):
    print("relay started", host, port)
    s.settimeout(10)
    try:
        while True:
            print("awaiting data")
            data1, addr1 = s.recvfrom(1420)
            print("r ", addr1, " : ", data1)
            target.sendto(data1, (host, port))
    except socket.timeout:
        print("contact gone silent. killing socket")
        s.close()

def awaitturns(s1,s2):
    print("awaitturns started")
    data1, addr1 = s1.recvfrom(1420)
    data2, addr2 = s2.recvfrom(1420)
    print("received %s from s1", data1)
    print("received %s from s2", data2)
    s1.sendto(data2, addr1)
    s2.sendto(data1, addr2)
    # activate bouncemode
    bounceleft  = multiprocessing.Process(target=sockbounce, args=(s1, s2, addr2[0], addr2[1])) 
    bounceright = multiprocessing.Process(target=sockbounce, args=(s2, s1, addr1[0], addr1[1])) 
    bounceleft.start()
    bounceright.start()

# management socket
sockx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockx.bind(("0.0.0.0", 51337))
magic = bytes([0x54, 0x55, 0x52, 0x4e, 0x4d, 0x45]) # TURNME

def managementsocket():
    print("TURN started")
    while True:
        print("awaiting datax")
        datax, addrx = sockx.recvfrom(1420)
        print(datax)
        print(magic)
        if (datax == magic):
            print("turnme request, generating portpair...")
            s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s1.bind(("0.0.0.0", 0))

            s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s2.bind(("0.0.0.0", 0))
            
            pairtosend = str(s1.getsockname()[1]) + "::" + str(s2.getsockname()[1])

            sockx.sendto(str.encode(pairtosend), addrx)
            turnproc = multiprocessing.Process(target=awaitturns, args=(s1,s2)) 
            turnproc.start()

psx = multiprocessing.Process(target=managementsocket)
psx.start()


exit 
manager = multiprocessing.Manager()
maddr1 = manager.Value("maddr1", "0")
maddr2 = manager.Value("maddr2", "0")
mport1 = manager.Value("mport1", 0)
mport2 = manager.Value("mport2", 0)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind(("0.0.0.0", 31337))

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind(("0.0.0.0", 31338))


data1, addr1 = sock1.recvfrom(1420)
data2, addr2 = sock2.recvfrom(1420)
print("received %s from sock1", data1)
print("received %s from sock2", data2)
sock1.sendto(data2, addr1)
sock2.sendto(data1, addr2)

maddr1.value=addr1[0]
mport1.value=addr1[1]

maddr2.value=addr2[0]
mport2.value=addr2[1]

def sock1reader():
    print("relay1 started")
    while True:
        print("awaiting data1")
        data1, addr1 = sock1.recvfrom(1420)
        if (mport1.value != addr1[1]):
            print("changed1")
            mport1.value=addr1[1]
        print("r1 ", addr1)
        sock2.sendto(data1, (maddr2.value, mport2.value))

def sock2reader():
    print("relay2 started")
    while True: 
        print("awaiting data2")
        data2, addr2 = sock2.recvfrom(1420)
        if (mport2.value != addr2[1]):
            print("changed2")
            mport2.value=addr2[1]
        print("r2 ", addr2)
        sock1.sendto(data2, (maddr1.value, mport1.value))

print("WARNING: underpass is not finished yet, do not use for production")
ps1 = multiprocessing.Process(target=sock1reader)
ps2 = multiprocessing.Process(target=sock2reader)
ps1.start()
ps2.start()

