from django import forms
from .models import StudyRecord


class StudyRecordForm(forms.ModelForm):
    """学習記録のフォーム"""
    
    class Meta:
        model = StudyRecord
        fields = ['date', 'title', 'hours', 'content']  # ← hours
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：Django学習'
            }),
            'hours': forms.NumberInput(attrs={  # ← hours に修正！
                'class': 'form-control',
                'min': '0',
                'step': '0.1',  # ← 0.1刻みに変更（DecimalFieldに合わせる）
                'placeholder': '例：3.5'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '学習内容を入力してください'
            }),
        }
        labels = {
            'date': '学習日',
            'title': 'タイトル',
            'hours': '学習時間（時間）',  # ← hours に修正！
            'content': '学習内容',
        }