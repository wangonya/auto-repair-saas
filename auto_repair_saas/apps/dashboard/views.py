from datetime import timedelta

from dateutil import rrule
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
    def _get_sales_chart_data(period, period_range, sales):
        overall_job_charges = list()
        cash_job_charges = list()
        card_job_charges = list()
        mpesa_job_charges = list()
        chart_dates = list()

        if period == 'year':
            for day in rrule.rrule(
                    rrule.MONTHLY, dtstart=period_range[0],
                    until=period_range[1]
            ):
                day = day.date()
                chart_dates.append(day.strftime("%B-%Y"))
                overall_job_charges.append(sales.filter(
                    payment_registered_on__year=day.year,
                    payment_registered_on__month=day.month
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
                cash_job_charges.append(sales.filter(
                    payment_registered_on__year=day.year,
                    payment_registered_on__month=day.month,
                    payment_method='cash'
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
                card_job_charges.append(sales.filter(
                    payment_registered_on__year=day.year,
                    payment_registered_on__month=day.month,
                    payment_method='card'
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
                mpesa_job_charges.append(sales.filter(
                    payment_registered_on__year=day.year,
                    payment_registered_on__month=day.month,
                    payment_method='mpesa'
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
        else:
            for day in rrule.rrule(
                    rrule.DAILY, dtstart=period_range[0], until=period_range[1]
            ):
                day = day.date()
                chart_dates.append(day)
                overall_job_charges.append(sales.filter(
                    payment_registered_on=day
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
                cash_job_charges.append(sales.filter(
                    payment_registered_on=day, payment_method='cash'
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
                card_job_charges.append(sales.filter(
                    payment_registered_on=day, payment_method='card'
                ).aggregate(Sum('charged')).get('charged__sum') or 0)
                mpesa_job_charges.append(sales.filter(
                    payment_registered_on=day, payment_method='mpesa'
                ).aggregate(Sum('charged')).get('charged__sum') or 0)

        return (overall_job_charges, cash_job_charges, card_job_charges,
                mpesa_job_charges, chart_dates)

    def _compile_dashboard_data(self, period, period_range):
        dashboard_data = dict()
        all_jobs = Job.objects.all()
        period_range_jobs = all_jobs.filter(
            created_at__gte=period_range[0], created_at__lte=period_range[1]
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
        ).values('name').annotate(
            earnings=Sum('job__charged')
        ).order_by('-earnings')[:5]

        pending_estimates = period_range_jobs.filter(status='pending')
        confirmed_estimates = period_range_jobs.filter(status='confirmed')
        jobs_in_progress = period_range_jobs.filter(status='in_progress')
        jobs_done = period_range_jobs.filter(status='done')

        (overall_job_charges, cash_job_charges,
         card_job_charges, mpesa_job_charges,
         chart_dates) = self._get_sales_chart_data(period, period_range, sales)

        dashboard_data['sales'] = sum(overall_job_charges)
        dashboard_data['chart_dates'] = chart_dates
        dashboard_data['overall_job_charges'] = overall_job_charges
        dashboard_data['cash_job_charges'] = cash_job_charges
        dashboard_data['card_job_charges'] = card_job_charges
        dashboard_data['mpesa_job_charges'] = mpesa_job_charges
        dashboard_data['top_earners'] = list(top_earners)

        job_states = (
            (pending_estimates, 'pending_estimates'),
            (confirmed_estimates, 'confirmed_estimates'),
            (jobs_in_progress, 'jobs_in_progress'),
            (jobs_done, 'jobs_done')
        )
        for job_state in job_states:
            dashboard_data[f'{job_state[1]}_count'] = job_state[0].count()
            dashboard_data[f'{job_state[1]}_charged'] = job_state[0].aggregate(
                Sum('charged')).get('charged__sum') or 0

        return dashboard_data

    def get(self, request):
        period = request.GET.get('period', default='week')
        now = timezone.now().replace(hour=23, minute=59)
        period_range_ceil = now

        if period == 'month':
            period_range_floor = now - timedelta(30)
        elif period == 'year':
            period_range_floor = now.replace(year=now.year - 1, day=1)
        else:
            period_range_floor = now - timedelta(6)

        period_range = (
            period_range_floor.replace(hour=0, minute=0), period_range_ceil
        )
        data = self._compile_dashboard_data(period, period_range)
        return JsonResponse(data)
