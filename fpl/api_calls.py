from re import S
import pandas as pd
import json
import requests

def get_manager_history(manager_id: int) -> pd.DataFrame:

    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/history/"

    response = requests.get(f"{url}")

    if response.status_code == 200:
        print("Succes!")
        data = response.json()
        df = pd.DataFrame.from_records(data["current"])

        return df

    else:
        print(f"Error: {response.status_code}")
        print(f"URL: {url}")

def get_combined_manager_history(managers_dict: dict) -> pd.DataFrame:
    
    list_dfs = []
    for manager in managers_dict.keys():


        manager_id = managers_dict[manager]
        df = get_manager_history(manager_id=manager_id)

        df["manager"] = manager
        list_dfs.append(df)

    df_mananger_history_comb = pd.concat(list_dfs)

    return df_mananger_history_comb

if __name__ == "__main__":
    
    # manager_id = 1302722

    # df = get_manager_history(manager_id=manager_id)

    # print(df.columns)
    
    managers_dict = {
        "Chistian": 1302722,
        "Hans-Martin": 1302722,
        "Andreas": 1302722,
    }

    df_combined = get_combined_manager_history(managers_dict=managers_dict)
    print(df_combined)