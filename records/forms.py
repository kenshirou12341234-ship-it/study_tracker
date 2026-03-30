from django import forms
from .models import StudyRecord


class StudyRecordForm(forms.ModelForm):
    """学習記録のフォーム"""
    
    class Meta:
        model = StudyRecord
        fields = ['date', 'title', 'hours', 'content']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトルを入力（任意）'
            }),
            'hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.1',
                'placeholder': '例：3.5'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '学習内容を入力（任意）'
            }),
        }
        labels = {
            'date': '学習日',
            'title': 'タイトル',
            'hours': '学習時間（時間）',
            'content': '学習内容',
        }
    
    # ↓ ここから __init__ メソッド（Meta クラスの外に出す）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # title と content を任意項目にする
        self.fields['title'].required = False
        self.fields['content'].required = False