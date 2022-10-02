# NASA Space Apps 2022 Backend
## Team: Space Jam
## Challenge: Take Flight: Making the Most of NASA’s Airborne Data
Backend Code for NASA Space Apps 2022.

# Dependencies
- Python 3.10
- Pipenv

# How to Run
This project uses pipenv for dependency management. 

1. Install pipenv
```
pip install --user pipenv
```

2. Begin pipenv shell
```
pipenv shell
```

3. Install project's dependencies
```
pipenv install
```

4. Run the project
```
gunicorn -c src/gunicorn.conf.py -b :5000 src.main:app
```

# Public API
This API is currently hosted publicly using Google Cloud. If you would like to hit this endpoint without needing
to install or build the project you can access the API at the following URL:

`https://space-app-364302.uc.r.appspot.com/api/google-cloud/filename/2020_pcp.png`

The data will be returned in the following format:
```
{
    "callbackUrl": "...",
    "filename": "..."
}
```

The `callbackUrl` field is a signed URL from Google Cloud that is valid for 1 hour. With this URL you can download and view the visualizations.

You can change the final parameter to a variety of file names in order to see multiple different data sets visualized.
