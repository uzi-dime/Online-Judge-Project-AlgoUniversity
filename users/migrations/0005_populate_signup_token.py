import uuid
from django.db import migrations

def gen_signup_tokens(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for user in User.objects.all():
        user.signup_token = str(uuid.uuid4())
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_signup_token'),
    ]

    operations = [
        migrations.RunPython(gen_signup_tokens),
    ]
