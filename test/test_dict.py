import pytest
from coreapp.dict import Dict

@pytest.fixture
def env():
    import configparser
    from env.Env import Env
    conf = configparser.RawConfigParser()
    conf.read('../tradalis.conf')
    conf.remove_option("Application", "class")
    return Env(conf)

def test_dic(env):
    print(Dict.getAll())
    s = Dict('Strategy')
    s.cde = 'IOW'
    s.description = 'Short term In/Out vertical spread'
    print(s.__dict__)
    print(Dict.getAll())

    s = Dict('Strategy')
    s.cde = 'EARN'
    s.description = 'Simple, near-term earnings play'
    print(s.__dict__)
    print(Dict.getAll())

