from django.shortcuts import redirect, reverse


def for_not_authorized(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect(reverse('towns:index'))
        date = func(request, *args, **kwargs)
        return date
    return wrap
