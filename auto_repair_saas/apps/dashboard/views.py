from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from auto_repair_saas.apps.jobs.models import Job
from auto_repair_saas.apps.staff.models import Staff


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        return render(request, self.template_name)


class DashboardDataView(LoginRequiredMixin, View):
    @staticmethod
    def _compute_dashboard_data(period_range):
        dashboard_data = dict()
        all_jobs = Job.objects.all()
        period_range_jobs = all_jobs.filter(
            created_on__gte=period_range[0], created_on__lte=period_range[1]
        )

        sales = all_jobs.filter(
            paid=True,
            payment_registered_on__gte=period_range[0],
            payment_registered_on__lte=period_range[1]
        )

        top_earners = Staff.objects.filter(
            job__paid=True,
            job__payment_registered_on__gte=period_range[0],
            job__payment_registered_on__lte=period_range[1]
        ).order_by('-job__charged').values('job__charged', 'name')[:3]

        pending_estimates = period_range_jobs.filter(status='pending')
        confirmed_estimates = period_range_jobs.filter(status='confirmed')
        jobs_in_progress = period_range_jobs.filter(status='in_progress')
        jobs_done = period_range_jobs.filter(status='done')

        overall_job_charges = list()
        cash_job_charges = list()
        card_job_charges = list()
        mpesa_job_charges = list()
        chart_dates = list()

        for day in range(0, (period_range[1].day - period_range[0].day) + 1):
            _date = period_range[0] + timedelta(day)

            chart_dates.append(_date.date())
            overall_job_charges.append(sales.filter(
                payment_registered_on=_date
            ).aggregate(Sum('charged')).get('charged__sum') or 0)
            cash_job_charges.append(sales.filter(
                payment_registered_on=_date, payment_method='cash'
            ).aggregate(Sum('charged')).get('charged__sum') or 0)
            card_job_charges.append(sales.filter(
                payment_registered_on=_date, payment_method='card'
            ).aggregate(Sum('charged')).get('charged__sum') or 0)
            mpesa_job_charges.append(sales.filter(
                payment_registered_on=_date, payment_method='mpesa'
            ).aggregate(Sum('charged')).get('charged__sum') or 0)

        dashboard_data['sales'] = sum(overall_job_charges)
        dashboard_data['chart_dates'] = chart_dates
        dashboard_data['overall_job_charges'] = overall_job_charges
        dashboard_data['cash_job_charges'] = cash_job_charges
        dashboard_data['card_job_charges'] = card_job_charges
        dashboard_data['mpesa_job_charges'] = mpesa_job_charges
        dashboard_data['pending_estimates_count'] = pending_estimates.count()
        dashboard_data[
            'pending_estimates_charged'] = pending_estimates.aggregate(
            Sum('charged')).get('charged__sum') or 0
        dashboard_data[
            'confirmed_estimates_count'] = confirmed_estimates.count()
        dashboard_data[
            'confirmed_estimates_charged'] = confirmed_estimates.aggregate(
            Sum('charged')).get('charged__sum') or 0
        dashboard_data['in_progress_jobs_count'] = jobs_in_progress.count()
        dashboard_data[
            'in_progress_jobs_charged'] = jobs_in_progress.aggregate(
            Sum('charged')).get('charged__sum') or 0
        dashboard_data[
            'done_jobs_count'] = jobs_done.count()
        dashboard_data[
            'done_jobs_charged'] = jobs_done.aggregate(
            Sum('charged')).get('charged__sum') or 0
        dashboard_data['top_earners'] = list(top_earners)

        return dashboard_data

    def get(self, request):
        period = request.GET.get('period', default='week')
        now = timezone.now().replace(hour=23, minute=59)
        period_range_ceil = now

        if period == 'month':
            period_range_floor = now - timedelta(30)
        elif period == 'year':
            period_range_floor = now - timedelta(364)
        else:
            period_range_floor = now - timedelta(6)

        period_range = (
            period_range_floor.replace(hour=0, minute=0), period_range_ceil
        )

        data = self._compute_dashboard_data(period_range)
        return JsonResponse(data)
