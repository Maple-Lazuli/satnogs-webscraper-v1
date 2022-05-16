![image-20220515234951600](/home/ada/CodeProjects/satnogs-webscraper/images/image-20220515234951600.png)

# SATNOGS Web-scraper

[SATNOGS](https://satnogs.org/) is an open source network of ground stations around the world that collect satellite telemetry. The data SATNOGS aggregates has extreme value for numerous purposes, but can be difficult to compile into a single dataset.

This project serves to alleviate the difficulty of compiling from SATNOGS by using their back-end database to generate a list of satellites and telemetry intercept events, then uses that list to scrape the observation events from the [SATNOGS network](https://network.satnogs.org/observations/)

## Concept of Execution

The script functions in 4 phases:

1. Aggregate Satellite Data
2. Aggregate Telemetry Data
3. Scrape Observation Webpages and Process PSDs
4. Compile Dataset

#### 1. Aggregate Satellite Data

The script starts by using the Satellites Endpoint ([api reference](https://db.satnogs.org/api/schema/docs/#/satellites)) to compile a list of satellites in the database and record the *unique IDs* that SATNOGS uses internally. Below is an example of the data collected for each satellite in the database:

```json
[
  {
    "norad_cat_id": 25544,
    "name": "ISS",
    "names": "ZARYA",
    "image": "https://db-satnogs.freetls.fastly.net/media/satellites/ISS.jpg",
    "status": "alive",
    "decayed": null,
    "launched": "1998-11-20T00:00:00Z",
    "deployed": "1998-11-20T00:00:00Z",
    "website": "https://www.nasa.gov/mission_pages/station/main/index.html",
    "operator": "None",
    "countries": "RU,US",
    "telemetries": [
      {
        "decoder": "iss"
      }
    ]
  }
]
```

#### 2. Aggregate Telemetry Intercept Event Data

Then the script will use those *unique IDs* to query the Telemetry Endpoint ([api reference](https://db.satnogs.org/api/schema/docs/#/telemetry/telemetry_retrieve)) to capture the telemetry intercept events, which includes an *Observation ID*.  Below is an example of the data collected for each telemetry intercept event:

```json
{"sat_id": "BWZN-6466-6429-8096-5664", 
 "norad_cat_id": 99811, 
 "transmitter": "", 
 "app_source": "network", 
 "schema": "", 
 "decoded": "", 
 "frame": "4FCE27030FCBF246B8536D8D662499180C245B0516A050735CEA32DF17B06F1CE1EB4327C95AC1EB02EC6DA99CF728D1555F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F5F", "observer": "Budapest UHF2 (west only)-JN97ml", 
 "timestamp": "2021-03-28T02:03:00Z", 
 "version": "", 
 "observation_id": 3852450, 
 "station_id": 1824, 
 "associated_satellites": []
}
```



An important note here is that the results of from the telemetry endpoint are paginated, with 25 results per page. The script will iterate through the pages until it finds text identifying the last page in the results. 

#### 3. Scrape Observation Webpages

The script will then use the *Observation ID* to generate links to the webpages on the  [SATNOGS network](https://network.satnogs.org/) and scrape the contents of the webpages. An example observation can be found [here](https://network.satnogs.org/observations/5936801/). The script attempts to sensibly parse the text contents of the web pages and download the waterfall images (also know as power spectral display (PSD) images) to the disk. When the PSD images are downloaded, the script will crop the images to remove any text and convert the images to grey scale.  An example of the processing can be seen below:



![PSD Processing](/home/ada/CodeProjects/satnogs-webscraper/images/psd-processing.drawio.png)



#### 4. Dataset Compilation

After scraping all of the observation web pages, the script compiles the data from each step into a single comma seperated value (CSV) file.



## Script Execution

The script can be executed in two ways:

1. Using a Docker Container built from the Dockerfile in this repositiory
2. Running locally with the *data_pull.py* script

**NOTE**: Prior to execution with either method, a key needs to be recorded from [SATNOGS DB](https://db.satnogs.org/) and added to a keys.txt file.



### Using Docker

First, verify that docker engine is installed on the host machine.

Once verified, create the docker container with the command:

```bash
docker build . -f Dockerfile -t satnogs-webscraper
```

Then after the container has finished being built, run the container with the command:

```bash
docker run -d -v <path-to-save-data-in:/opt/app/data satnogs-webscraper
```

This will cause the script to run in a docker container and save the results to the directory specified in the previous command.

### Running Locally

First verify that python3  and pip are installed. 

Once verified, navigate to the root directory of the project and create a virtual environment with the command below:

```bash
python3 -m venv venv
```

Then  source that virtual environment with:

```bash
source ./venv/bin/activate
```

With the environment sourced, install the requirments with:

```bash
pip install requirements.txt
```

Finally, with the virtual environment still sourced and requirements installed, run the data_pull.py script:

```bash
python -m src.data_pull
```

