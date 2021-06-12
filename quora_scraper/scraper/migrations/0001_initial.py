# Generated by Django 3.0.8 on 2021-06-12 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(blank=True)),
                ('question_link', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataScrape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField(blank=True, null=True)),
                ('scrape_date', models.DateField(blank=True, null=True)),
                ('questions', models.ManyToManyField(null=True, to='scraper.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('upvoters', models.IntegerField()),
                ('views', models.IntegerField()),
                ('answer_date', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='scraper.Question')),
            ],
        ),
    ]
