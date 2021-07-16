from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
import random

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Title"}),
        max_length=100, 
        required=True
    )
    
    text = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={"placeholder": "Your text"}), 
        required=True
    )


def redirect_view(request):
    return index(request)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request, entry):
    if entry not in util.list_entries():
        raise Http404("Page does not exist")
    else:
        html = Markdown().convert(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "text": html,
        })


def search(request):

    if request.method == "POST":
        query = request.POST["q"]
        results = []

        for entry in util.list_entries():
            if query.lower() == entry.lower():
                return get_entry(request, entry)
            elif query.lower() in entry.lower():
                results.append(entry)   

        return render(request, "encyclopedia/search.html", {
            "results": results
        })
        
    else:
        return render(request, "encyclopedia/search.html", {})


def random_entry(request):

    entries = util.list_entries()
    r = random.randint(0, len(entries)-1)
    return HttpResponseRedirect(reverse("encyclopedia:get_entry", args=(entries[r],)))
    


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
           
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/new_entry.html", {})
                else:
                    util.save_entry(title, text)
                    return HttpResponseRedirect(reverse("encyclopedia:get_entry", args=(title,)))
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form": NewEntryForm()
        })


def edit(request, entry):

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("encyclopedia:get_entry", args=(title,)))
    else:
        form = NewEntryForm({
            "title": entry,
            "text": util.get_entry(entry)
        })
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": entry,
        })
        