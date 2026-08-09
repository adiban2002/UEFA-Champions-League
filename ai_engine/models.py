from django.db import models
class MatchPredictionLog(models.Model):
    team_name = models.CharField(max_length=100)
    predicted_win_probability = models.FloatField()
    anomaly_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team_name} - Prob: {self.predicted_win_probability}%"