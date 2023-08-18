from django.contrib.auth.models import User


def app_base_context(request):
    """ Contexto para todos los templates con datos de esta aplicacion """

    ctx = {
        'all_users': User.objects.all(),
    }
    return ctx
