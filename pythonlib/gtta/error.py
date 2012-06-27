# -*- coding: utf-8 -*-

class GTTAError(Exception):
    pass

class NotEnoughArguments(GTTAError):
    pass

class InvalidTargetFile(GTTAError):
    pass

class InvalidTarget(GTTAError):
    pass

class NoHostName(GTTAError):
    pass

class TaskTimeout(GTTAError):
    pass

class NoDataReturned(GTTAError):
    pass

class NoRecipient(GTTAError):
    pass

class NoAuth(GTTAError):
    pass

class InvalidAuth(GTTAError):
    pass

class NoMailServer(GTTAError):
    pass
