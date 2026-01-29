from django import forms

CLASS_CHOICES = [
    ("6", "Class 6"),
    ("7", "Class 7"),
    ("8", "Class 8"),
    ("9", "Class 9"),
    ("10", "Class 10"),
    ("11", "Class 11"),
    ("12", "Class 12"),
]


class StudentRegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Full Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Student Email (will be encrypted)"}),
        label="Student Email"
    )
    parent_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Parent/Guardian Full Name"}),
        label="Parent Name"
    )
    parent_email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Parent Email (for login & notifications)"}),
        label="Parent Email",
        required=True
    )
    mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Mobile Number"})
    )
    class_grade = forms.ChoiceField(
        choices=CLASS_CHOICES,
        widget=forms.Select(attrs={"class": "form-input"})
    )

    def clean_mobile(self):
        m = self.cleaned_data["mobile"].strip()
        if not m.isdigit() or len(m) < 10:
            raise forms.ValidationError("Enter a valid mobile number.")
        return m


class StudentEditForm(forms.Form):
    full_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    class_grade = forms.ChoiceField(
        choices=CLASS_CHOICES,
        widget=forms.Select(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-input"})
    )

    def clean_mobile(self):
        m = self.cleaned_data["mobile"].strip()
        if not m.isdigit() or len(m) < 10:
            raise forms.ValidationError("Enter a valid mobile number.")
        return m
