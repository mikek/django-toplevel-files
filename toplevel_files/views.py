from django.http import Http404, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.views.static import serve as django_serve
from django.conf import settings

from .models import TopLevelFile


@require_http_methods(['GET', 'HEAD'])
def serve(request, filename, simple_404=True, **kwargs):
    """
    Serves requested TopLevelFile.

    Checks if requested filename matches existing TopLevelFile object and
    returns 'django.views.static.serve' passing it all unhandled keyword
    arguments. 'filename' keyword argument is required and should be normally
    captured with urlconf. Passing 'simple_404=False' allows to render usual
    404 page with 'handler404'.

    """
    try:
        TopLevelFile.objects.only('id').get(type__file_name=filename)
    except TopLevelFile.DoesNotExist:
        if simple_404:
            return HttpResponseNotFound('file not found')
        else:
            raise Http404

    return django_serve(request, filename, document_root=settings.MEDIA_ROOT,
                        **kwargs)
