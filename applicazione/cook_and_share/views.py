from django.http import HttpResponse
from django.template import loader
import logging

logger = logging.getLogger(__name__)

def load_page(request):
    template = loader.get_template("index.html")
    context = {
        "logged": True,
        "homepage": "home",
        "profile_pic_setted": False,
        "profile_pic_path": "",
    }
    
    return HttpResponse(template.render(context, request))