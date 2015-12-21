# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('collegiate_number', models.CharField(max_length=20, blank=True, null=True, verbose_name='collegiate number')),
                ('tin', models.CharField(max_length=20, blank=True, null=True, verbose_name='taxpayer Identification Number (TIN)')),
                ('last_name_optional', models.CharField(max_length=30, blank=True, null=True, verbose_name='last name optional')),
                ('address', models.TextField(blank=True, null=True, verbose_name='address')),
                ('phone_contact', models.TextField(blank=True, null=True, verbose_name='phone contact')),
                ('staff_type', models.CharField(default=b'A', max_length=1, choices=[(b'A', 'Administrative'), (b'D', 'Doctor')], verbose_name='staff type')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'staff',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birth_growth', models.TextField(null=True, blank=True, verbose_name='birth and growth')),
                ('growth_sexuality', models.TextField(null=True, blank=True, verbose_name='growth and sexuality')),
                ('feed', models.TextField(null=True, blank=True, verbose_name='feed')),
                ('habits', models.TextField(null=True, blank=True, verbose_name='habits')),
                ('peristaltic_conditions', models.TextField(null=True, blank=True, verbose_name='peristaltic conditions')),
                ('psychological_conditions', models.TextField(null=True, blank=True, verbose_name='psychological conditions')),
                ('children_complaint', models.TextField(null=True, blank=True, verbose_name='children complaint')),
                ('venereal_disease', models.TextField(null=True, blank=True, verbose_name='veneral disease')),
                ('accident_surgical_operation', models.TextField(null=True, blank=True, verbose_name='accidents and surgical operations')),
                ('medical_intolerance', models.TextField(null=True, blank=True, verbose_name='medical intolerance')),
                ('mental_illness', models.TextField(null=True, blank=True, verbose_name='mental illness')),
                ('parents_status_health', models.TextField(null=True, blank=True, verbose_name='parents status health')),
                ('brothers_status_health', models.TextField(null=True, blank=True, verbose_name='brothers status health')),
                ('spouse_childs_status_health', models.TextField(null=True, blank=True, verbose_name='spouse and childs status health')),
                ('family_illness', models.TextField(null=True, blank=True, verbose_name='family illness')),
            ],
            options={
                'db_table': 'history',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('last_name_optional', models.CharField(max_length=30, null=True, blank=True, verbose_name='last name optional')),
                ('address', models.TextField(null=True, blank=True, verbose_name='address')),
                ('phone_contact', models.TextField(null=True, blank=True, verbose_name='phone contact')),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', 'Male'), (b'F', 'Female')], verbose_name='gender')),
                ('race', models.CharField(max_length=30, null=True, blank=True, verbose_name='race')),
                ('birth_date', models.DateField(help_text='yyyy-mm-dd', null=True, blank=True, verbose_name='birth date')),
                ('birth_place', models.CharField(max_length=50, null=True, blank=True, verbose_name='birth place')),
                ('decease_date', models.DateField(help_text='yyyy-mm-dd', null=True, blank=True, verbose_name='decease date')),
                ('tin', models.CharField(max_length=20, null=True, verbose_name='taxpayer Identification Number (TIN)', blank=True)),
                ('ssn', models.CharField(max_length=30, null=True, verbose_name='social Security Number (SSN)', blank=True)),
                ('health_card_number', models.CharField(max_length=30, null=True, blank=True, verbose_name='health card number')),
                ('family_situation', models.TextField(null=True, blank=True, verbose_name='family situation')),
                ('labour_situation', models.TextField(null=True, blank=True, verbose_name='labour situation')),
                ('education', models.TextField(null=True, blank=True, verbose_name='education')),
                ('insurance_company', models.CharField(max_length=30, null=True, blank=True, verbose_name='insurance company')),
                ('relatives', models.ManyToManyField(related_name='_patient_relatives_+', to='medical.Patient', blank=True)),
                ('doctor_assigned', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='doctor allocated by quota', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'patient',
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order_number', models.PositiveSmallIntegerField(verbose_name='order number')),
                ('closing_date', models.DateField(null=True, editable=False, blank=True, verbose_name='closing date')),
                ('meeting_place', models.CharField(max_length=50, blank=True, null=True, verbose_name='meeting place')),
                ('wording', models.TextField(verbose_name='wording')),
                ('subjetive', models.TextField(null=True, blank=True, verbose_name='subjetive')),
                ('objetive', models.TextField(null=True, blank=True, verbose_name='objetive')),
                ('appreciation', models.TextField(null=True, blank=True, verbose_name='appreciation')),
                ('action_plan', models.TextField(null=True, blank=True, verbose_name='action plan')),
                ('prescription', models.TextField(null=True, blank=True, verbose_name="doctor's orders")),
                ('connections', models.ManyToManyField(related_name='_problem_connections_+', to='medical.Problem', blank=True)),
                ('patient', models.ForeignKey(to='medical.Patient')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='attending physician', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['order_number'],
                'db_table': 'problem',
                'verbose_name': 'Medical Problem',
                'verbose_name_plural': 'Medical Problems',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('document_type', models.CharField(max_length=128, null=True, blank=True, verbose_name='MIME type')),
                ('document', models.FileField(upload_to=b'medical_tests/%Y/%m/%d', verbose_name='document')),
                ('problem', models.ForeignKey(to='medical.Problem')),
            ],
        ),
        migrations.AddField(
            model_name='history',
            name='patient',
            field=models.OneToOneField(to='medical.Patient'),
        ),
    ]
