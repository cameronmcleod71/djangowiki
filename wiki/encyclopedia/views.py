from django.shortcuts import render

from . import util

import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    name = title + '.md'
    # remember to make a case for when this file doesnt exist
    with open(name, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    
    return render(request, "encyclopedia/entry_page.html", {"entry_html": html})
