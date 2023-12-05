# Generated by Django 4.0.1 on 2022-01-18 18:43

import apostas.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import partidas.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cambio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moeda_origem', models.CharField(max_length=100)),
                ('moeda_destino', models.CharField(max_length=100)),
                ('taxa_cambio', models.DecimalField(decimal_places=10, max_digits=16)),
                ('taxa_rasbet', models.DecimalField(decimal_places=10, max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='Carteira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo_euro', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('saldo_dolar', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('saldo_dogecoin', models.DecimalField(decimal_places=10, default=0, max_digits=16)),
                ('saldo_bitcoin', models.DecimalField(decimal_places=10, default=0, max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='PartidaFormula1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('commence_time', models.DateTimeField()),
                ('estado', models.CharField(choices=[('A', 'active'), ('F', 'finished')], default='A', max_length=255)),
            ],
            bases=(models.Model, partidas.models.Partida),
        ),
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('morada', models.CharField(max_length=255)),
                ('codigoPostal', models.CharField(max_length=20)),
                ('nacionalidade', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('carteira', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apostas.carteira')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, partidas.models.Observer),
        ),
        migrations.CreateModel(
            name='Piloto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('position', models.IntegerField()),
                ('odds', models.DecimalField(decimal_places=2, default=1.1, max_digits=6)),
                ('partida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.partidaformula1')),
            ],
        ),
        migrations.CreateModel(
            name='PartidaFutebol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('commence_time', models.DateTimeField()),
                ('equipa_casa', models.CharField(max_length=255)),
                ('equipa_visitante', models.CharField(max_length=255)),
                ('odds_casa', models.DecimalField(decimal_places=2, max_digits=6)),
                ('odds_visitante', models.DecimalField(decimal_places=2, max_digits=6)),
                ('odds_empate', models.DecimalField(decimal_places=2, default=1.1, max_digits=6)),
                ('estado', models.CharField(choices=[('A', 'active'), ('F', 'finished')], default='A', max_length=255)),
                ('observadores', models.ManyToManyField(related_name='partidas_apostadas', to='apostas.Utilizador')),
            ],
            options={
                'unique_together': {('equipa_casa', 'commence_time')},
            },
            bases=(models.Model, partidas.models.Partida),
        ),
        migrations.AddField(
            model_name='partidaformula1',
            name='observadores',
            field=models.ManyToManyField(related_name='partidasFormula_apostadas', to='apostas.Utilizador'),
        ),
        migrations.CreateModel(
            name='CartaoBancario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('ccv', models.IntegerField()),
                ('expiracao', models.CharField(max_length=10)),
                ('nome', models.CharField(max_length=255)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='BoletimProfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moeda', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=10, default=0, max_digits=16)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='BoletimCusto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moeda', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=10, default=0, max_digits=16)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='ApostaFutebol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moeda', models.CharField(choices=[('E', 'Euro'), ('$', 'Dolar'), ('D', 'Dogecoin'), ('B', 'Bitcoin')], default='Euro', max_length=100)),
                ('valor', models.DecimalField(decimal_places=10, max_digits=16)),
                ('resultadoApostado', models.CharField(choices=[('E', 'empate'), ('C', 'casa'), ('V', 'visitante')], max_length=100)),
                ('estado', models.CharField(choices=[('A', 'active'), ('W', 'win'), ('L', 'lose'), ('S', 'suspended'), ('B', 'boletim')], default='A', max_length=20)),
                ('partida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.partidafutebol')),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.utilizador')),
            ],
            bases=(models.Model, apostas.models.Aposta),
        ),
        migrations.CreateModel(
            name='ApostaFormula1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moeda', models.CharField(choices=[('E', 'Euro'), ('$', 'Dolar'), ('D', 'Dogecoin'), ('B', 'Bitcoin')], default='Euro', max_length=100)),
                ('estado', models.CharField(choices=[('A', 'active'), ('W', 'win'), ('L', 'lose'), ('S', 'suspended'), ('B', 'boletim')], default='A', max_length=20)),
                ('valor', models.DecimalField(decimal_places=10, max_digits=16)),
                ('partida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.partidaformula1')),
                ('pilotoApostado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.piloto')),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apostas.utilizador')),
            ],
            bases=(models.Model, apostas.models.Aposta),
        ),
    ]