import pandas
import pandas as pd
import pytest
import os
import shutil
from src.data_pull import prepare_directory
from src.telemetry import Telemetry
import src.constants as cnst


class TestTelemetryClass:

    def has_key(self):
        """
        Test to ensure a user key has been added
        """
        assert 'api' in cnst.keys.keys()
        assert 'cookie' in cnst.keys.keys()
        assert 'token' in cnst.keys.keys()

    def test_url_and_parameters(self):
        """
        Tests that the url and parameters are correct when given an ID of a satellite.
        Reference: https://db.satnogs.org/api/schema/docs/#/telemetry/telemetry_retrieve
        NOTE: Examples in the reference use db-dev, not db.
        """

        iss_id = "XSKZ-5603-1870-9019-3066"
        expected_url = 'https://db.satnogs.org/api/telemetry/?sat_id=XSKZ-5603-1870-9019-3066'

        tm = Telemetry(max_pages=10)
        assert expected_url == tm.get_url_endpoint(iss_id)

    def test_telemetry_fetch(self):
        """
        Tests querying the telemetry endpoint of the satnogs DB when provided with a satellite ID.
        """
        iss_id = "XSKZ-5603-1870-9019-3066"
        iss_norad = 25544

        # clear the data directory then add the required subdirectories
        prepare_directory()
        assert not os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")

        tm = Telemetry(max_pages=1)
        tm_events = tm.fetch_telemetry_by_satellite(sat_id=iss_id)

        # should have around 25 events for the first response page
        assert len(tm_events) > 20

        first_event = tm_events[0]

        # verify the identifying contents of the first event of the first page
        assert first_event['sat_id'] == iss_id
        assert first_event['norad_cat_id'] == iss_norad

        # verify the tm events for the ISS were written to the disk
        assert os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")

    def test_multiple_fetch(self):
        """
        Tests querying the telemetry endpoint when given multiple sat_ids
        """

        # Satellite IDs to query with
        iss_id = "XSKZ-5603-1870-9019-3066"
        iss_norad = 25544
        humsat_d_id = "ISTU-1593-3487-2251-7574"
        humsat_d_norad = 39433
        cube_bel_1_id = "WMQB-0532-9164-6364-5821"
        cube_bel_1_norad = 43666

        # clear the data directory
        prepare_directory()
        # ensure the events are not saved to the disk
        assert not os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")
        assert not os.path.isfile(cnst.directories['tm_events'] + humsat_d_id + ".json")
        assert not os.path.isfile(cnst.directories['tm_events'] + cube_bel_1_id + ".json")

        tm = Telemetry(max_pages=1)
        tm.get_events_by_sat_id(sat_ids=[iss_id, humsat_d_id, cube_bel_1_id])
        # Verify the events were written to the disk
        assert os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")
        assert os.path.isfile(cnst.directories['tm_events'] + humsat_d_id + ".json")
        assert os.path.isfile(cnst.directories['tm_events'] + cube_bel_1_id + ".json")

        # iterate through the returned events and verify entries for each satellite
        found_iss = False
        found_humsat_d = False
        found_cube_bel_1 = False

        for event in tm.telemetry_events:

            if event['sat_id'] == iss_id and event['norad_cat_id'] == iss_norad:
                found_iss = True

            if event['sat_id'] == humsat_d_id and event['norad_cat_id'] == humsat_d_norad:
                found_humsat_d = True

            if event['sat_id'] == cube_bel_1_id and event['norad_cat_id'] == cube_bel_1_norad:
                found_cube_bel_1 = True

        assert found_iss
        assert found_humsat_d
        assert found_cube_bel_1

    def test_multi_process_fetch(self):
        """
        Tests querying the telemetry endpoint when given multiple sats using multiprocessing.
        """

        # Satellite IDs to query with
        iss_id = "XSKZ-5603-1870-9019-3066"
        iss_norad = 25544
        humsat_d_id = "ISTU-1593-3487-2251-7574"
        humsat_d_norad = 39433
        cube_bel_1_id = "WMQB-0532-9164-6364-5821"
        cube_bel_1_norad = 43666

        # clear the data directory
        prepare_directory()
        # ensure the events are not saved to the disk
        assert not os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")
        assert not os.path.isfile(cnst.directories['tm_events'] + humsat_d_id + ".json")
        assert not os.path.isfile(cnst.directories['tm_events'] + cube_bel_1_id + ".json")

        tm = Telemetry(max_pages=1)
        tm.multiprocess_fetch(sat_ids=[iss_id, humsat_d_id, cube_bel_1_id])
        # Verify the events were written to the disk
        assert os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")
        assert os.path.isfile(cnst.directories['tm_events'] + humsat_d_id + ".json")
        assert os.path.isfile(cnst.directories['tm_events'] + cube_bel_1_id + ".json")

        tm.get_archived_satellites_events()

        # iterate through the returned events and verify entries for each satellite
        found_iss = False
        found_humsat_d = False
        found_cube_bel_1 = False

        for event in tm.telemetry_events:

            if event['sat_id'] == iss_id and event['norad_cat_id'] == iss_norad:
                found_iss = True

            if event['sat_id'] == humsat_d_id and event['norad_cat_id'] == humsat_d_norad:
                found_humsat_d = True

            if event['sat_id'] == cube_bel_1_id and event['norad_cat_id'] == cube_bel_1_norad:
                found_cube_bel_1 = True

        assert found_iss
        assert found_humsat_d
        assert found_cube_bel_1

    def test_clear_archived_events(self):
        """
        Test that the function properly clears the retrieved telemetry events of earlier fetches.
        """

        prepare_directory()
        iss_id = "XSKZ-5603-1870-9019-3066"

        assert not os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")

        tm = Telemetry(max_pages=1)
        tm.fetch_telemetry_by_satellite(sat_id=iss_id)

        assert os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")

        tm.clear_archived_events()

        assert not os.path.isfile(cnst.directories['tm_events'] + iss_id + ".json")

    def test_get_events_df(self):
        """
        Test the creation of a pandas dataframe from the stored telemetry events
        """

        # Satellite IDs to query with
        iss_id = "XSKZ-5603-1870-9019-3066"
        humsat_d_id = "ISTU-1593-3487-2251-7574"
        cube_bel_1_id = "WMQB-0532-9164-6364-5821"

        # clear the data directory
        prepare_directory()

        tm = Telemetry(max_pages=1)
        tm.multiprocess_fetch(sat_ids=[iss_id, humsat_d_id, cube_bel_1_id])

        tm_df = tm.get_events_df()
        assert type(tm_df) == pandas.DataFrame

        assert iss_id in list(set(tm_df['sat_id'].values))
        assert humsat_d_id in list(set(tm_df['sat_id'].values))
        assert cube_bel_1_id in list(set(tm_df['sat_id'].values))


