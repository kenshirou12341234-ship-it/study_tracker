from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, render  # ← render を追加
from django.urls import reverse_lazy
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import StudyRecord
from .forms import StudyRecordForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class RecordListView(LoginRequiredMixin, ListView):
    """学習記録一覧（自分の記録だけ表示）"""
    model = StudyRecord
    template_name = 'records/list.html'
    context_object_name = 'records'
    
    def get_queryset(self):
        """自分の記録だけを取得"""
        return StudyRecord.objects.filter(user=self.request.user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 自分の記録だけを集計（get_queryset()を再利用）
        user_records = self.get_queryset()
        
        # 総学習時間
        total_hours = user_records.aggregate(Sum('hours'))['hours__sum'] or 0
        context['total_hours'] = total_hours
        
        # 今週の学習時間
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_hours = user_records.filter(
            date__gte=week_start
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        context['week_hours'] = week_hours
        
        # 今月の学習時間
        month_start = today.replace(day=1)
        month_hours = user_records.filter(
            date__gte=month_start
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        context['month_hours'] = month_hours
        
        # レコード数
        context['record_count'] = user_records.count()
        
        return context


class RecordDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """学習記録詳細（自分の記録だけアクセス可能）"""
    model = StudyRecord
    template_name = 'records/detail.html'
    context_object_name = 'record'
    
    def test_func(self):
        """自分の記録かどうかをチェック"""
        record = self.get_object()
        return record.user == self.request.user
    
    def handle_no_permission(self):
        """権限がない場合の処理"""
        messages.error(self.request, 'この記録にアクセスする権限がありません。')
        return redirect('records:list')


class RecordCreateView(LoginRequiredMixin, CreateView):
    """学習記録新規作成"""
    model = StudyRecord
    form_class = StudyRecordForm
    template_name = 'records/form.html'
    success_url = reverse_lazy('records:list')
    
    def form_valid(self, form):
        """保存前にユーザーを紐づける"""
        form.instance.user = self.request.user
        messages.success(self.request, '学習記録を作成しました。')
        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """学習記録編集（自分の記録だけ編集可能）"""
    model = StudyRecord
    form_class = StudyRecordForm
    template_name = 'records/form.html'
    
    def test_func(self):
        """自分の記録かどうかをチェック"""
        record = self.get_object()
        return record.user == self.request.user
    
    def handle_no_permission(self):
        """権限がない場合の処理"""
        messages.error(self.request, 'この記録を編集する権限がありません。')
        return redirect('records:list')
    
    def get_success_url(self):
        """編集後は詳細ページに戻る"""
        messages.success(self.request, '学習記録を更新しました。')
        return reverse_lazy('records:detail', kwargs={'pk': self.object.pk})


class RecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """学習記録削除（自分の記録だけ削除可能）"""
    model = StudyRecord
    template_name = 'records/delete.html'
    success_url = reverse_lazy('records:list')
    
    def test_func(self):
        """自分の記録かどうかをチェック"""
        record = self.get_object()
        return record.user == self.request.user
    
    def handle_no_permission(self):
        """権限がない場合の処理"""
        messages.error(self.request, 'この記録を削除する権限がありません。')
        return redirect('records:list')
    
    def delete(self, request, *args, **kwargs):
        """削除時にメッセージを表示"""
        messages.success(self.request, '学習記録を削除しました。')
        return super().delete(request, *args, **kwargs)


# ↓ ここから register 関数（クラスの外に配置）
def register(request):
    """新規登録ビュー"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後に自動ログイン
            messages.success(request, 'アカウントを作成しました。')
            return redirect('records:list')  # 学習記録一覧へリダイレクト
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})