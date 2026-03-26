class AccountException(Exception):
    pass


class AccountAlreadyExist(AccountException):
    pass

class UsernameAlreadyExist(AccountException):
    pass

class AccountNotFound(AccountException):
    pass


class AccountIsDeactivate(AccountException):
    pass


class InvalidPassword(AccountException):
    pass


class AccountHasNoId(AccountException):
    pass
