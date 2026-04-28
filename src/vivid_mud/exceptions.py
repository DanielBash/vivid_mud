class VividError(Exception):
    pass

class AppError(VividError):
    pass

class ServerMissing(AppError):
    pass

class ClientMissing(AppError):
    pass