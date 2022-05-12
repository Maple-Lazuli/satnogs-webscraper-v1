import json
import pandas as pd
from satellites import Satellites
from telemetry import Telemetry
from observation_scrapper import ObservationScrapper
import constants as cnst


def fix_freqs(freq):
    """
    Helper function to clean up the frequencies from the web scraping
    :param freq: The frequency to clean
    :return: Cleaned frequency string
    """
    if freq is None:
        return 0
    freq = freq.replace(",", "")
    return freq[:-2]


def complete_dataset():
    """
    Creates the completed dataset by combining the events, observations, and satellite data into one dataframe.
    :param complete_path: The path to store the completed dataframe in.
    :return: Returns a copy of the completed dataframe.
    """
    with open(cnst.directories['observation_json'], 'r') as file_in:
        observations_df = pd.DataFrame.from_dict(json.load(file_in))
    observations_df['Frequency'] = observations_df['Frequency'].apply(lambda x: fix_freqs(x)).astype(int)
    observations_df['Observation_id'] = observations_df['Observation_id'].fillna(-1).astype(int)

    with open(cnst.directories['tm_compiled_json'], 'r') as file_in:
        events_df = pd.DataFrame.from_dict(json.load(file_in))
    events_df['observation_id'] = events_df['observation_id'].fillna(-1).astype(int)
    observations_df = observations_df.merge(events_df, left_on='Observation_id', right_on='observation_id', how='left')

    sat_df = pd.read_csv(cnst.directories['satellites_csv'])
    observations_df = observations_df.merge(sat_df, on='sat_id', how='left')
    observations_df.to_csv(cnst.directories['combined_csv'])
    return observations_df


if __name__ == '__main__':
    # Pull list of satellite IDs from SATNOGs Database
    # sat = Satellites()
    # sat_ids = sat.get_dataframe().index.values
    # # Use satellite IDs to query TM events and find observation IDs
    # tm = Telemetry(prints=True, max_pages=1)
    # tm.clear_archived_events()
    # tm.multiprocess_fetch(sat_ids, update_tm_events=True)
    # tm_df = tm.get_events_df(save_csv=True)
    # # extract observation IDs from the telemetry data frame
    # tm_df['observation_id'] = tm_df['observation_id'].fillna(0)
    # tm_df['observation_id'] = tm_df['observation_id'].astype(int)
    # observations = pd.unique(tm_df[tm_df['observation_id'] > 0]['observation_id'])
    # # start web scraping from the observation IDs
    # scrapper = ObservationScrapper()
    # scrapper.multiprocess_scrape_observations(observations)
    # obs_df = scrapper.get_dataframe(save_csv=True)
    complete_dataset()

