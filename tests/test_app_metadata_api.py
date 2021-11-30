""""""
from os import getenv
from typing import Dict, List

import datetime as dt

import shimoku_api_python as shimoku


api_key: str = getenv('API_TOKEN')
business_id: str = getenv('BUSINESS_ID')
app_id: str = getenv('APP_ID')


config = {
    'access_token': api_key
}

s = shimoku.Client(config)


def test_get_app():
    app: Dict = s.app.get_app(
        business_id=business_id,
        app_id=app_id,
    )
    assert app


def test_update_app():
    """Set the updatedAt field of an App to '2000-01-01'
    Then revert the updatedAt to its original value
    """
    app: Dict = s.app.get_app(
        business_id=business_id,
        app_id=app_id,
    )
    old_val: str = app['createdAt']

    val: str = '2000-01-01'
    app_data: Dict = {
        'createdAt': val
    }
    s.app.update_app(
        business_id=business_id,
        app_id=app_id,
        app_data=app_data
    )

    app_updated: Dict = (
        s.app.get_app(
            business_id=business_id,
            app_id=app_id,
        )
    )

    assert app_updated['createdAt'] == val

    #########
    # Revert the change
    #########

    app_data: Dict = {
        'createdAt': old_val
    }
    s.app.update_app(
        business_id=business_id,
        app_id=app_id,
        app_data=app_data
    )

    app_updated: Dict = (
        s.app.get_app(
            business_id=business_id,
            app_id=app_id,
        )
    )

    assert app_updated['createdAt'] == old_val


def test_create_and_delete_app():
    test_app_type_id: str = getenv('APP_TYPE_TEST')
    app_id: str = (
        s.app.create_app(
            business_id=business_id,
            app_type_id=test_app_type_id,
        )
    )

    assert len(app_id) > 0

    app: Dict = s.app.get_app(
        business_id=business_id,
        app_id=app_id,
    )

    assert app['createdAt'] == dt.date.today()

    result: Dict = s.app.delete_app(
        business_id=business_id,
        app_id=app_id,
    )

    assert result


def test_get_app_reports():
    reports: List[Dict] = s.app.get_app_reports(
        business_id=business_id,
        app_id=app_id,
    )
    assert reports
    assert reports[0]


def test_get_app_report_ids():
    report_ids: List[str] = s.app.get_app_report_ids(
        business_id=business_id,
        app_id=app_id,
    )
    assert report_ids
    assert len(report_ids[0]) > 0
    assert isinstance(report_ids[0], str)


def test_get_app_path_names():
    path_names: List[str] = (
        s.app.get_app_path_names(
            business_id=business_id,
            app_id=app_id,
        )
    )
    assert path_names


# test_get_app()
# TODO pending:
test_update_app()
# TODO pending:
test_create_and_delete_app()
# test_get_app_reports()
# test_get_app_report_ids()
# test_get_app_path_names()
