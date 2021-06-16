from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, ListView
from django.urls import reverse

from . import models
from scraper.scraper import QuoraScraper

import datetime
import time
import ast

scraper = QuoraScraper()

class SearchQueryView(View):
    template_name = "scraper/search_query.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        query = request.POST["query"]
        n_questions = request.POST["numberOfQuestions"]
        if query and n_questions:
            scraper.start_driver()

            username = "noumanmufc11@gmail.com"
            password = "Arbisoft1!"

            scraper.set_credentials(username, password)
            scraper.login()

            time.sleep(5)
            scraper.search_for_query(query)

            time.sleep(10)
            scraper.get_questions(int(n_questions))

            data_scrape = models.DataScrape()
            data_scrape.query = query
            data_scrape.scrape_date = datetime.date.today()

            data_scrape.save()

            if len(scraper.questions):
                return render(request, 
                              self.template_name, 
                              context={"questions": scraper.questions, "data_scrape_id": data_scrape.id})


class DataScrapeDetailView(View):
    model = models.DataScrape
    template_name = 'scraper/questions_stats.html'

    def get(self, request, *args, **kwargs):
        data_scrape_id = kwargs['data_scrape_id']
        response_questions = self.get_response_questions(data_scrape_id)

        return render(request, self.template_name, context={'questions': response_questions})
    
    def get_response_questions(self, data_scrape_id):
        response_questions = []
        data_scrape = models.DataScrape.objects.filter(id=data_scrape_id).first()
        questions = data_scrape.questions.all()
        for index, question in enumerate(questions):
            response_question = {
                'text': question.question_text,
                'link': question.question_link,
                'name': f'question_{index+1}',
                'answers': []
            }
            
            answers = models.Answer.objects.filter(
                question__id=question.id)
            
            for answer in answers:
                response_question['answers'].append({
                    'upvoters': answer.upvoters,
                    'views': answer.views,
                    'username': answer.username,
                    'date': answer.answer_date
                })

            response_questions.append(response_question)
        return response_questions


class QuestionStatsView(View):
    template_name = "scraper/questions_stats.html"

    def post(self, request):
        question_keys = list(request.POST.keys())[1:]
        print(request.POST.keys())
        data_scrape_id = request.POST['data_scrape_id']
        data_scrape = models.DataScrape.objects.get(id=data_scrape_id)
        for key in question_keys:
            if key not in ['data_scrape_id']:
                question = request.POST[key]
                print(question)
                question_json = ast.literal_eval(question)

                question_object = models.Question(
                    question_text=question_json['text'],
                    question_link=question_json['link'])
                question_object.save()

                answers = scraper.scrape_question_details(question_json, 3)

                data_scrape.questions.add(question_object)

                for answer in answers:
                    answer_object = models.Answer(username=answer['username'],
                                                  views=answer['views'],
                                                  upvoters=answer['upvoters'],
                                                  answer_date=answer['date'])
                    answer_object.question = question_object
                    answer_object.save()

        scraper.close_driver()

        if len(scraper.answers):
            return HttpResponseRedirect(reverse("scraper:data_scrape", args=(data_scrape.id, )))


class DataScrapesListView(ListView):
    model = models.DataScrape
    template_name = 'scraper/data_scrapes.html'
    context_object_name = 'data_scrapes'

class DataScrapeDeleteView(View):
    def post(self, request):
        scrape_queries = list(request.POST.keys())[1:]
        print(scrape_queries)
        for query in scrape_queries:
            scrape_id = request.POST[query]
            models.DataScrape.objects.get(id=scrape_id).delete()

        return HttpResponseRedirect(
            reverse("scraper:data_scrapes"))
