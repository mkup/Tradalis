import pytest
from apps.grouping import TradeGroup
from apps.proposal import Proposal

@pytest.fixture
def env():
    import configparser
    from env.Env import Env
    conf = configparser.RawConfigParser()
    conf.read('../tradalis.conf')
    conf.remove_option("Application", "class")
    return Env(conf)

def test_groupSingles(env):
    g = TradeGroup('ira')
    g.groupSingles()
    print()
    for p in Proposal.Props:
        print(p)
        print()
    print("Count ", str(len(Proposal.Props)))

def test_proposal(env):
    g = TradeGroup('ira')
    g.groupSingles()
    p = Proposal.Props[0]
    print(repr(p))
    p.accept()
    env.getP().commit()

def test_groupSymbol(env):
    g = TradeGroup('ira')
    sym = 'ADSK'
    tup = g.groupSymbol(sym, None, None)
    trades = tup[0]
    transactions = tup[1]
    for tr in trades:
        print('------------')
        print(tr)
        for t in tr.tranCol:
            print(t)
    print('--Unattached Transactions--')
    for t in transactions:
        print(t)

def test_batch(env):
#    import batch
    import sys
    act = 'ira'
    sym = 'adsk'
    if not (act and sym):
        print('Error: account or symbol is not specified')
        print('Usage:    batch.py -a <account nickname> -o symbol -s <symbol>')
        sys.exit(3)
    g = TradeGroup(act)
    tup = g.groupSymbol(sym, None, None)
    trades = tup[0]
    transactions = tup[1]
    for tr in trades:
        print('------------')
        print(tr)
        for t in tr.tranCol:
            print(t)
    print('--Unattached Transactions--')
    for t in transactions:
        print(t)

    print('-- Propose groupping --')
#        ch = input('trade <trade ID> add <comma separated list of transactions>  OR  stop \n')
    ch = 'trade 74 add 246'
    if ch =='stop':
        print('Process Stopped')
#        break
    w = ch.split()
    if not (w[0] == 'trade' and w[2] == 'add'):
        print('Incorrect instructions')
    else:
        trade = next((tr for tr in trades if tr.id == int(w[1])), None)
        if not trade:
            print('Trade is not found: ' + w[1])
#            continue
        lst = w[3].split(',')
        trans = []
        for i in lst:
            t = next((r for r in transactions if r.id == int(i)), None)
            if t:
                trans.append(t)
            else:
                print('Transaction is not found: ' + i)
                trans = []
        if trans:
            Proposal(trade, trans).accept()
            print('---- Accepted ----')
            print(trade)
            for t in trans:
                print(t)
