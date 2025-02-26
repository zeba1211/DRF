from rest_framework.throttling import UserRateThrottle

class empRateThrottle(UserRateThrottle):
    scope='emp'