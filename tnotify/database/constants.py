__all__ = (
    'DEFAULT_USER_PERMISSIONS',
    'DEFAULT_ADMIN_PERMISSIONS',
    'DEFAULT_MASTER_PERMISSIONS',
)


DEFAULT_USER_PERMISSIONS = [
    'GetNotifyExceptions',
    'GetNotifyInfo',
]

DEFAULT_ADMIN_PERMISSIONS = [
    *DEFAULT_USER_PERMISSIONS,

    'AddUser',
    'RemoveUser',
    'AdminPanel',
    'ChangeUserPermissions'
]

DEFAULT_MASTER_PERMISSIONS = [
    *DEFAULT_ADMIN_PERMISSIONS,

    'AddAdmin',
    'RemoveAdmin',
]
