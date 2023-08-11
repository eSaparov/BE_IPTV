from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import videos
import re
from django.db.models import Q
from django.core.files.images import get_image_dimensions
from .forms import FilterOrderForm

class LoginInterfaceView(LoginView):
    template_name = 'registration/login.html'
    success_url = ""

class LogoutInterfaceView(LogoutView):
    template_name = 'registration/logout.html'

def index(request):
    return render(request, "index.html")

class VideosListView(LoginRequiredMixin, ListView):
    model = videos
    context_object_name = "video_list"
    template_name = "forms/video_list.html"
    login_url = "/login"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FilterOrderForm()
        context['filter_Disabled'] = self.request.GET.get('filter_Disabled')
        context['filter_Featured'] = self.request.GET.get('filter_Featured')
        context['ordering'] = self.request.GET.get('orderby')
        return context

    def get_queryset(self):
        filter_Disabled = self.request.GET.get('filter_Disabled')
        filter_Featured = self.request.GET.get('filter_Featured')
        ordering = self.request.GET.get('ordering', 'name')

        if filter_Featured == 'on' and filter_Disabled == 'on':
            new_context = videos.objects.filter(disabled=True).filter(isFeatured=True).order_by(ordering)
        elif filter_Disabled == 'on':
            new_context = videos.objects.filter(disabled=True).order_by(ordering)
        elif filter_Featured == 'on':
            new_context = videos.objects.filter(isFeatured=True).order_by(ordering)
        else:
            new_context = videos.objects.order_by(ordering)



        return new_context


class VideoDetailView(LoginRequiredMixin, DetailView):
    model = videos
    context_object_name = "video_detail"
    template_name = "forms/video_detail.html"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        w, h = get_image_dimensions(self.object.iconFile)
        if w != 400:
            k = 400 / w
            w = w * k
            h = h * k
        if h != 400:
            k = 400 / h
            w = w * k
            h = h * k

        context["width"] = w
        context["height"] = h

        return context
    
    def get_queryset(self):
        queryset = videos.objects.all()
        return queryset
    



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_video(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(
            query_string, ['name', 'shortName', 'description'])
        video_list = videos.objects.filter(entry_query)

    return render(request, 'forms/video_list.html', locals())
