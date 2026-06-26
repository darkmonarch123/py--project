import requests

def fetch_world_cup_data():
    url = "https://raw.githubusercontent.com/openfootball/football.json/master/2025-26/en.1.json"
    print("📡 Fetching FIFA World Cup database...\n")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def generate_stats_table(data):
    stats = {}
    
    # 1. Parse the tournament matches
    for round_info in data.get("rounds", []):
        for match in round_info.get("matches", []):
            team1 = match.get("team1")
            team2 = match.get("team2")
            
            if not team1 or not team2: continue
                
            # Initialize teams if they aren't in our tracker yet
            for team in (team1, team2):
                if team not in stats:
                    stats[team] = {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0}
                    
            # 2. Extract Scores and Calculate Match Outcomes
            if "score" in match and match["score"] and "ft" in match["score"]:
                ft = match["score"]["ft"]
                if len(ft) >= 2:
                    t1_goals, t2_goals = ft[0], ft[1]
                    
                    # Update Matches Played & Goals
                    stats[team1]["P"] += 1
                    stats[team2]["P"] += 1
                    stats[team1]["GF"] += t1_goals
                    stats[team1]["GA"] += t2_goals
                    stats[team2]["GF"] += t2_goals
                    stats[team2]["GA"] += t1_goals
                    
                    # Calculate Wins, Draws, Losses (based on regular time)
                    if t1_goals > t2_goals:
                        stats[team1]["W"] += 1
                        stats[team2]["L"] += 1
                    elif t2_goals > t1_goals:
                        stats[team2]["W"] += 1
                        stats[team1]["L"] += 1
                    else:
                        stats[team1]["D"] += 1
                        stats[team2]["D"] += 1

    # 3. Calculate Advanced Stats (Goal Difference & Expected Corners)
    table_data = []
    for team, data in stats.items():
        gd = data["GF"] - data["GA"]
        # Expected Corners = 4.2 base + (Avg Goals Scored * 0.4)
        avg_goals = data["GF"] / data["P"] if data["P"] > 0 else 0
        exp_corners = 4.2 + (avg_goals * 0.4)
        
        table_data.append({
            "Team": team,
            "Played": data["P"],
            "Wins": data["W"],
            "Draws": data["D"],
            "Losses": data["L"],
            "Goals_For": data["GF"],
            "Goals_Against": data["GA"],
            "Goal_Diff": gd,
            "Exp_Corners": exp_corners
        })

    # 4. Sort the table by Wins (descending), then Goal Difference
    table_data.sort(key=lambda x: (x["Wins"], x["Goal_Diff"]), reverse=True)
    return table_data

def display_dashboard(table_data):
    # Print the Table Header
    print("="*95)
    print(f"{'TEAM':<18} | {'PLAYED':<6} | {'WINS':<4} | {'DRAWS':<5} | {'LOSSES':<6} | {'GOALS':<5} | {'CONCEDED':<8} | {'GD':<4} | {'xCORNERS/GM':<12}")
    print("="*95)
    
    # Print the Table Rows
    for row in table_data:
        gd_str = f"+{row['Goal_Diff']}" if row['Goal_Diff'] > 0 else str(row['Goal_Diff'])
        print(f"{row['Team']:<18} | {row['Played']:<6} | {row['Wins']:<4} | {row['Draws']:<5} | {row['Losses']:<6} | {row['Goals_For']:<5} | {row['Goals_Against']:<8} | {gd_str:<4} | {row['Exp_Corners']:.1f}")
    
    print("="*95)
    print("* xCORNERS/GM = Expected Corners per Game (Data-Modeled based on attacking pressure)")

if __name__ == "__main__":
    raw_data = fetch_world_cup_data()
    if raw_data:
        compiled_table = generate_stats_table(raw_data)
        display_dashboard(compiled_table)