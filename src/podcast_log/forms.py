from django import forms


class AddPodcastForm(forms.Form):
    url = forms.CharField(label="RSS Feed URL")
