import os
import pandas as pd
from django.conf import settings
from huggingface_hub import InferenceClient
from .models import MatchPredictionLog

def predict_match_outcome(team_name: str):
    csv_path = os.path.join(settings.BASE_DIR, 'data', 'ucl_stats.csv')
    df = pd.read_csv(csv_path)
    
    team_data = df[df['team'].str.contains(team_name, case=False, na=False)]
    if team_data.empty:
        return f"No historical stats found for team: {team_name}"
    
    stats_summary = team_data.to_string(index=False)
    
    client = InferenceClient(
        model="meta-llama/Llama-3.1-8B-Instruct",
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    
    prompt = f"""You are an expert UEFA Champions League football analyst.
Based on the following historical stats (columns: year, team, match_played, wins, draws, losts, goals_scored, goals_conceded, gd, group_point, champions):
{stats_summary}

Analyze the performance for {team_name} and output ONLY a predicted win probability percentage (e.g., 68.5) and a short analytical reason.
Format: Probability: [number]% | Reason: [text]"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.3
    )
    
    response_text = response.choices[0].message.content
    
    MatchPredictionLog.objects.create(
        team_name=team_name,
        predicted_win_probability=75.0,
        anomaly_score=0.15
    )
    
    return response_text