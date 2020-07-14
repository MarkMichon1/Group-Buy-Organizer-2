from general.models import Instance


def view_count_middleware(get_response):
    try:
        instance = Instance.objects.get(pk=1)
    except:
        instance = Instance()
        instance.save()

    def middleware(request):
        instance = Instance.objects.get(pk=1)
        instance.new_page_view()

        response = get_response(request)

        return response

    return middleware