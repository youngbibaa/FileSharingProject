from django.contrib.auth.forms import UserCreationForm, UserChangeForm  # type: ignore
from .models import CustomUser, Comment, Review, File
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )


class FileCreationForm(forms.ModelForm):
    class Meta:
        model = File
        fields = (
            "title",
            "description",
            "file",
            "category",
        )


class FileChangeForm(forms.Form):
    class Meta:
        model = File
        fields = (
            "title",
            "description",
            "file",
            "category",
        )


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            "text",
        )
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40})  # Можно настроить размер textarea
        }


class CommentChangeForm(forms.Form):
    class Meta:
        model = Comment
        fields = ("text",)


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "rating",
            "text",
        )


class ReviewChangeForm(forms.Form):
    class Meta:
        model = Review
        fields = (
            "rating",
        )
