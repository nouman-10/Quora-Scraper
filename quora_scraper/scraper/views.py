from django.shortcuts import render
from django.views.generic import View


class SearchQueryView(View):
    template_name = "scraper/search_query.html"

    def get(self, request):
        return render(request, self.template_name)