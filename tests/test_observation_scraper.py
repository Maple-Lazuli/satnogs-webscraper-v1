import json
import os

import pandas

from src.data_pull import prepare_directory
from src.observation_scraper import ObservationScraper
import src.constants as cnst


class TestObservationScraperClass:

    def has_key(self):
        """
        Test to ensure a user key has been added
        """
        assert 'api' in cnst.keys.keys()
        assert 'cookie' in cnst.keys.keys()
        assert 'token' in cnst.keys.keys()

    def test_single_scrape(self):
        """
        Test scraping an observation from network.satnogs.org
        """

        # Clear the data directory and create needed directories
        prepare_directory()

        link_to_observation = "https://network.satnogs.org/observations/5025420/"

        observation_id = '5025420'
        satellite_norad = "42017"
        satellite_name = "NAYIF-1"

        scraper = ObservationScraper()
        scrape = scraper.scrape_observation(link_to_observation)

        assert observation_id == scrape['Observation_id']
        assert scrape['Satellite'].find(satellite_norad) != -1
        assert scrape['Satellite'].find(satellite_name) != -1
        # verify the waterfall image was downladed and verify the dimensions are two-dimensional
        assert os.path.isfile(scrape['Downloads']['waterfall_hash_name'])
        assert len(scrape['Downloads']['waterfall_shape']) == 2
        assert scrape['Downloads']['waterfall_shape'][0] > 0
        assert scrape['Downloads']['waterfall_shape'][1] > 0


    def test_multiple_scrape(self):
        """
        Test scraping an observation from network.satnogs.org when only given the ID
        """

        # Clear the data directory and create needed directories
        prepare_directory()

        observation1_id = '5025420'
        observation1_satellite_norad = "42017"
        observation1_satellite_name = "NAYIF-1"

        observation2_id = '44444'
        observation2_satellite_norad = "42761"
        observation2_satellite_name = "ZHUHAI-1 OVS-01"

        scraper = ObservationScraper()
        scraper.scrape_observations([5025420, 44444])

        #verify the observations were added to the internal list
        found_observation1 = False
        found_observation2 = False

        for observation in scraper.observations_list:
            if observation['Observation_id'] == observation1_id:
                if observation['Satellite'].find(observation1_satellite_norad) != -1:
                    if observation['Satellite'].find(observation1_satellite_name) != -1:
                        found_observation1 = True

            if observation['Observation_id'] == observation2_id:
                if observation['Satellite'].find(observation2_satellite_norad) != -1:
                    if observation['Satellite'].find(observation2_satellite_name) != -1:
                        found_observation2 = True

        assert found_observation1
        assert found_observation2

        # verify observations were written to the disk

        assert os.path.isfile(cnst.directories['observation_json'])

        with open(cnst.directories['observation_json'], 'r') as file_in:
            observations = json.load(file_in)

        #verify the observations were written to the disk
        found_observation1 = False
        found_observation2 = False

        for observation in observations:
            if observation['Observation_id'] == observation1_id:
                if observation['Satellite'].find(observation1_satellite_norad) != -1:
                    if observation['Satellite'].find(observation1_satellite_name) != -1:
                        found_observation1 = True

            if observation['Observation_id'] == observation2_id:
                if observation['Satellite'].find(observation2_satellite_norad) != -1:
                    if observation['Satellite'].find(observation2_satellite_name) != -1:
                        found_observation2 = True

        assert found_observation1
        assert found_observation2

    def test_multiprocess_scrape(self):
        """
        Test scraping an observation from network.satnogs.org when only given the ID using multiprocessing
        """

        # Clear the data directory and create needed directories
        prepare_directory()

        observation1_id = '5025420'
        observation1_satellite_norad = "42017"
        observation1_satellite_name = "NAYIF-1"

        observation2_id = '44444'
        observation2_satellite_norad = "42761"
        observation2_satellite_name = "ZHUHAI-1 OVS-01"

        scraper = ObservationScraper()
        scraper.multiprocess_scrape_observations([5025420, 44444])

        #verify the observations were added to the internal list
        found_observation1 = False
        found_observation2 = False

        for observation in scraper.observations_list:
            if observation['Observation_id'] == observation1_id:
                if observation['Satellite'].find(observation1_satellite_norad) != -1:
                    if observation['Satellite'].find(observation1_satellite_name) != -1:
                        found_observation1 = True

            if observation['Observation_id'] == observation2_id:
                if observation['Satellite'].find(observation2_satellite_norad) != -1:
                    if observation['Satellite'].find(observation2_satellite_name) != -1:
                        found_observation2 = True

        assert found_observation1
        assert found_observation2

        # verify observations were written to the disk

        assert os.path.isfile(cnst.directories['observation_json'])

        with open(cnst.directories['observation_json'], 'r') as file_in:
            observations = json.load(file_in)

        #verify the observations were written to the disk
        found_observation1 = False
        found_observation2 = False

        for observation in observations:
            if observation['Observation_id'] == observation1_id:
                if observation['Satellite'].find(observation1_satellite_norad) != -1:
                    if observation['Satellite'].find(observation1_satellite_name) != -1:
                        found_observation1 = True

            if observation['Observation_id'] == observation2_id:
                if observation['Satellite'].find(observation2_satellite_norad) != -1:
                    if observation['Satellite'].find(observation2_satellite_name) != -1:
                        found_observation2 = True

        assert found_observation1
        assert found_observation2


    def test_get_dataframe(self):

        # Clear the data directory and create needed directories
        prepare_directory()

        observation1_id = 5025420

        observation2_id = 44444

        scraper = ObservationScraper()
        scraper.multiprocess_scrape_observations([5025420, 44444])

        assert not os.path.isfile(cnst.directories['observation_csv'])

        obs_df = scraper.get_dataframe(load_from_disk_first=False, save_csv=True)

        assert os.path.isfile(cnst.directories['observation_csv'])
        assert type(obs_df) == pandas.DataFrame
        assert str(observation1_id) in list(obs_df['Observation_id'].values)
        assert str(observation2_id) in list(obs_df['Observation_id'].values)

        scraper2 = ObservationScraper()
        obs_df = scraper2.get_dataframe(load_from_disk_first=True, save_csv=False)

        assert os.path.isfile(cnst.directories['observation_csv'])
        assert type(obs_df) == pandas.DataFrame
        assert observation1_id in obs_df['Observation_id'].values
        assert observation2_id in obs_df['Observation_id'].values





