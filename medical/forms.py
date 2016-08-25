# -*- coding: UTF-8 -*-

# Copyright (c) 2014-2016 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

from django import forms
from django.utils.translation import ugettext_lazy as _

from ajax_select.fields import AutoCompleteSelectMultipleField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from .models import Patient, Problem, Staff, History, Test


class PatientForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Basic data'),
                'first_name',
                'last_name',
                'last_name_optional',
                'gender',
                'doctor_assigned',
                'race',
                'birth_date',
                'birth_place',
                'decease_date',
            ),
            Fieldset(
                _('Administrative data'),
                'address',
                'phone_contact',
                'tin',
                'ssn',
                'health_card_number',
                'insurance_company',
            ),
            Fieldset(
                _('Extra data'),
                'family_situation',
                'labour_situation',
                'education',
            ),
            FormActions(
                Submit('save', _('Save'), css_class='btn-lg'),
            ),
        )
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['doctor_assigned'].queryset = Staff.doctors.all()

    class Meta:
        model = Patient
        exclude = ('relatives',)
        widgets = {
            'address': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
            'phone_contact': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
            'family_situation': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
            'labour_situation': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
            'education': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class PatientSearchForm(forms.Form):
    required_css_class = 'required'

    search_type = forms.ChoiceField(
        label=_('Field'),
        required=True,
        choices=(
            ('last_name', _('Last name')),
            ('first_name', _('First name')),
            ('last_name_optional', _('Last name optional')),
            ('address', _('Address')),
            ('phone_contact', _('Phone contact')),
            ('race', _('Race')),
            ('birth_date', _('Birth date')),
            ('birth_place', _('Birth place')),
            ('decease_date', _('Decease date')),
            ('tin', _('Taxpayer Identification Number (TIN)')),
            ('ssn', _('Social Security Number (SSN)')),
            ('health_card_number', _('Health card number')),
            ('insurance_company', _('Insurance company')),
            # TODO ('collegiate_number', _('Collegiate number')),
        ),
        initial='last_name'
    )

    search_text = forms.CharField(
        label=_('Value'),
        required=False,
        help_text=_('(empty = see all results)')
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PatientSearchForm, self).__init__(*args, **kwargs)
        self.fields['search_type'].initial = self.request.GET.get(
            'search_type',
            'last_name'
        )
        self.fields['search_text'].initial = self.request.GET.get(
            'search_text',
            ''
        )


class PatientSearchByMedicalProblemForm(forms.Form):
    required_css_class = 'required'

    search_type_problem = forms.ChoiceField(
        label=_('Field'),
        required=True,
        choices=(
            ('wording', _('Wording')),
            ('subjetive', _('Subjetive')),
            ('objetive', _('Objetive')),
            ('appreciation', _('Appreciation')),
            ('action_plan', _('Action Plan')),
            ('prescription', _('Prescription'))
        ),
        initial='wording'
    )

    search_text_problem = forms.CharField(
        label=_('Value'),
        required=False,
        help_text=_('(empty = see all results)')
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PatientSearchByMedicalProblemForm, self).__init__(*args, **kwargs)
        self.fields['search_type_problem'].initial = self.request.GET.get(
            'search_type_problem', 'wording'
        )
        self.fields['search_text_problem'].initial = self.request.GET.get(
            'search_text_problem', ''
        )


class ProblemForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    closed = forms.BooleanField(label=_('Closed problem?'), required=False)

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.fields['order_number'].widget.attrs['readonly'] = True
        if self.instance:
            self.fields['closed'].initial = self.instance.closing_date

    class Meta:
        model = Problem
        fields = (
            'order_number', 'doctor', 'wording',
            'meeting_place', 'subjetive', 'objetive', 'appreciation',
            'action_plan', 'prescription', 'closed', 'patient'
        )
        widgets = {
            'patient': forms.HiddenInput(),
        }


class HistoryAntecedentsForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Personal antecedents'),
                'medical_intolerance', 'birth_growth', 'growth_sexuality',
                'feed', 'habits', 'peristaltic_conditions', 'psychological',
                'children_complaint', 'venereal_disease',
                'accident_surgical_operation', 'mental_illness', 'patient',
            ),
            Fieldset(
                _('Family antecedents'),
                'parents_status_health', 'brothers_status_health',
                'spouse_childs_status_health', 'family_illness',
            ),
            FormActions(
                Submit('save', _('Save'), css_class='btn-lg'),
            ),
        )
        super(HistoryAntecedentsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = History
        fields = '__all__'
        widgets = {
            'patient': forms.HiddenInput(),
        }


class PatientRelativesForm(forms.ModelForm):
    relatives = AutoCompleteSelectMultipleField(
        channel='patients',
        required=False,
        help_text='',
        show_help_text=False,
        label=''
    )

    class Meta:
        model = Patient
        fields = ('relatives',)


class ProblemConnectionsForm(forms.ModelForm):
    connections = AutoCompleteSelectMultipleField(
        channel='problems',
        required=False,
        help_text='',
        show_help_text=False,
        label=''
    )

    class Meta:
        model = Problem
        fields = ('connections',)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('document', 'document_type', 'problem')
        widgets = {
            'problem': forms.HiddenInput(),
        }
