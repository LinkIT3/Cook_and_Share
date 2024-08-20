
from math import fabs
from multiprocessing import context
from re import template
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from datetime import datetime
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