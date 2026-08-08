import pandas as pd
import os

class UCLAnalyticsEngine:
    def __init__(self, csv_file_path="data/ucl_stats.csv"):
        self.csv_file_path = csv_file_path
        self.df = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"Dataset not found at: {self.csv_file_path}")
        
        df = pd.read_csv(self.csv_file_path)
        df.columns = df.columns.str.strip().str.lower()
        return df

    def get_team_comprehensive_stats(self, team_name):
        team_df = self.df[self.df['team'].str.lower() == team_name.lower()]
        
        if team_df.empty:
            return {"error": f"Team '{team_name}' not found in dataset."}

        total_matches = int(team_df['match_played'].sum())
        total_wins = int(team_df['wins'].sum())
        total_draws = int(team_df['draws'].sum())
        total_losses = int(team_df['losts'].sum())
        total_goals_scored = int(team_df['goals_scored'].sum())
        total_goals_conceded = int(team_df['goals_conceded'].sum())
        total_gd = int(team_df['gd'].sum())
        total_group_points = int(team_df['group_point'].sum())
        total_championships = int(team_df['champions'].sum())
        
        win_ratio = round((total_wins / total_matches) * 100, 2) if total_matches > 0 else 0.0

        return {
            "team": team_name,
            "total_matches": total_matches,
            "wins": total_wins,
            "draws": total_draws,
            "losses": total_losses,
            "win_ratio_percentage": win_ratio,
            "goals_scored": total_goals_scored,
            "goals_conceded": total_goals_conceded,
            "goal_difference": total_gd,
            "group_points": total_group_points,
            "championships_won": total_championships
        }

    def get_season_highlights(self, year):
        season_df = self.df[self.df['year'] == year]
        
        if season_df.empty:
            return {"error": f"Data for season year '{year}' not found."}
        
        season_sorted = season_df.sort_values(by=['champions', 'group_point', 'gd'], ascending=False)
        return season_sorted.to_dict(orient='records')

    def get_top_ranked_teams(self, metric='goals_scored', top_n=5):
        valid_metrics = ['match_played', 'wins', 'draws', 'losts', 'goals_scored', 'goals_conceded', 'gd', 'group_point', 'champions']
        if metric not in valid_metrics:
            return {"error": f"Invalid metric. Choose from {valid_metrics}"}
        
        aggregated = self.df.groupby('team')[metric].sum().reset_index()
        top_teams = aggregated.sort_values(by=metric, ascending=False).head(top_n)
        
        return top_teams.to_dict(orient='records')

if __name__ == "__main__":
    engine = UCLAnalyticsEngine()
    print("UCL Analytics Engine Loaded Successfully with exact columns!")
    print("Top 3 Goal Scoring Teams:", engine.get_top_ranked_teams('goals_scored', 3))