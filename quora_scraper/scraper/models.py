from django.db import models


class Question(models.Model):
    question_text = models.TextField(blank=True)
    question_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question_text


class DataScrape(models.Model):
    questions = models.ManyToManyField(Question, null=True)
    query = models.TextField(blank=True, null=True)
    scrape_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.query}'


class Answer(models.Model):
    username = models.TextField()
    upvoters = models.TextField()
    views = models.TextField()
    answer_date = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.username
