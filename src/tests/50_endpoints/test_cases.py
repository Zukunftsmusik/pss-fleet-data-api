from datetime import datetime

import pytest

from src.api.models.enums import ErrorCode
from src.tests import conftest


does_exist_collection_and_alliance = [
    # collection_exists, alliance_exists, expected_error_code
    pytest.param(True, False, ErrorCode.ALLIANCE_NOT_FOUND, id="alliance_missing"),
    pytest.param(False, True, ErrorCode.COLLECTION_NOT_FOUND, id="collection_missing"),
    pytest.param(False, False, ErrorCode.COLLECTION_NOT_FOUND, id="collection_and_alliance_missing"),
]
"""collection_exists, alliance_exists, expected_error_code"""


does_exist_collection_and_user = [
    # collection_exists, user_exists, expected_error_code
    pytest.param(True, False, ErrorCode.USER_NOT_FOUND, id="user_missing"),
    pytest.param(False, True, ErrorCode.COLLECTION_NOT_FOUND, id="collection_missing"),
    pytest.param(False, False, ErrorCode.COLLECTION_NOT_FOUND, id="collection_and_user_missing"),
]
"""collection_exists, user_exists, expected_error_code"""


invalid_ids = [
    # id
    pytest.param(0, id="id_invalid_as_int"),
    pytest.param("0", id="id_invalid_as_str"),
]
"""id"""


invalid_collection_and_alliance_ids = [
    # collection_is, alliance_id, expected_error_code
    pytest.param(0, 1, ErrorCode.PARAMETER_COLLECTION_ID_INVALID, id="collection_id_invalid"),
    pytest.param(1, 0, ErrorCode.PARAMETER_ALLIANCE_ID_INVALID, id="alliance_id_invalid"),
    pytest.param(0, 0, ErrorCode.PARAMETER_COLLECTION_ID_INVALID, id="collection_id_and_alliance_id_invalid"),
]
"""collection_is, alliance_id, expected_error_code"""


invalid_collection_and_user_ids = [
    # collection_is, user_id, expected_error_code
    pytest.param(0, 1, ErrorCode.PARAMETER_COLLECTION_ID_INVALID, id="collection_id_invalid"),
    pytest.param(1, 0, ErrorCode.PARAMETER_USER_ID_INVALID, id="user_id_invalid"),
    pytest.param(0, 0, ErrorCode.PARAMETER_COLLECTION_ID_INVALID, id="collection_id_and_user_id_invalid"),
]
"""collection_is, user_id, expected_error_code"""


invalid_filter_parameters = [
    # parameters, expected_error_code
    pytest.param({"fromDate": None}, ErrorCode.PARAMETER_FROM_DATE_INVALID, id="from_date_none"),
    pytest.param({"fromDate": "abc"}, ErrorCode.PARAMETER_FROM_DATE_INVALID, id="from_date_random_string"),
    pytest.param({"fromDate": "2016-13-01T00:00:00"}, ErrorCode.PARAMETER_FROM_DATE_INVALID, id="from_date_not_a_valid_date"),
    pytest.param({"fromDate": "2016-01-01T00:00:00"}, ErrorCode.PARAMETER_FROM_DATE_TOO_EARLY, id="from_date_too_early"),
    pytest.param({"toDate": None}, ErrorCode.PARAMETER_TO_DATE_INVALID, id="to_date_none"),
    pytest.param({"toDate": "abc"}, ErrorCode.PARAMETER_TO_DATE_INVALID, id="to_date_random_string"),
    pytest.param({"toDate": "2016-13-01T00:00:00"}, ErrorCode.PARAMETER_TO_DATE_INVALID, id="to_date_not_a_valid_date"),
    pytest.param(
        {"fromDate": "2020-02-01T00:00:00Z", "toDate": "2020-01-01T00:00:00Z"},
        ErrorCode.FROM_DATE_AFTER_TO_DATE,
        id="from_date_after_to_date",
    ),
    pytest.param({"interval": None}, ErrorCode.PARAMETER_INTERVAL_INVALID, id="interval_none"),
    pytest.param({"interval": "invalid"}, ErrorCode.PARAMETER_INTERVAL_INVALID, id="interval_invalid"),
    pytest.param({"desc": None}, ErrorCode.PARAMETER_DESC_INVALID, id="desc_none"),
    pytest.param({"skip": None}, ErrorCode.PARAMETER_SKIP_INVALID, id="skip_none"),
    pytest.param({"skip": -1}, ErrorCode.PARAMETER_SKIP_INVALID, id="skip_negative"),
    pytest.param({"take": None}, ErrorCode.PARAMETER_TAKE_INVALID, id="take_none"),
    pytest.param({"take": -1}, ErrorCode.PARAMETER_TAKE_INVALID, id="take_negative"),
    pytest.param({"take": 101}, ErrorCode.PARAMETER_TAKE_INVALID, id="take_too_big"),
]
"""parameters, expected_error_code"""


invalid_save_collection_methods = [
    # method
    pytest.param("DELETE", id="delete"),
    pytest.param("PATCH", id="patch"),
    pytest.param("PUT", id="put"),
]
"""method"""


def invalid_save_collection_payloads() -> list:
    """payload"""
    payload_1 = conftest._create_collection_create_9()
    payload_1.metadata = None

    payload_2 = conftest._create_collection_create_9()
    payload_2.fleets = None

    payload_3 = conftest._create_collection_create_9()
    payload_3.users = None

    payload_4 = conftest._create_collection_create_9()
    payload_4.metadata.timestamp = None

    payload_5 = conftest._create_collection_create_9()
    payload_5.metadata.timestamp = datetime(2000, 1, 1)

    payload_6 = conftest._create_collection_create_9()
    payload_6.fleets[0] = tuple(payload_6.fleets[0][:-1])

    payload_7 = conftest._create_collection_create_9()
    fleet_7: list = list(payload_7.fleets[0])
    fleet_7.append(0)
    payload_7.fleets[0] = tuple(fleet_7)

    payload_8 = conftest._create_collection_create_9()
    payload_8.users[0] = tuple(payload_6.users[0][:-1])

    payload_9 = conftest._create_collection_create_9()
    user_9: list = list(payload_9.users[0])
    user_9.append(0)
    payload_9.users[0] = tuple(user_9)

    payload_10 = conftest._create_collection_create_3()
    payload_11 = conftest._create_collection_create_8()

    payload_12 = conftest._create_collection_create_9()
    user_12 = list(payload_12.users[0])
    user_12[5] = 10  # AllianceMembership (encoded)
    payload_12.users[0] = tuple(user_12)

    payload_13 = conftest._create_collection_create_9()
    user_13 = list(payload_13.users[0])
    user_13[7] = -10  # LastLoginDate (encoded)
    payload_13.users[0] = tuple(user_13)

    payload_14 = conftest._create_collection_create_9()
    del payload_14.metadata

    payload_15 = conftest._create_collection_create_9()
    del payload_15.fleets

    payload_16 = conftest._create_collection_create_9()
    del payload_16.users

    return [
        pytest.param(payload_1, id="metadata_None"),
        pytest.param(payload_2, id="fleets_None"),
        pytest.param(payload_3, id="users_None"),
        pytest.param(payload_4, id="metadata_timestamp_None"),
        pytest.param(payload_5, id="metadata_timestamp_before_pss_start_date"),
        pytest.param(payload_6, id="fleet_too_short"),
        pytest.param(payload_7, id="fleet_too_long"),
        pytest.param(payload_8, id="user_too_short"),
        pytest.param(payload_9, id="user_too_long"),
        pytest.param(payload_10, id="schema_version_3"),
        pytest.param(payload_11, id="schema_version_8"),
        pytest.param(payload_12, id="user_invalid_alliance_membership"),
        pytest.param(payload_13, id="user_last_login_date_before_pss_start_date"),
        pytest.param(payload_14, id="metadata_deleted"),
        pytest.param(payload_15, id="fleets_deleted"),
        pytest.param(payload_16, id="users_deleted"),
    ]


invalid_upload_files = [
    # folder_path, file_name, expected_error_code
    pytest.param("src/tests/test_data", "invalid_json.txt", ErrorCode.INVALID_JSON_FORMAT, id="invalid_json_file"),
    pytest.param("src/tests/test_data", "some.txt", ErrorCode.INVALID_JSON_FORMAT, id="txt_file"),
    pytest.param(
        "src/tests/test_data",
        "upload_test_data_schema_4_says_schema_9.json",
        ErrorCode.SCHEMA_VERSION_MISMATCH,
        id="schema_version_and_schema_not_match",
    ),
]
"""folder_path, file_name, expected_error_code"""


root_api_keys = [
    # root_api_key
    pytest.param(None, id="none"),
    pytest.param("", id="empty"),
]
"""root_api_key"""


valid_ids = [
    # id
    pytest.param(1, id="id_valid"),
    pytest.param("1", id="id_valid_as_str"),
]
"""id"""


valid_collection_and_child_ids = [
    # collection_id, child_id
    pytest.param(1, 1, id="ids_valid_1"),
    pytest.param(1, "1", id="ids_valid_2"),
    pytest.param("1", 1, id="ids_valid_3"),
    pytest.param("1", "1", id="ids_valid_4"),
]
"""collection_id, child_id"""


valid_id_and_filter_parameters = [
    # id, parameters, headers
    pytest.param(1, {}, {}, id="no_params"),
    pytest.param(1, {}, {"Accept-Encoding": "gzip"}, id="no_params_accept_gzip"),
    pytest.param(1, {"fromDate": "2020-02-01T00:00:00Z", "toDate": "2020-03-01T00:00:00Z"}, {}, id="from_to_date_valid"),
    pytest.param(1, {"fromDate": "2020-02-01T00:00:00+06:00", "toDate": "2020-03-01T00:00:00Z"}, {}, id="from_to_date_valid_different_timezones"),
    pytest.param(1, {"fromDate": "2020-02-01T00:00:00", "toDate": "2020-03-01T00:00:00Z"}, {}, id="from_to_date_valid_one_without_timezone"),
    pytest.param(1, {"skip": 0, "take": 100}, {}, id="skip_take_valid_1"),
    pytest.param(1, {"skip": 5, "take": 5}, {}, id="skip_take_valid_2"),
]
"""id, parameters"""


valid_upload_files = [
    # schema_version, folder_path, file_name, collection_create_cls, to_db_convert_func
    pytest.param("src/tests/test_data", "upload_test_data_schema_2.json", id="schema_version_3_without_division_design_id"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_3.json", id="schema_version_3"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_4.json", id="schema_version_4"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_5.json", id="schema_version_5"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_6.json", id="schema_version_6"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_7.json", id="schema_version_7"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_8.json", id="schema_version_8"),
    pytest.param("src/tests/test_data", "upload_test_data_schema_9.json", id="schema_version_9"),
]
"""schema_version, folder_path, file_name, collection_create_cls, to_db_convert_func"""
