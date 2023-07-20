# Auth0 User Retrieval and IP Geolocation Script

## Overview

This repository contains a Python script that leverages Auth0's Management APIs to retrieve all users and active users from your Auth0 account. It then calculates the ratio of active users to all users and obtains the users' locations through IP geolocation using the ipinfo service. The script writes this data to a CSV file with a timestamp in the filename for further analysis and reporting.

Before executing the script, ensure that you have installed all the required dependencies specified in `requirements.txt`. Also, remember to rename `template.env` to `.env` and replace all the variables inside with your Auth0 account and ipinfo service credentials.

## Prerequisites

Before running the script, you need to have the following:

1. Python 3.x installed on your machine.
2. Auth0 account with appropriate credentials and access to the Management APIs.
3. An ipinfo service API token. You can obtain it from [ipinfo](https://ipinfo.io/signup).

## Setup

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Tripflow-io/Travelers-scripts.git
cd Travelers-scripts/export_users
```

2. Install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

3. Rename `template.env` to `.env` and edit the `.env` file to include your Auth0 account and ipinfo service credentials:
```bash
AUTH0_TENANT_DOMAIN=YOUR_AUTH0_TENANT_DOMAIN_HERE
IPINFO_TOKEN=YOUR_IPINFO_TOKEN_HERE
AUTH0_TOKEN=YOUR_AUTH0_TOKEN_HERE
```

## Usage
Run the script using the following command:
```bash
python auth0_user_geolocation.py
```

The script will perform the following steps:
1. Authenticate with Auth0 using the provided credentials.
2. Retrieve all users and active users from your Auth0 account.
3. Calculate the ratio of active users to all users.
4. Perform IP geolocation for each user to obtain their location data using the ipinfo service.
5. Write the user data, including location information, to a CSV file with a timestamp in the filename. The filename will be in the format `users_YYYY-MM-DD_HH-MM-SS.csv`, where `YYYY` is the year, `MM` is the month, `DD` is the day, `HH` is the hour, `MM` is the minute, and `SS` is the second.

## CSV Format
The CSV file will have the following columns:

1. `name`: The name of the user (if available).
2. `nickname`: The nickname of the user (if available).
3. `email`: The email address associated with the user.
4. `logins_count`: The number of logins for the user.
5. `last_login`: The timestamp of the user's last login.
6. `last_ip`: The IP address of the user's last login.

## Note
- Ensure that your Auth0 account has the necessary permissions to access the Management APIs and retrieve user data.
- Make sure to handle your API keys and sensitive information securely and avoid sharing them publicly.

## License
### MIT License
Feel free to use, modify, and distribute this script following the terms of the MIT License.

## Reach out
For any questions or issues, please open an issue on the repository or contact the author at [lorenzobalzani@tripflow.io](mailto:lorenzobalzai@tripflow.io).
