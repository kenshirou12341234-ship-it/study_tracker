from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Certification(models.Model):
    """学習項目マスタ（資格、学習内容など）"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='certifications',
        verbose_name='ユーザー'
    )
    name = models.CharField(max_length=100, verbose_name='学習項目名')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    class Meta:
        verbose_name = '学習項目'
        verbose_name_plural = '学習項目'
        ordering = ['name']


class StudyRecord(models.Model):
    """学習記録"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='study_records',
        verbose_name='ユーザー'
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name='study_records',
        verbose_name='学習項目',
        null=True,
        blank=True
    )
    date = models.DateField(verbose_name='学習日')
    hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='学習時間'
    )
    description = models.TextField(
        blank=True,
        verbose_name='学習内容'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        cert_name = self.certification.name if self.certification else '未分類'
        return f"{self.user.username} - {cert_name} - {self.date} ({self.hours}時間)"
    
    class Meta:
        verbose_name = '学習記録'
        verbose_name_plural = '学習記録'
        ordering = ['-date']