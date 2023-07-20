import requests
import time
import datetime
import pandas as pd
import gzip
import io
from colorama import init, Fore
from tabulate import tabulate
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

def get_ip_location(ip_address):
    headers = {
        "Authorization": f"Bearer {env_vars['IPINFO_TOKEN']}",
    }
    url = f'https://ipinfo.io/{ip_address}/json'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def enrich_data(df):
    print("Step 3. Enriching data...")
    print("\tStep 3.1. Enriching last login location...")
    df['last_location'] = df.apply(lambda row: get_ip_location(row['last_ip']), axis=1)
    df = df.drop(columns=['last_ip'])
    return df

if __name__ == "__main__":
    create_export_job_endpoint = f"https://{env_vars['AUTH0_TENANT_DOMAIN']}/api/v2/jobs/users-exports"
    stats_endpoint = f"https://{env_vars['AUTH0_TENANT_DOMAIN']}/api/v2/stats/active-users"

    headers = {
        "Authorization": f"Bearer {env_vars['AUTH0_TOKEN']}",
        "Content-Type": "application/json"
    }

    export_payload = {
        "format": "csv",
        "fields": [
            {
                "name": "name"
            },
            {
                "name": "nickname"
            },
            {
                "name": "email"
            },
            {
                "name": "logins_count"
            },
            {
                "name": "last_login"
            },
            {
                "name": "last_ip"
            }
    ]
    }

    try:
        # Create user export job
        response = requests.post(create_export_job_endpoint, headers=headers, json=export_payload)
        response.raise_for_status()
        job_id = response.json()["id"]
        print(f"Step 1. Create users exporting job.\n\tJob ID: {job_id}")
        print("Step 2. Gathering users...")

        # Export all users
        print(f"\tStep 2.2 Downloading users from AWS...")
        time.sleep(10)
        export_job = requests.get(f"https://{env_vars['AUTH0_TENANT_DOMAIN']}/api/v2/jobs/{job_id}", headers=headers)
        export_job.raise_for_status()
        users_url = export_job.json()["location"]
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        local_file_path = f"users_{timestamp}.csv"
        print(f"\tStep 2.2 Exporting users to local file: {local_file_path}")

        try:
            with gzip.open(io.BytesIO(requests.get(users_url).content), 'rt') as gz_file:
                content = gz_file.read().replace("'", "").replace('"', '')
                with open(local_file_path, 'w', newline='') as csv_file:
                    csv_file.write(content)
        
            df = pd.read_csv(local_file_path)
            df = enrich_data(df)
            df.to_csv(local_file_path, index=False)

            # Get number of active users
            stats_response = requests.get(stats_endpoint, headers=headers)
            stats_response.raise_for_status()
            active_users = stats_response.json()

            init(autoreset=True)  # Initialize colorama for colored output

            table_data = [
                ["Active users", Fore.GREEN + f"{active_users}"],
                ["Total users", Fore.CYAN + f"{len(df)}"],
                ["Ratio of active users to total users", Fore.MAGENTA + f"{active_users / len(df):.2%}"],
            ]

            table_headers = ["Statistic", "Value"]

            table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid")
            print(Fore.YELLOW + table)
    
        except requests.exceptions.RequestException as e:
            print(f"Error while downloading users.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error while connecting to Auth0 management API. Check your token.")