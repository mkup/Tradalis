from unittest import TestCase

import pytest
from coreapp.trade import Trade, Spread
import datetime


@pytest.fixture
def persist():
    import configparser
    from env.Persistence import Persistence
    conf = configparser.RawConfigParser()
    conf.read('../tradalis.conf')
    conf.remove_option("Application", "class")
    return Persistence.startup(conf)

@pytest.fixture
def env():
    import configparser
    from env.Env import Env
    conf = configparser.RawConfigParser()
    conf.read('../tradalis.conf')
    conf.remove_option("Application", "class")
    return Env(conf)


def test_insertTrade(persist):
    tr = Trade()
    tr.account = 'cash'
    tr.symbol = 'AAPL'
    tr.dateOpen = datetime.date.today()
    tr.spread = Spread()
    i = persist.retriever.insertTrade(tr)
    print("inserted " + str(i))
    persist.connection.commit()
    assert (i)


def test_updateTrade(env):
    col = env.getP().retriever.getTrades('cash')
    tr = col[0]
    tr.dateClose = datetime.date(2017,5,30)
    env.getP().changes['trade']['u'].append(tr)
    env.getP().commit()
