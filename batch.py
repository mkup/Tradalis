import sys, getopt
import configparser
from coreapp.vendors import Vendor
from env.Persistence import Persistence


def main(argv):
    vendor = 'TDA'
    ifile = 'files/transactions.csv'
    act = 'ira'
    op = 'group'
    sym = ''
    try:
        opts, args = getopt.getopt(argv, "hr:f:a:o:s:", [])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        print("Option: ", opt, ' ', arg)
        if opt == '-h':
            help()
            sys.exit()
        elif opt == '-r':
            vendor = arg
        elif opt == '-f':
            ifile = arg
        elif opt == '-a':
            act = arg
        elif opt == '-o':
            op = arg
        elif opt == '-s':
            sym = arg
    if op == 'group':
        group(act)
    elif op == 'load':
        load(vendor,act,ifile)
    elif op == 'symbol':
        symbol(act, sym)
    else:
        print('Unknown operation - ' + op)
        sys.exit(1)


def help():
    print('batch.py -a <account nickname> -r <vendor> -f <inputfile> or')
    print('batch.py -a <account nickname> -o <operation>')
    print('batch.py -a <account nickname> -o symbol -s <symbol>')


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


def group(act):
    """ Propose trades for unattached transactions """
    if not act:
        print('Error: account is not specified')
        print('Usage:    batch.py -a <account nickname> -o group')
        sys.exit(3)
    e = env()
    from apps.grouping import TradeGroup
    from apps.proposal import Proposal
    g = TradeGroup(act)
    g.groupSingles()
    a = 0
    r = 0
    print('Grouping unattached transactions for account - ' + act)
    for p in Proposal.Props:
        p.trade.calculateSpread()
        print(p.trade)
        for t in p.trans:
            print(t)
        again = True
        while(again):
            ch = input('a - accept; r - skip; or stop : ')
            again = False
            if ch == 'a':
                p.accept()
                e.persistence.commit()
                a += 1
            elif ch == 'r':
                p.reject
                e.persistence.abort()
                r += 1
            elif ch =='stop':
                e.persistence.abort()
                print('Process stopped')
                print('Accepted: ' + str(a) + '   Rejected: ' + str(r))
                sys.exit(0)
            else:
                print('Wrong input')
                again = True
    print('Accepted: ' + str(a) + '   Rejected: ' + str(r))

def symbol(act, sym):
    """ Propose trades for unattached transactions """
    if not (act and sym):
        print('Error: account or symbol is not specified')
        print('Usage:    batch.py -a <account nickname> -o symbol -s <symbol>')
        sys.exit(3)
    e = env()
    from apps.grouping import TradeGroup
    from apps.proposal import Proposal
    g = TradeGroup(act)
    tup = g.groupSymbol(sym, None, None)
    trades = tup[0]
    transactions = tup[1]
    for tr in trades:
        print('------------')
        print(tr)
        for t in tr.transCol:
            print(t)
    print{'-- Unattached --'}
    for t in transactions:
        print(t)

    print('-- Propose groupping --')
    while():
        ch = input('trade <trade ID> add <comma separated list of transactions>  OR  stop')
        if ch =='stop':
            print('Process Stopped')
            break
        w = ch.split()
        if not (w[0] == 'trade' and w[2] == 'add'):
            print('Incorrect instructions')
        else:
            trade = next([tr for tr in trades if tr.id == int(w[1])], None)
            if not trade:
                print('Trade is not found: ' + w[1])
                continue
            lst = w[3].split(',')
            trans = []
            for i in lst:
                t = next([r for r in transactions if r.id == int(i)], None)
                if t:
                    trans.append(t)
                else:
                    print('Transaction is not found: ' + i)
                    trans = []
            if trans:
                #Proposal(trade, trans).accept()
                print('---- Accepted ----')
                print(trade)
                for t in trans:
                    print(t)


def env():
    import configparser
    from env.Env import Env
    conf = configparser.RawConfigParser()
    conf.read('tradalis.conf')
    conf.remove_option("Application", "class")
    return Env(conf)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        load('TDA', 'cash', 'files/transactions.csv')

