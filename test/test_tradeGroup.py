import pytest
from apps.grouping import TradeGroup

@pytest.fixture
def env():
    import configparser
    from env.Env import Env
    conf = configparser.RawConfigParser()
    conf.read('../tradalis.conf')
    conf.remove_option("Application", "class")
    return Env(conf)

def test_groupSingles(env):
    g = TradeGroup('cash')
    g.groupSingles()
    print()
    for p in g.props:
        p.trade.calculateSpread()
        print(p.trade)
        for t in p.trans:
            print(t)
        print()
    assert 0
