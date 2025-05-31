import sys
import os

# Get the absolute path to the 'daily' folder
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'daily'))
sys.path.append(base_path)

# sys.path.append('/Users/bea/Desktop/daily-planner/daily')
# print(sys.path)

from daily_planner.planner import run_planner

if __name__ == "__main__":
    run_planner()
