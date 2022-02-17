import requests
from requests.compat import quote_plus
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
BASE_CRIAGSLIST_URL = 'https://hyderabad.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request,'base.html')
def new_search(request):
    search= request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_CRIAGSLIST_URL.format(quote_plus(search))
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features="html.parser")
    post_listings = soup.find_all('li',{'class':'result-row'})
    final_postings=[]
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-date'):
            post_date= post.find(class_='result-date').text
        else:
            post_date= 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url='https://www.improvutopia.com/wp-content/uploads/2016/02/empty.png.jpeg'


        final_postings.append((post_title,post_url,post_date,post_image_url))




    frontend={ 'search':search,
               'final_postings':final_postings,

    }
    return render(request,'my_app/new_search.html',frontend)
