import csv
import argparse
import os
import subprocess
from collections import defaultdict

PLAYERS_FILE = "players.csv"
MATCHES_FILE = "matches.csv"

def load_players():
    if not os.path.exists(PLAYERS_FILE):
        return []
    with open(PLAYERS_FILE) as file:
        reader = csv.DictReader(file)
        return [{"name": row["name"], "color": row["color"], "points": int(row["points"]), "matches": int(row["matches"])} for row in reader]

def load_matches():
    if not os.path.exists(MATCHES_FILE):
        return []
    with open(MATCHES_FILE) as file:
        reader = csv.DictReader(file)
        return [{"player": row["player"], "cup": row["cup"], "points": int(row["points"])} for row in reader]

def save_players(players):
    with open(PLAYERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "color", "points", "matches"])
        writer.writeheader()
        writer.writerows(players)

def save_matches(matches):
    with open(MATCHES_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["player", "cup", "points"])
        writer.writeheader()
        writer.writerows(matches)

def add_player(players):
    name = input("🎮 Player name: ")
    color = input("🎨 Player color: ")
    players.append({"name": name, "color": color, "points": 0, "matches": 0})
    return players

def add_score(matches):
    player = input("🏁 Player: ")
    cup = input("🏆 Cup: ")
    points = int(input("🎯 Points: "))
    matches.append({"player": player, "cup": cup, "points": points})
    return matches

def calculate_points(players, matches):
    totals = defaultdict(int)
    counts = defaultdict(int)
    for m in matches:
        totals[m["player"]] += m["points"]
        counts[m["player"]] += 1
    for p in players:
        p["points"] = totals[p["name"]]
        p["matches"] = counts[p["name"]]
    return players

def write_md(players, matches, output_file="index.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🏆 Mario Kart Tournament\n\n## 🥇 Rankings\n\n")
        players.sort(key=lambda p: p["points"] / p["matches"] if p["matches"] else 0, reverse=True)
        for p in players:
            if p["matches"] == 0:
                avg = 0
            else:
                avg = round(p["points"]/p["matches"], 2)
            f.write(f"""
**{p["name"]}: {avg} Avg Points**
<div style="background-color: #eee; border-radius: 8px; width: 100%; height: 20px;">
  <div style="width: {(avg):.1f}%; background-color: {p["color"]}; height: 100%; border-radius: 8px;"></div>
</div>
""")
        f.write("\n---\n\n## 🏁 Race Results\n\n")
        f.write("| Player | Cup | Points |\n|--------|-----|--------|\n")
        for m in reversed(matches):
            f.write(f"| {m['player']} | {m['cup']} | {m['points']} |\n")

def git_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "🔄 Mario Kart update"], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    parser = argparse.ArgumentParser(description="🏎️ Mario Kart Tournament Manager")
    parser.add_argument("--add-player", action="store_true", help="Add a player")
    parser.add_argument("--add-score", action="store_true", help="Add a race score")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild site and push")
    args = parser.parse_args()

    players = load_players()
    matches = load_matches()

    if args.add_player:
        players = add_player(players)

    if args.add_score:
        for player in players:
            print(player["name"])
        matches = add_score(matches)

    if args.add_player or args.add_score or args.rebuild:
        players = calculate_points(players, matches)
        save_players(players)
        save_matches(matches)
        write_md(players, matches)

    if args.rebuild:
        git_push()

if __name__ == "__main__":
    main()
