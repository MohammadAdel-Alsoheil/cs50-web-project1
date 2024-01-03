from django.shortcuts import render
from django import http
from django.http import HttpResponse
from . import util
import markdown
import random
from django import forms
import os



class md_form_title(forms.Form):
    title = forms.CharField(label="Enter the entry's title:")


        
def convert_to_html(title):
    entry = util.get_entry(title)
    converter = markdown.Markdown()

    if entry==None:
        return None
   
    return converter.convert(entry)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def get_title(request, TITLE, isSearch=False):
        
    entry = convert_to_html(TITLE)
    

    if entry==None:
       
       if isSearch:
           return None
       
       return render(request, "encyclopedia/Entry_not_found.html",{
           "title":TITLE
       })
    
    return render(request, "encyclopedia/title.html",{
        "title": TITLE,
        "content": entry
    })


def search_results(request):
    
    if request.method == "POST":
        query = request.POST.get('q') 


        page = get_title(request, query,True)

        if page==None:
            all_entries =  util.list_entries()
            result = []
            for name in all_entries:
               if str(query.lower()) in name.lower():
                   result.append(name)
            
            if len(result)==0:
                return render(request, "encyclopedia/None.html")

            return render(request, "encyclopedia/possible_Pages.html",{
                "entries":result
            })



        else:
            return page
        

def add_page(request):

    if request.method == "POST":
        
        form = md_form_title(request.POST)

        if form.is_valid():
            entry = form.cleaned_data["title"]
            text = request.POST.get("markdown")

            if entry in util.list_entries():
                return render(request, "encyclopedia/Save_error.html",{
                    "entry":entry
                })
            
            util.save_entry(entry,text)

            return get_title(request,entry)


    return render(request, "encyclopedia/Add.html",{
        "form": md_form_title()
    } )



def edit_page(request,entry):

    if request.method=="POST":
        text = request.POST.get("markdown")

        util.save_entry(entry,text)

        return get_title(request,entry)

    content = util.get_entry(entry)

    if content==None:
        return render(request, "encyclopedia/Entry_not_found.html",{
            "title":entry
        })
    

    return render(request, "encyclopedia/Edit.html",{
        "entry":entry,
        "content": content
    })


def randomize(request):

    entries = util.list_entries()

    randomIndex = random.randint(0,len(entries)-1)

    return render(request, "encyclopedia/title.html",{
        "title": entries[randomIndex],
        "content": convert_to_html(entries[randomIndex])
    })





