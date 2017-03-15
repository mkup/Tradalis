from dbTable import DB_table

class Trade(DB_table):

    def defineNames(self):
        self.tname = "Trade"
        ar = ['id', 'date', 'vendorId', 'description', 'quantity', 'symbol', 'price', 'commision', 'netCash',
                      'instrument', 'expiration', 'strike', 'trade', 'account']
        for i in range(len(ar)):
            self.dic[i] = [ar[i],'']

    def __init__(self):
        self.id = 0
        self.acct = ''          # account nick (for now)
        self.posCache = []      # List of transaction IDs for tracking transactio list changes
        self.posCol = []       # Collection of transactions - this has utility usage only
        self.description = ''
        self.symbol = ''        # Derived from positions
        self.strategy = ''
        self.spread = None
        self.long_short = ''    # ('LONG', 'SHORT') - derived from positions
        self.open_closed = 'PLAN'   #('OPEN', 'CLOSED', 'PLAN')
        self.verdict = ''       # notes on trade outcome
        self.outcome = ''       # Formal outcome for analysis
        self.dt_open = None     # Derived from positions
        self.dt_close = None    # Derived from positions
        self.risk = 0.0         # trade initial exposure, derived from positions
        self.net = 0.0          # Derived from positions
