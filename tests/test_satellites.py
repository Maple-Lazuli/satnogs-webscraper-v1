import pandas as pd
import pytest
import os
import shutil
from src.satellites import Satellites
import src.constants as cnst


class TestSatellitesClass:

    def has_key(self):
        assert 'api' in cnst.keys.keys()
        assert 'cookie' in cnst.keys.keys()
        assert 'token' in cnst.keys.keys()

    def test_fetch_pull(self):
        sats = Satellites()
        assert sats.response_json is None
        sats.fetch_json(write_json=False)
        assert sats.response_json is not None
        assert type(sats.response_json) == list
        assert len(sats.response_json) > 0

    def test_fetch_saving(self):
        # Clear the directory and make the satellites directory
        if os.path.exists(cnst.directories['data']):
            shutil.rmtree(cnst.directories['data'])
        os.makedirs(cnst.directories['data'])
        os.makedirs(cnst.directories['satellites'], exist_ok=True)

        # Verify the file does not exist
        assert not os.path.isfile(cnst.directories['satellites_json'])

        sats = Satellites()
        sats.fetch_json(write_json=True)

        # Verify the file was created after fetching
        assert os.path.isfile(cnst.directories['satellites_json'])

    def test_dataframe_creation(self):
        # Clear the directory and make the satellites directory
        if os.path.exists(cnst.directories['data']):
            shutil.rmtree(cnst.directories['data'])
        os.makedirs(cnst.directories['data'])
        os.makedirs(cnst.directories['satellites'], exist_ok=True)

        # Verify the files do not exist yet
        assert not os.path.isfile(cnst.directories['satellites_json'])
        assert not os.path.isfile(cnst.directories['satellites_csv'])

        sats = Satellites()
        sat_df = sats.get_dataframe(save_to_disk=False)
        assert os.path.isfile(cnst.directories['satellites_json'])
        assert not os.path.isfile(cnst.directories['satellites_csv'])
        assert type(sat_df) == pd.DataFrame
        assert sat_df.shape[0] > 0
        assert sat_df.shape[1] > 0

        sats.get_dataframe(save_to_disk=True)
        assert os.path.isfile(cnst.directories['satellites_csv'])


