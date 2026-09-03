import os
import pandas as pd
from django.conf import settings
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from .models import MatchPredictionLog

def predict_match_outcome(team_name: str):
    csv_path = os.path.join(settings.BASE_DIR, 'data', 'ucl_stats.csv')
    df = pd.read_csv(csv_path)
    
    team_data = df[df['team'].str.contains(team_name, case=False, na=False)]
    if team_data.empty:
        return f"No historical stats found for team: {team_name}"
    
    stats_summary = team_data.to_string(index=False)
    
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        temperature=0.3,
        max_new_tokens=250,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    
    prompt = PromptTemplate.from_template(
        """You are an expert UEFA Champions League football analyst.
Based on the following historical stats (columns: year, team, match_played, wins, draws, losts, goals_scored, goals_conceded, gd, group_point, champions):
{stats_summary}

Analyze the performance for {team_name} and output ONLY a predicted win probability percentage (e.g., 68.5) and a short analytical reason.
Format: Probability: [number]% | Reason: [text]"""
    )
    
    chain = prompt | llm
    response = chain.invoke({"team_name": team_name, "stats_summary": stats_summary})
    
    MatchPredictionLog.objects.create(
        team_name=team_name,
        predicted_win_probability=75.0,
        anomaly_score=0.15
    )
    
    return response