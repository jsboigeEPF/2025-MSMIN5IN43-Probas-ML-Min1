"""
Modèle de Prédictions de Football (Simplifié - Sans PyMC)
Basé sur les statistiques descriptives des équipes
"""

import numpy as np
from typing import Dict, List
from datetime import datetime


class BayesianFootballModel:
    """
    Modèle simplifié de prédictions de football
    Utilise les statistiques descriptives sans inférence Bayésienne complexe
    """

    def __init__(self):
        self.team_stats = {}
        self.is_fitted = False

    def fit(self, matches: List[Dict], draws: int = 500, tune: int = 500):
        """
        Entraîner le modèle sur les matchs historiques
        matches: liste de {'team1': str, 'team2': str, 'home_score': int, 'away_score': int}
        """
        self.team_stats = {}
        
        for match in matches:
            team1 = match.get('team1')
            team2 = match.get('team2')
            
            if not team1 or not team2:
                continue
                
            if team1 not in self.team_stats:
                self.team_stats[team1] = {
                    'matches': 0,
                    'wins': 0,
                    'draws': 0,
                    'losses': 0,
                    'goals_for': 0,
                    'goals_against': 0,
                    'attack_strength': 1.0,
                    'defense_strength': 1.0
                }
            if team2 not in self.team_stats:
                self.team_stats[team2] = {
                    'matches': 0,
                    'wins': 0,
                    'draws': 0,
                    'losses': 0,
                    'goals_for': 0,
                    'goals_against': 0,
                    'attack_strength': 1.0,
                    'defense_strength': 1.0
                }
            
            home_score = match.get('home_score', 0)
            away_score = match.get('away_score', 0)
            
            self.team_stats[team1]['matches'] += 1
            self.team_stats[team1]['goals_for'] += home_score
            self.team_stats[team1]['goals_against'] += away_score
            
            self.team_stats[team2]['matches'] += 1
            self.team_stats[team2]['goals_for'] += away_score
            self.team_stats[team2]['goals_against'] += home_score
            
            # Résultat
            if home_score > away_score:
                self.team_stats[team1]['wins'] += 1
                self.team_stats[team2]['losses'] += 1
            elif home_score < away_score:
                self.team_stats[team1]['losses'] += 1
                self.team_stats[team2]['wins'] += 1
            else:
                self.team_stats[team1]['draws'] += 1
                self.team_stats[team2]['draws'] += 1
        
        # Calculer les forces d'attaque et défense
        for team, stats in self.team_stats.items():
            if stats['matches'] > 0:
                stats['attack_strength'] = stats['goals_for'] / max(stats['matches'], 1)
                stats['defense_strength'] = 1.0 / (stats['goals_against'] / max(stats['matches'], 1) + 1)
        
        self.is_fitted = True

    def predict_match(self, team1: str, team2: str, n_samples: int = 10000) -> Dict:
        """
        Prédire le résultat d'un match
        """
        if not self.is_fitted:
            return {'error': 'Model not fitted yet'}
        
        if team1 not in self.team_stats:
            return {'error': f'Team {team1} not in training data'}
        if team2 not in self.team_stats:
            return {'error': f'Team {team2} not in training data'}
        
        stats1 = self.team_stats[team1]
        stats2 = self.team_stats[team2]
        
        home_attack = max(stats1['attack_strength'], 0.1)
        home_defense = max(stats1['defense_strength'], 0.1)
        away_attack = max(stats2['attack_strength'], 0.1)
        away_defense = max(stats2['defense_strength'], 0.1)
        
        home_advantage = 0.3
        
        expected_home_goals = (home_attack / away_defense) * (1 + home_advantage)
        expected_away_goals = (away_attack / home_defense)
        
        home_wins = 0
        draws = 0
        away_wins = 0
        
        np.random.seed(42)
        for _ in range(n_samples):
            home_goals = np.random.poisson(max(expected_home_goals, 0.1))
            away_goals = np.random.poisson(max(expected_away_goals, 0.1))
            
            if home_goals > away_goals:
                home_wins += 1
            elif home_goals == away_goals:
                draws += 1
            else:
                away_wins += 1
        
        home_win_prob = home_wins / n_samples
        draw_prob = draws / n_samples
        away_win_prob = away_wins / n_samples
        
        home_odds = 1 / max(home_win_prob, 0.01)
        draw_odds = 1 / max(draw_prob, 0.01)
        away_odds = 1 / max(away_win_prob, 0.01)
        
        return {
            'team1': team1,
            'team2': team2,
            'home_win_prob': float(home_win_prob),
            'draw_prob': float(draw_prob),
            'away_win_prob': float(away_win_prob),
            'expected_home_goals': float(expected_home_goals),
            'expected_away_goals': float(expected_away_goals),
            'home_odds': float(home_odds),
            'draw_odds': float(draw_odds),
            'away_odds': float(away_odds),
            'confidence': 0.7,
            'timestamp': datetime.now().isoformat()
        }

    def get_team_stats(self) -> Dict[str, Dict]:
        """Retourner les stats de toutes les équipes"""
        result = {}
        for team, stats in self.team_stats.items():
            result[team] = {
                'attack': float(stats['attack_strength']),
                'defense': float(stats['defense_strength']),
                'strength': float((stats['attack_strength'] + 1.0 / max(stats['defense_strength'], 0.1)) / 2),
                'matches': int(stats['matches']),
                'wins': int(stats['wins']),
                'draws': int(stats['draws']),
                'losses': int(stats['losses'])
            }
        return result
