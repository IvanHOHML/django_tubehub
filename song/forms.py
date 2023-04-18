from .models import Playlist
from django.forms import ModelForm, CharField, TextInput

class PlaylistForm(ModelForm):
    url = CharField(
        required=True,
        widget=TextInput(
            attrs={
                "placeholder":"https://www.youtube.com/watch?v=Gjcz2BOaWXo&list=PLicBGo8PsMeROVj8Wk9TJbv9eTUc-5iiW",
                "class": "textarea is-success is-medium"
            },
        ),
        label = "",
    )
    class Meta:
        model = Playlist
        fields = ["url"]