#-------------------------------------------------------------------------------
# Name:        range2cidr
# Version:     1.2
# Purpose:     Converts IP ranges to CIDR form
#
# Author:      Ender Akbas @endr_akbas
#
# Created:     08.04.2015
#-------------------------------------------------------------------------------
import argparse
import os
import re

def reg(list):
    ipler = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',list)
    return ipler
    
def calculate(iprange):
    part1 = "".join(iprange.split('-')[0])          #first part of ip range
    part2 = "".join(iprange.split('-')[1])          #second part of ip range

    mask = 0        #subnet mask
    subnet = ""     #result as CIDR
    sub = ""

    #compare octets
    for i in range(0,4):
        #add 8 for same octets
        if (part1.split('.')[i] == part2.split('.')[i]):
            mask += 8
            subnet += "".join(part1.split('.')[i]) + "."

            continue

        #compare bit by bit for non-same octets
        else:
            diff1 = format(int(part1.split('.')[i]), '#010b')[2:]
            #binary format of octet

            #binary format of octet
            diff2 = format(int(part2.split('.')[i]), '#010b')[2:]

            #compare bit by bit for non-same octets
            for bit in range(0,8):
                if (diff1[bit] == diff2[bit]):
                    mask += 1
                    sub += diff1[bit]
                    #print sub

                else:
                    sub += "0"

            strSub = str(int(sub,2))

            subnet += strSub + "."
            for x in range(i+1,4):
                subnet += "0" + "."
            subnet = subnet[:-1]
            subnet += "/" + str(mask)
            break
    return subnet
####################

parser = argparse.ArgumentParser(description='Converts IP ranges to CIDR form')
parser.add_argument('-f','--file', dest='filename', required=True,
                   help='The file that contains IP ranges')
parser.add_argument('-o','--outfile', dest='outfile',
                   help='Output file')
#parser.add_argument('-u','--url', dest='url',
                   help='URL of list')

args = parser.parse_args()

if not os.path.exists(args.filename):
    parser.error("Specified file not found")

else:
    f = open(args.filename,'r')
    dosya = f.read()
    ips = reg(dosya)

    if args.outfile:
        fo = open(args.outfile,'w+')
        for ipx in ips:
            fo.write(calculate(ipx)+'\n')
        fo.close()
    else:
        for ipx in ips:
            print calculate(ipx)
    f.close()


