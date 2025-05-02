def profile_sidebar(request):
    if request.user.is_authenticated:
        return {
            'user_profile': request.user.profile
        }
    return {}