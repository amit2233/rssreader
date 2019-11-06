import feedparser
import requests
import datetime
from django.utils import timezone
from django.shortcuts import render

from.models import Source, Post  

# Create your views here.

def home(request):
    return render(request, 'template/home.html')


def fix_relative(html, url):

    """ this is fucking cheesy """
    
    
    try:
        base = "/".join(url.split("/")[:3])

        html = html.replace("src='//", "src='http://")
        html = html.replace('src="//', 'src="http://')


        html = html.replace("src='/", "src='%s/" % base)
        html = html.replace('src="/', 'src="%s/' % base)
    
    except Exception as ex:
        pass    

    return html


def rss_feeds(request):
    url = request.POST['url']
    try:
        feed_url = Source.objects.get(feed_url=url)
        posts = Post.objects.filter(source=feed_url).order_by('created')
        return render(request, 'template/home.html', context={'posts': posts})
    except Source.DoesNotExist:
        ret = requests.get(url, allow_redirects=False, timeout=20)
        content = feedparser.parse(ret.content)
        source = Source(feed_url=url)

        try:
            source.etag = ret.headers["etag"]
        except Exception as ex:
            source.etag = None                                   
        
        try:
            sourhttps://zeenews.india.com/rss/india-national-news.xmlce.last_modified = ret.headers["Last-Modified"]
        except Exception as ex:
            source.last_modified = None                                   

        try:
            source.name = content.feed.title
        except Exception as ex:
            pass

        try:
            source.site_url = content.feed.link
        except Exception as ex:
            pass
    
        source.save()    
        entries = content['entries']

        for e inhttps://zeenews.india.com/rss/india-national-news.xml entries:
            body = ""

            if hasattr(e, "summary"):
                if len(e.summary) > len(body):
                    body = e.summary
            
            if hasattr(e, "summary_detail"):
                if len(e.summary_detail.value) > len(body):
                    body = e.summary_detail.value        

            if hasattr(e, "description"):
                if len(e.description) > len(body):
                    body = e.description

            body = fix_relative(body, source.site_url)

            try:
                created  = datetime.datetime.fromtimestamp(time.mktime(e.published_parsed)).replace(tzinfo=timezone.utc)

            except Exception as ex:
                created  = timezone.now()
    
            try:
                title = e.title
            except Exception as ex:
                title = ""
                            
            try:
                link = e.link
            except Exception as ex:
                link = ''

            try:
                guid = e.guid
            except:
                try:
                    guid = e.link
                except:
                    guid = ""
            post = Post.objects.create(source=source, title=title, link=link,
            guid=guid, body=body, created=created)

        posts = Post.objects.filter(source=source).order_by('created')
        return render(request, 'template/home.html', context={'posts': posts})

