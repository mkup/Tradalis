import pytest
from coreapp.trade import Trade

@pytest.fixture
def env():
    import configparser
    from env.Env import Env
    conf = configparser.RawConfigParser()
    conf.read('../tradalis.conf')
    conf.remove_option("Application", "class")
    return Env(conf)

def test_construct(env):
#    trans = [t for t in env.getP().retriever.getUnattachedTransactions('cash') if t.symbol == 'ACAD']   # Sngle stock
    trans = [t for t in env.getP().retriever.getUnattachedTransactions('cash') if t.symbol == 'AAPL']   # Vert
    tr = Trade()
    tr.account = 'cash'
    tr.state = 'PLAN'
    tr.addTrans(trans)
    print(tr)

