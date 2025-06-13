from django.utils.deprecation import MiddlewareMixin

class LogUserIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return

        # Get IP Address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Check and update if changed
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.last_login_ip != ip:
            profile.last_login_ip = ip
            profile.save()
