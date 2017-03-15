import sys, getopt
import configparser
from coreapp.vendors import Vendor
from env.Persistence import Persistence


def main(argv):
    vendor = 'TDA'
    ifile = 'files/transactions.csv'
    act = 'cash'
    try:
        opts, args = getopt.getopt(argv, "hr:f:a:", [])
    except getopt.GetoptError:
        print('batch.py -r <vendor> -f <inputfile> -a <account nickname>')
        sys.exit(2)
    for opt, arg in opts:
        print("Option: ", opt, ' ', arg)
        if opt == '-h':
            print('batch.py -r <vendor> -f <inputfile>')
            sys.exit()
        elif opt == '-r':
            vendor = arg
        elif opt == '-f':
            ifile = arg
        elif opt == '-a':
            act = arg
    load(vendor,act,ifile)

def load(v,a,f):
    if v and a and f:
        conf = configparser.RawConfigParser()
        conf.read('tradalis.conf')
        conf.remove_option("Application", "class")
        if not Persistence.P:
            p = Persistence.startup(conf)
        else:
            p = Persistence.P
        Vendor.loadVendors()
        Vendor.getVendor(v).fromFile(a, f)
        p.shutdown()
    else:
        print('Error: too few arguments')
        print('Usage:    batch.py -r <vendor> -f <inputfile> -a <account nickname>')
        print('Supply all 3 arguments')
        sys.exit(3)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        load('TDA', 'cash', 'files/transactions.csv')

