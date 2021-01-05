from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
from .forms import inputanForm
from .models import PostModel
from elasticsearch import Elasticsearch
import pickle
import numpy as np
from datetime import datetime

with open('/home/nasri/ProjectKantor/pythonProject2/SentimentDjango/django_app/TugasAkhir/nb_pickle_pos','rb') as r:
    prob_pos = pickle.load(r)
with open('/home/nasri/ProjectKantor/pythonProject2/SentimentDjango/django_app/TugasAkhir/nb_pickle_neg','rb') as r:
    prob_neg = pickle.load(r)
with open('/home/nasri/ProjectKantor/pythonProject2/SentimentDjango/django_app/TugasAkhir/nb_pickle_neut','rb') as r:
    prob_neut = pickle.load(r)
with open('/home/nasri/ProjectKantor/pythonProject2/SentimentDjango/django_app/TugasAkhir/total_tfidf_pos','rb') as r:
    total_tfidf_pos = pickle.load(r)
with open('/home/nasri/ProjectKantor/pythonProject2/SentimentDjango/django_app/TugasAkhir/total_idf_pos','rb') as r:
    total_idf_pos = pickle.load(r)

def NB(sentence, prob_pos, prob_neg, prob_neut, total_tfidf, total_idf):
    nb_pos, nb_neg, nb_neut = 1, 1 ,1
    for i in sentence.split():
        if i in prob_pos:
            nb_pos *= prob_pos[i]
        else:
            nb_pos *= 1 / (total_tfidf + total_idf)
        if i in prob_neg:
            nb_neg *= prob_neg[i]
        else:
            nb_neg *= 1 / (total_tfidf + total_idf)
        if i in prob_neut:
            nb_neut *= prob_neut[i]
        else:
            nb_neut *= 1 / (total_tfidf + total_idf)
    return nb_pos, nb_neg, nb_neut


es = Elasticsearch('http://localhost:9200/')

def index(request):
    req = requests.get('http://localhost:8899/dashboard_covid')
    js = req.json()
    pie_covid = requests.get("http://localhost:8899/chart-prov-covid")
    js_pie = pie_covid.json()
    news = requests.get("http://localhost:8899/covid-news")
    news_cov = news.json()
    datas = js[0]['_source']
    context = {"name":"nasri Adzlani",
               "covid":datas,
               "pie":js_pie,
               "news":news_cov}
    return render(request, 'index.html', context)

@csrf_exempt
def inputan_sentimen(request):
    form = inputanForm()
    if request.method == 'POST':
        inp = request.POST['input']
        sent = NB(inp, prob_pos, prob_neg, prob_neut, total_tfidf_pos, total_idf_pos)
        res = np.argmax(sent)
        if (res == 0):
            sentiment = "positif"
        elif (res == 1):
            sentiment = "negatif"
        else:
            sentiment = "netral"
        print(inp)
        print(sentiment)
        dict = {"data":inp,
                "sentiment":sentiment,
                "date":datetime.now().timestamp()}
        print(dict)
        check = es.search(index='komen_sentimen',body={"query":{"match_phrase":{"data":inp}}})
        res = check['hits']['total']
        val = res['value']
        if (val < 1):
            elastic = es.index(index='komen_sentimen', body=dict, id=datetime.now().timestamp())
    req = requests.get('http://localhost:8899/table_sentiment')
    tb = req.json()

    context = {"form": form,
               "tb":tb}
    print(context)
    return render(request, 'inputan.html', context)

def map(request):
    map_req = requests.get('http://localhost:8899/trends')
    maps = map_req.json()

    return render(request, 'map.html',maps)

def sen_default(request):
    pos = requests.get('http://localhost:8899/covid_positive')
    positive = pos.json()
    neu = requests.get('http://localhost:8899/covid_neutral')
    neutral = neu.json()
    neg = requests.get('http://localhost:8899/covid_negatif')
    negative = neg.json()
    dics = {
        "name":"nasri Adzlani",
        "positif":positive,
        "netral":neutral,
        "negatif":negative
    }
    return render(request, 'sen_default.html', dics)

def login(request):
    if request.method=='GET':
        url = 'http://localhost:8899/get_account'
        response = requests.get(url)
        print(response.json())
        pass
    return render(request, 'login.html')

def register(request):
    hasil = Register(request.POST or None)
    if request.method == 'POST':
        datas = {"data":hasil.data}
        print(datas)
    
    return render(request, 'register.html')