# Generated by Django 2.0.7 on 2018-07-13 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_book_publication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrower_type', models.CharField(choices=[('S', 'Student'), ('T', 'Teacher')], max_length=1)),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('issue_count', models.IntegerField()),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='IssueSlip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True)),
                ('actual_return_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='books',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='books',
        ),
        migrations.AddField(
            model_name='book',
            name='is_available',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.AddField(
            model_name='issueslip',
            name='book_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Book'),
        ),
        migrations.AddField(
            model_name='issueslip',
            name='borrower_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Borrower'),
        ),
    ]
