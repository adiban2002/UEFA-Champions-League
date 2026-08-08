import os
import pandas as pd
from analytics.metrics import UCLAnalyticsEngine

class UCLReportGenerator:
    def __init__(self, csv_file_path="data/ucl_stats.csv"):
        self.engine = UCLAnalyticsEngine(csv_file_path)

    def generate_team_report(self, team_name):
        stats = self.engine.get_team_comprehensive_stats(team_name)
        
        if "error" in stats:
            return stats

        report_summary = (
            f"=== UCL PERFORMANCE REPORT: {stats['team'].upper()} ===\n"
            f"• Total Matches Played: {stats['total_matches']}\n"
            f"• Total Wins: {stats['wins']} | Draws: {stats['draws']} | Losses: {stats['losses']}\n"
            f"• Win Ratio: {stats['win_ratio_percentage']}%\n"
            f"• Goals Scored: {stats['goals_scored']} | Goals Conceded: {stats['goals_conceded']}\n"
            f"• Net Goal Difference (GD): {stats['goal_difference']}\n"
            f"• Total Group Points: {stats['group_points']}\n"
            f"• Championships Won: {stats['championships_won']}\n"
            f"=================================================="
        )
        
        return {
            "status": "success",
            "summary_text": report_summary,
            "metrics": stats
        }

    def generate_global_leaderboard_report(self, top_n=5):
        return {
            "status": "success",
            "top_scorers": self.engine.get_top_ranked_teams('goals_scored', top_n),
            "championship_leaders": self.engine.get_top_ranked_teams('champions', top_n),
            "highest_group_scorers": self.engine.get_top_ranked_teams('group_point', top_n)
        }