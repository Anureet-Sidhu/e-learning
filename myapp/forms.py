from django import forms
from myapp.models import Order, Student


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = {'student', 'course', 'levels', 'order_date'}
        widgets = {
            'student': forms.RadioSelect(attrs={'class': 'radio'}),
            'order_date': forms.SelectDateWidget(attrs={'class': 'years=date.today()'})
        }
        labels = {
            'student': "Student Name",
            'order_date': "Order Date"
        }

class InterestForm(forms.Form):
    CHOICES = [(1, 'Yes'), (2, 'No')]
    interested = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=CHOICES)
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Additional Comments')

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = {'username', 'password', 'first_name', 'last_name', 'city', 'interested_in'}
        widgets = {
            'city': forms.RadioSelect(attrs={'class': 'radio'}),
            'password': forms.PasswordInput
        }
        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'interested_in': "Interested In"
        }
