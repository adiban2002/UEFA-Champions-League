from django.db import models
class UCLStats(models.Model):
    year = models.IntegerField(db_index=True)
    team = models.CharField(max_length=100)
    match_played = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losts = models.IntegerField()
    goals_scored = models.IntegerField()
    goals_conceded = models.IntegerField()
    gd = models.IntegerField()
    group_point = models.IntegerField()
    champions = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "UCL Statistic"
        verbose_name_plural = "UCL Statistics"

    def __str__(self):
        return f"{self.team} ({self.year})"