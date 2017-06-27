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
        p.trade.calculateSpread()
        print(p.trade)
        for t in p.trans:
            print(t)
        print()
    print("Count ", str(len(Proposal.Props)))

def test_proposal(env):
    g = TradeGroup('ira')
    g.groupSingles()
    p = Proposal.Props[0]
    print(repr(p))
    p.accept()
    env.getP().commit()

def test_batchGroup(env):
    import batch
    batch.group('ira')
