from django import forms
from .models import Certification, StudyRecord


class CertificationForm(forms.ModelForm):
    """学習項目作成・編集フォーム"""
    
    class Meta:
        model = Certification
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: RUNTEQ、基本情報技術者試験'
            })
        }
        labels = {
            'name': '学習項目名'
        }


class StudyRecordForm(forms.ModelForm):
    """学習記録作成・編集フォーム"""
    
    class Meta:
        model = StudyRecord
        fields = ['certification', 'date', 'hours', 'description']
        widgets = {
            'certification': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.25',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '今日学習した内容を記録しましょう'
            })
        }
        labels = {
            'certification': '学習項目',
            'date': '学習日',
            'hours': '学習時間（時間）',
            'description': '学習内容'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # ログインユーザーの学習項目のみを選択肢として表示
        if user:
            self.fields['certification'].queryset = Certification.objects.filter(user=user)