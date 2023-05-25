# Generated by Django 4.1.7 on 2023-04-05 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_remove_solutions_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutions',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='upvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_at', models.DateTimeField(auto_now_add=True)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.solutions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]