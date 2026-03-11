from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import StudyRecord

class RecordListView(ListView):
    """学習記録一覧"""
    model = StudyRecord
    template_name = 'records/list.html'
    context_object_name = 'records'
    ordering = ['-date']  # 新しい順に表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 総学習時間
        total_hours = StudyRecord.objects.aggregate(Sum('hours'))['hours__sum'] or 0
        context['total_hours'] = total_hours
        
        # 今週の学習時間
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())  # 今週の月曜日
        week_hours = StudyRecord.objects.filter(
            date__gte=week_start
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        context['week_hours'] = week_hours
        
        # 今月の学習時間
        month_start = today.replace(day=1)
        month_hours = StudyRecord.objects.filter(
            date__gte=month_start
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        context['month_hours'] = month_hours
        
        # レコード数
        context['record_count'] = StudyRecord.objects.count()
        
        return context

class RecordDetailView(DetailView):
    """学習記録詳細"""
    model = StudyRecord
    template_name = 'records/detail.html'
    context_object_name = 'record'

class RecordCreateView(CreateView):
    """学習記録新規作成"""
    model = StudyRecord
    template_name = 'records/form.html'
    fields = ['title', 'content', 'hours', 'date']
    success_url = reverse_lazy('records:list')

class RecordUpdateView(UpdateView):
    """学習記録編集"""
    model = StudyRecord
    template_name = 'records/form.html'
    fields = ['title', 'content', 'hours', 'date']
    success_url = reverse_lazy('records:list')

class RecordDeleteView(DeleteView):
    """学習記録削除"""
    model = StudyRecord
    template_name = 'records/delete.html'
    success_url = reverse_lazy('records:list')