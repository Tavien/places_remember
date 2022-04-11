def get_avatar(backend, response, user=None, *args, **kwargs):
    """
    Pipeline to get profile photo link
    """
    url = response.get('photo', '')

    if url:
        user.photo = url
        user.save()
