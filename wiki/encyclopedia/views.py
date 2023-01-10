from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django import forms

from . import util

import markdown


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Page Title")
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))


class NewEntryBodyForm(forms.Form):
    create_form = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):

    # TODO: If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
    
    html = markdown.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry_page.html", {"entry_html": html})

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "")
    if query in entries:
        html = markdown.markdown(util.get_entry(query))
        return render(request, "encyclopedia/entry_page.html", {"entry_html": html})
    else:
        possible_entries = []
        for entry in entries:
            if query.lower() in entry.lower():
                possible_entries.append(entry)
        if len(possible_entries) != 0:
            return render(request, "encyclopedia/search.html", {"possible_entries": possible_entries})
        else:
            return HttpResponse("Page not found.")


def create_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["title"] not in util.list_entries():
                new_title = form.cleaned_data["title"]
                new_body = form.cleaned_data["body"]
                util.save_entry(new_title,new_body)
                messages.success(request, 'New entry successfully admitted into the wikipedia.')
            else:
                messages.error(request, 'This entry already exists in the wikipedia. Admittion failed.')
                return render(request, "encyclopedia/create_entry.html", {"form": form})
        else:
            messages.error(request, 'Admission failed.')
            return render(request, "encyclopedia/create_entry.html", {"form": form})
    return render(request, "encyclopedia/create_entry.html", {"form": NewEntryForm()})

        

    
