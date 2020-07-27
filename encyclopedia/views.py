from django.shortcuts import render, HttpResponse
from django import forms
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util
import logging
import os
import random as rn


logger = logging.getLogger('mylogger')
#Specify styling to django forms
#Method 1
class EntrySearch(models.Model):
    entry_name = models.CharField(max_length=10)

class NewEntry(models.Model):
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=100)

class EntryTitle(forms.Form):
    title = forms.CharField(label="")

#Method 2
#Create a Form based on model
class EntrySearchForm(forms.ModelForm):
    class Meta:
        model = EntrySearch
        fields=['entry_name']
        widgets = {
            'entry_name': forms.TextInput(attrs={ 'class':'search'}),
        }
        labels = {
            'entry_name': "Search here"
        }
class NewEntryForm(forms.ModelForm):
    class Meta:
        model = NewEntry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'id':'titleInput',
                                            'placeholder':"Entry title"}),
            'content': forms.Textarea(attrs={'class':'form-control',
                                             'id':'entryContentText',
                                             'rows':'4',
                                             'placeholder':"Entry content"})
        }
        #<input type="text" class="form-control" id="titleInput" placeholder="New entry title " >
        #<textarea class="form-control" id="exampleFormControlTextarea1" rows="4" placeholder="New entry content">

def index(request):
    if request.method == 'GET':
        search_form = EntrySearchForm(request.GET)
        if search_form.is_valid():
            entry_string = search_form.cleaned_data["entry_name"]
            logger.info('Requesting entry: ' + entry_string)
            entry_content = util.get_entry(entry_string)
            if entry_content is not None:
                my_dic = {"title": entry_string,
                    "content": markdown2.markdown(entry_content)}
                return render(request, "encyclopedia/wiki.html", my_dic)
            else:
                results = util.find_partial_match(entry_string)
                return render(request,"encyclopedia/search_results.html", {
                    "results": results
                })
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form" : EntrySearchForm()
        })
    else:
        logger.info("Just loading the page")
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form" : EntrySearchForm()
        })

def wiki_ini(request):
    logger.info('wiki_ini')
    if request.method == 'GET':
        if 'title' in request.GET:
            title = request.GET['title']
            content = request.GET['content']
            util.save_entry(title, content)
            logger.info('title:' + title )
            logger.info('content:' + content )
            return render(request, "encyclopedia/wiki.html", {
                'title':title,
                'content': markdown2.markdown(content)
            })
        else:
            return render (request, "encyclopedia/wiki.html", {
                "title":"default"})

def wiki(request, title):
    entry_con = util.get_entry(title)
    if entry_con is not None:
        content = entry_con if entry_con is not None else "Entry not found"
        my_dic = {"title": title,
                    "content": markdown2.markdown(content)}
        return render(request, "encyclopedia/wiki.html",my_dic)
    else:
        return render(request,"encyclopedia/notfound.html")


def newpage(request):
    # res = os.listdir(os.path.join(os.getcwd(),'entries'))
    if request.method == 'GET':
        return render(request,"encyclopedia/newpage.html",{
            "new_entry_form":NewEntryForm()
    })
    else:
        new_entry_form = NewEntryForm(request.POST)
        if new_entry_form.is_valid():
            if util.get_entry(new_entry_form['title'].value()) is None:
                title = new_entry_form['title'].value()
                content = new_entry_form['content'].value()
                util.save_entry(title, content)
                my_dic = {"title": title,
                        "content": markdown2.markdown(content)}
                return render(request, "encyclopedia/wiki.html", my_dic)
            else:
                return render(request, "encyclopedia/error.html")
        else:
            return render(request,"encyclopedia/newpage.html",{
                    "new_entry_form":NewEntryForm()})

def edit_entry(request):
    new_entry_form = EntryTitle(request.GET)
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_entry.html",{
                'title': title,
                'content': content
            })
    else:
        return render(request, "encyclopedia/error.html")

def random(request):
    entries = util.list_entries()
    random_entry = entries[rn.randint(0, len(entries)-1)]
    content = util.get_entry(random_entry)
    return render(request, "encyclopedia/wiki.html", {
        'title':random_entry,
        'content': markdown2.markdown(content)
    })
    # return HttpResponseRedirect(reverse("encyclopedia:index"))

        
 

