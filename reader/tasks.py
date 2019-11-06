from celery import shared_task
import feedparser
import requests
import datetime
from django.utils import timezone
from .models import Source, Post
from .views import fix_relative

@shared_task
def update_rss_feed():
    sources = Source.objects.all()
    for source_feed in sources:
        headers = {} 

        if source_feed.etag:
            headers["If-None-Match"] = str(source_feed.etag)
        if source_feed.last_modified:
            headers["If-Modified-Since"] = str(source_feed.last_modified)
        
        ret = requests.get(source_feed.feed_url, headers=headers, allow_redirects=False, timeout=20)
        content = feedparser.parse(ret.content)
 
        try:
            source_feed.etag = ret.headers["etag"]
        except Exception as ex:
            source_feed.etag = None                                   
        try:
            source_feed.last_modified = ret.headers["Last-Modified"]
        except Exception as ex:
            source_feed.last_modified = None

        try:
            source_feed.name = content.feed.title
        except Exception as ex:
            pass

        try:
            source_feed.site_url = content.feed.link
        except Exception as ex:
            pass
    
        source_feed.save()    
        entries = content['entries']

        for e in entries:

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

            body = fix_relative(body, source_feed.site_url)

            try:
                guid = e.guid
            except:
                try:
                    guid = e.link
                except:
                    guid = ""

            try:
                p  = Post.objects.filter(source=source_feed).filter(guid=guid)[0]
            except:
                p = Post(body=" ", source=source_feed )    

            p.body = body
            
            try:
                p.created  = datetime.datetime.fromtimestamp(time.mktime(e.published_parsed)).replace(tzinfo=timezone.utc)
            except Exception as ex:
                p.created  = timezone.now()

            try:
                p.title = e.title
            except Exception as ex:
                pass
                            
            try:
                p.link = e.link
            except Exception as ex:
                pass
    
            p.save()  