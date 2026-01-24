from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="email_hash",
            field=models.CharField(max_length=64, unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="mobile_hash",
            field=models.CharField(max_length=64, unique=True, db_index=True),
        ),
    ]
