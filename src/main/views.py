from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    messages.info(request, 'This is an info message.')
    messages.success(request, 'This is a success message.')
    messages.warning(request, 'This is a warning message.')
    messages.error(request, 'This is an error message.')
    return render_to_response('main/index.html',
                              RequestContext(request))