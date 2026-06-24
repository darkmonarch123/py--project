import math
import random
import requests

# --------------------------------------------------------
# 1. Data Pipeline
# --------------------------------------------------------
def fetch_live_data():
    url = "https://raw.githubusercontent.com/openfootball/football.json/master/2020-21/en.1.json"
    print("📡 Pulling latest match logs from data stream...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

# --------------------------------------------------------
# 2. Analytics Core (Data Modeling)
# --------------------------------------------------------
def process_advanced_stats(data):
    raw_stats = {}
    matches = data.get("matches", []) if "matches" in data else []
    if "rounds" in data:
        for round_info in data["rounds"]:
            matches.extend(round_info.get("matches", []))
            
    for match in matches:
        home_team = match.get("team1")
        away_team = match.get("team2")
        if not home_team or not away_team:
            continue
            
        if home_team not in raw_stats:
            raw_stats[home_team] = {"h_scored": 0, "h_conceded": 0, "h_games": 0, "a_scored": 0, "a_conceded": 0, "a_games": 0}
        if away_team not in raw_stats:
            raw_stats[away_team] = {"h_scored": 0, "h_conceded": 0, "h_games": 0, "a_scored": 0, "a_conceded": 0, "a_games": 0}
            
        if "score" in match and match["score"] and "ft" in match["score"]:
            ft_score = match["score"]["ft"]
            if len(ft_score) >= 2:
                home_goals, away_goals = ft_score[0], ft_score[1]
                
                raw_stats[home_team]["h_scored"] += home_goals
                raw_stats[home_team]["h_conceded"] += away_goals
                raw_stats[home_team]["h_games"] += 1
                
                raw_stats[away_team]["a_scored"] += away_goals
                raw_stats[away_team]["a_conceded"] += home_goals
                raw_stats[away_team]["a_games"] += 1

    model_database = {}
    for team, data in raw_stats.items():
        if data["h_games"] > 0 and data["a_games"] > 0:
            model_database[team] = {
                "home_attack": data["h_scored"] / data["h_games"],
                "home_defense": data["h_conceded"] / data["h_games"],
                "away_attack": data["a_scored"] / data["a_games"],
                "away_defense": data["a_conceded"] / data["a_games"]
            }
    return model_database

# --------------------------------------------------------
# 3. Simulation & Advanced Market Math
# --------------------------------------------------------
def simulate_poisson(lambda_val):
    if lambda_val <= 0: return 0
    e_lambda = math.exp(-lambda_val)
    k, p = 0, 1.0
    while p > e_lambda:
        k += 1
        p *= random.random()
    return k - 1

def execute_multi_market_simulation(database, home_team, away_team, iterations=25000):
    # Goal Expectations
    expected_home_goals = (database[home_team]["home_attack"] + database[away_team]["away_defense"]) / 2
    expected_away_goals = (database[away_team]["away_attack"] + database[home_team]["home_defense"]) / 2
    
    # Corner Expectations (Derived from attacking metrics. Base league average is ~5.5 per team)
    expected_home_corners = 4.8 + (database[home_team]["home_attack"] * 0.4)
    expected_away_corners = 4.2 + (database[away_team]["away_attack"] * 0.4)

    # Market Counter Variables
    home_wins, away_wins, draws = 0, 0, 0
    first_goal_home, first_goal_away, first_goal_none = 0, 0, 0
    total_corners_accumulated = 0
    
    over_1_5, over_2_5, over_3_5 = 0, 0, 0

    # Execute Monte Carlo Pathing Matrix
    for _ in range(iterations):
        # 1. Simulate Goals
        sim_h_goals = simulate_poisson(expected_home_goals)
        sim_v_goals = simulate_poisson(expected_away_goals)
        total_goals = sim_h_goals + sim_v_goals
        
        # 2. Simulate Corners
        sim_h_corners = simulate_poisson(expected_home_corners)
        sim_v_corners = simulate_poisson(expected_away_corners)
        total_corners_accumulated += (sim_h_corners + sim_v_corners)

        # Match Outcomes
        if sim_h_goals > sim_v_goals: home_wins += 1
        elif sim_v_goals > sim_h_goals: away_wins += 1
        else: draws += 1

        # Over / Under Target Lines
        if total_goals > 1.5: over_1_5 += 1
        if total_goals > 2.5: over_2_5 += 1
        if total_goals > 3.5: over_3_5 += 1

        # First Goal Dynamics (Probability distribution calculation based on scoring weights)
        if total_goals == 0:
            first_goal_none += 1
        else:
            # Chance of scoring first correlates heavily to attacking rate
            weight_home = expected_home_goals / (expected_home_goals + expected_away_goals)
            if random.random() < weight_home:
                first_goal_home += 1
            else:
                first_goal_away += 1

    # Crunching Analytics Ratios
    avg_predicted_corners = total_corners_accumulated / iterations

    # --------------------------------------------------------
    # 4. Display Pro-Tier Analytics Dashboard
    # --------------------------------------------------------
    print("\n" + "═"*60)
    print("📊       PRO-TIER MULTI-MARKET PREDICTION REPORT")
    print("═"*60)
    print(f"🏟️  MATCHUP: {home_team} (HOME) vs {away_team} (AWAY)")
    print("─"*60)
    print("🔮 MAIN MATCH OUTCOMES")
    print(f" └─ {home_team} Win Chance   : {(home_wins/iterations)*100:.2f}%")
    print(f" └─ {away_team} Win Chance   : {(away_wins/iterations)*100:.2f}%")
    print(f" └─ Draw Chance              : {(draws/iterations)*100:.2f}%")
    print("─"*60)
    
    print("⚽ OVER / UNDER GOAL MARKETS")
    print(f" └─ Over 1.5 Total Goals     : {(over_1_5/iterations)*100:.2f}%  |  Under 1.5: {(1 - over_1_5/iterations)*100:.2f}%")
    print(f" └─ Over 2.5 Total Goals     : {(over_2_5/iterations)*100:.2f}%  |  Under 2.5: {(1 - over_2_5/iterations)*100:.2f}%")
    print(f" └─ Over 3.5 Total Goals     : {(over_3_5/iterations)*100:.2f}%  |  Under 3.5: {(1 - over_3_5/iterations)*100:.2f}%")
    print("─"*60)

    print("🚩 CORNERS & SPECIALS")
    print(f" └─ Predicted Total Corners  : {avg_predicted_corners:.1f}")
    print(f" └─ {home_team} Scores First: {(first_goal_home/iterations)*100:.2f}%")
    print(f" └─ {away_team} Scores First: {(first_goal_away/iterations)*100:.2f}%")
    print(f" └─ No Goals Scored (0-0)   : {(first_goal_none/iterations)*100:.2f}%")
    print("═"*60 + "\n")

# --------------------------------------------------------
# 5. Controller Layer
# --------------------------------------------------------
def main():
    raw_data = fetch_live_data()
    if not raw_data: return
    
    processed_db = process_advanced_stats(raw_data)
    available_teams = sorted(list(processed_db.keys()))
    
    print("\n🏆 LIVE PREMIER LEAGUE TEAMS:")
    for index, team_name in enumerate(available_teams, 1):
        print(f" {index:2d}. {team_name}")
        
    print("\n📌 INPUT MATCHUP FIXTURE NUMBERS")
    try:
        home_idx = int(input("Enter Home Team Number: ")) - 1
        away_idx = int(input("Enter Away Team Number: ")) - 1
        
        if home_idx == away_idx:
            print("❌ Invalid Matchup: A team cannot play itself.")
            return
            
        execute_multi_market_simulation(processed_db, available_teams[home_idx], available_teams[away_idx])
    except (ValueError, IndexError):
        print("❌ Error: Select valid numerical indices from the panel menu above.")

if __name__ == "__main__":
    main()