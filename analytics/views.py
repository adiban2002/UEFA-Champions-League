from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from analytics.models import UCLStats
from analytics.reports import UCLReportGenerator

@login_required(login_url='/admin/login/')
def ucl_dashboard_view(request):
    report_gen = UCLReportGenerator()
    leaderboard = report_gen.generate_global_leaderboard_report(top_n=5)
    total_records = UCLStats.objects.count()
    
    context = {
        'total_records': total_records,
        'top_scorers': leaderboard.get('top_scorers', []),
        'championship_leaders': leaderboard.get('championship_leaders', []),
        'highest_group_scorers': leaderboard.get('highest_group_scorers', []),
    }
    
    return render(request, 'analytics/dashboard.html', context)