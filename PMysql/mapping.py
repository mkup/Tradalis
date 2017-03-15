# todo: code and reorganize marshaling-unmarshaling for Trades and Dictionaries
# todo: fromTransaction

from coreapp.positions import Position, Option
from coreapp.trade import Trade

class Map(object):

    @staticmethod
    def marshall(obj):
        if isinstance(obj,Position):
            return Map.toTransaction(obj)
        elif isinstance(obj,Option):
            return Map.toOption(obj)
        elif isinstance(obj,Trade):
            return Map.toTrade(obj)

    @staticmethod
    def marshallTrade(tr):
        """convert Trade to DB_trade"""
        return 0

    @staticmethod
    def marshallTransaction(tr):
        """convert Position to DB_transaction"""
        return 0

    @staticmethod
    def marshallOption(op):
        """convert Option to DB_transaction"""
        return 0

    def unmarshallTransaction(self, tran):
        """" Translate DB_transaction record to either Position or Option object"""

        return 0

    @staticmethod
    def unmarshallTrade(tr):
        """" Translate DB_trade record to Trade object """
        return 0
