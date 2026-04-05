from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Certification, StudyRecord
from .forms import CertificationForm, StudyRecordForm


@login_required
def dashboard(request):
    """ダッシュボード表示"""
    
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    
    # ログインユーザーの学習記録のみを取得
    user_records = StudyRecord.objects.filter(user=request.user)
    
    # 集計
    total_hours = user_records.aggregate(Sum('hours'))['hours__sum'] or 0
    weekly_hours = user_records.filter(
        date__gte=start_of_week
    ).aggregate(Sum('hours'))['hours__sum'] or 0
    monthly_hours = user_records.filter(
        date__gte=start_of_month
    ).aggregate(Sum('hours'))['hours__sum'] or 0
    
    # 最近の学習記録
    recent_records = user_records[:5]
    
    # 学習項目別の集計
    cert_stats = []
    for cert in Certification.objects.filter(user=request.user):
        hours = user_records.filter(certification=cert).aggregate(Sum('hours'))['hours__sum'] or 0
        cert_stats.append({
            'name': cert.name,
            'hours': hours
        })
    
    context = {
        'total_hours': total_hours,
        'weekly_hours': weekly_hours,
        'monthly_hours': monthly_hours,
        'recent_records': recent_records,
        'cert_stats': cert_stats,
    }
    
    return render(request, 'records/dashboard.html', context)


@login_required
def record_list(request):
    """学習記録一覧"""
    records = StudyRecord.objects.filter(user=request.user)
    return render(request, 'records/record_list.html', {'records': records})


@login_required
def record_create(request):
    """学習記録作成"""
    if request.method == 'POST':
        form = StudyRecordForm(request.POST, user=request.user)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, '学習記録を作成しました！')
            return redirect('records:dashboard')
    else:
        form = StudyRecordForm(user=request.user)
    
    return render(request, 'records/record_form.html', {'form': form, 'title': '学習記録を作成'})


@login_required
def record_update(request, pk):
    """学習記録編集"""
    record = get_object_or_404(StudyRecord, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = StudyRecordForm(request.POST, instance=record, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '学習記録を更新しました！')
            return redirect('records:dashboard')
    else:
        form = StudyRecordForm(instance=record, user=request.user)
    
    return render(request, 'records/record_form.html', {'form': form, 'title': '学習記録を編集'})


@login_required
def record_delete(request, pk):
    """学習記録削除"""
    record = get_object_or_404(StudyRecord, pk=pk, user=request.user)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, '学習記録を削除しました！')
        return redirect('records:dashboard')
    
    return render(request, 'records/record_confirm_delete.html', {'record': record})


# ========== 学習項目管理 ==========

@login_required
def certification_list(request):
    """学習項目一覧"""
    certifications = Certification.objects.filter(
        user=request.user
    ).annotate(
        total_hours=Sum('study_records__hours')
    ).order_by('name')
    
    return render(request, 'records/certification_list.html', {
        'certifications': certifications
    })


@login_required
def certification_create(request):
    """学習項目作成"""
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = request.user
            certification.save()
            messages.success(request, f'学習項目「{certification.name}」を作成しました！')
            return redirect('records:certification_list')
    else:
        form = CertificationForm()
    
    return render(request, 'records/certification_form.html', {'form': form, 'title': '学習項目を作成'})


@login_required
def certification_update(request, pk):
    """学習項目編集"""
    certification = get_object_or_404(Certification, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, f'学習項目「{certification.name}」を更新しました！')
            return redirect('records:certification_list')
    else:
        form = CertificationForm(instance=certification)
    
    return render(request, 'records/certification_form.html', {'form': form, 'title': '学習項目を編集'})


@login_required
def certification_delete(request, pk):
    """学習項目削除"""
    certification = get_object_or_404(Certification, pk=pk, user=request.user)
    
    if request.method == 'POST':
        certification.delete()
        messages.success(request, f'学習項目「{certification.name}」を削除しました！')
        return redirect('records:certification_list')
    
    return render(request, 'records/certification_confirm_delete.html', {'certification': certification})


# ========== ユーザー登録 ==========

class RegisterView(CreateView):
    """ユーザー登録"""
    form_class = UserCreationForm
    template_name = 'records/register.html'
    success_url = reverse_lazy('login')