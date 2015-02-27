class UnauthorizedException(Exception):
    pass


class BadRequestException(Exception):
    pass


class NotFoundException(Exception):
    pass


class RedirectException(Exception):
    pass


class ServerErrorException(Exception):
    pass


class UnexpectedException(Exception):
    pass


class LocationHeaderNotFoundException(Exception):
    pass