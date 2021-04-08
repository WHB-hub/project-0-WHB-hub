from markdown2 import Markdown
from django import forms
from django.shortcuts import render, redirect
from re import search

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': 'textarea'}))


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Page Title'}))
    body = forms.CharField(widget=forms.Textarea)




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


# Get and return the desired wiki entry
def wiki(request, title):  
    # Get the entry from the url
    entry = util.get_entry(title)

    # Check if the entry exists
    if not entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": "ERROR: Requested File Not Found",
            "title": "ERROR"
        })

    # Convert the markdown entry to html
    markdowner = Markdown()
    html = markdowner.convert(entry)

    # Else return the requested page
    return render(request, "encyclopedia/entry.html", {
        "entry": html,
        "title": title
    })


def search(request):    
    if request.method == "POST":
        form = SearchForm(request.POST)  # Load form data
        if form.is_valid():
            q = form.cleaned_data["q"]  # Get search query
            entry = util.get_entry(q)  # Check for an exact match to the search query
            
            if not entry:  # If no match, find all entries that are close
                entries = util.list_entries()
                search_results = []
                for entry in entries:  # Search through all entries for the substring
                    if q.lower() in entry.lower():
                        search_results.append(entry)
                return render(request, "encyclopedia/search.html", {  # Return search page with results listed
                    "form": SearchForm(),
                    "q": q,
                    "entries": search_results
                })
            return redirect(f"wiki/{q}")
    
    return render(request, "encyclopedia/search.html", {
        "form": SearchForm()
    })