from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "bajada", "fase", "contenido", "imagen"]
        widgets = {
            "fase": forms.RadioSelect,
            "contenido": forms.Textarea(attrs={"rows": 14}),
            "titulo": forms.TextInput(attrs={"placeholder": "Un título para esta noche"}),
        }
