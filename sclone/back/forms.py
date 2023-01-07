from django import forms
from .models import Images,Profile,Likepost

class ImageForm(forms.ModelForm):
    class Meta:
        
        model = Images
        fields = ('file',)

class liker(forms.ModelForm):
    class Meta:
        
        model = Likepost
        fields = ('postid','username',)
