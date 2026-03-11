from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model 

User = get_user_model()  


class StudyRecord(models.Model):
    """学習記録モデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField('タイトル', max_length=200)
    content = models.TextField('学習内容')
    hours = models.DecimalField('学習時間（時間）', max_digits=4, decimal_places=1)
    date = models.DateField('学習日', default=timezone.now)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '学習記録'
        verbose_name_plural = '学習記録'
        ordering = ['-date', '-created_at']  # 新しい順に表示

    def __str__(self):
        return f"{self.date} - {self.title}"