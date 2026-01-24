


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_uid', models.CharField(max_length=16, unique=True)),
                ('full_name', models.CharField(max_length=120)),
                ('class_grade', models.CharField(max_length=20)),
                ('email_enc', models.BinaryField()),
                ('mobile_enc', models.BinaryField()),
                ('email_hash', models.CharField(max_length=64, unique=True)),
                ('mobile_hash', models.CharField(max_length=64, unique=True)),
                ('last_login_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
