# Generated by Django 3.1.7 on 2021-03-07 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_capitales_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('topico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.topicos')),
            ],
        ),
        migrations.CreateModel(
            name='data_Temperatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promedio', models.FloatField()),
                ('anio', models.IntegerField()),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.capitales')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paises')),
            ],
        ),
        migrations.CreateModel(
            name='data_Deforestacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('umbral', models.IntegerField()),
                ('anio', models.IntegerField()),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.capitales')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paises')),
            ],
        ),
        migrations.CreateModel(
            name='data_CO2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('anio', models.IntegerField()),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paises')),
            ],
        ),
    ]
