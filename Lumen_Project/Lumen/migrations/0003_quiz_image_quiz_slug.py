from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Lumen', '0002_quizresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='quiz_covers/'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]