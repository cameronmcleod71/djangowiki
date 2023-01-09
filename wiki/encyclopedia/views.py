from django.shortcuts import render

from . import util

import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):

    # TODO: If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
    
    html = markdown.markdown(util.get_entry(title))
    
    return render(request, "encyclopedia/entry_page.html", {"entry_html": html})
