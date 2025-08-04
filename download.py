# Copyright (c) 2025 Linh Pham
# wwdtm-audio-download is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Wait Wait Don't Tell Me Segment Audio Downloader Script."""

import datetime
import json
from pathlib import Path

import requests
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.types import RowType


def read_database_config(
    config_file: str = "config.json",
) -> dict[str, str | int | float | bool | None]:
    """Read database configuration settings from a JSON file."""
    file_path: Path = Path.cwd() / "config.json"
    with file_path.open(mode="r", encoding="utf-8") as config_file:
        config_dict: dict[str, str | int | float | bool | None] = json.load(config_file)
        if "database" in config_dict:
            return config_dict["database"]


def retrieve_show_dates(
    database_connection: MySQLConnection, start_year: int = 2006
) -> list[datetime.date]:
    """Retrieve all show dates as a list of date objects."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = (
        "SELECT showdate FROM ww_shows WHERE YEAR(showdate) >= %s ORDER BY showdate ASC"
    )
    cursor: MySQLCursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (start_year,))
    results: list[RowType] = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _dates: list[str] = []
    for row in results:
        _dates.append(row[0])

    database_connection.close()
    return _dates


def download_segments(
    show_date: datetime.date, destination_path: Path, file_name_prefix: str = "WWDTM"
) -> None:
    """Download audio segments for a specific show date."""
    url_prefix: str = "https://ondemand.npr.org/anon.npr-mp3/npr/waitwait"
    _year: str = f"{show_date.year:04d}"
    _month: str = f"{show_date.month:02d}"
    _day: str = f"{show_date.day:02d}"

    for segment in range(1, 11):
        audio_url: str = f"{url_prefix}/{_year}/{_month}/{_year}{_month}{_day}_waitwait_{segment:02d}.mp3"
        file_name: str = (
            f"{file_name_prefix} {_year}-{_month}-{_day} S{segment:02d}.mp3"
        )
        _year_path: Path = destination_path / _year
        if not _year_path.exists():
            _year_path.mkdir()

        response: requests.Response = requests.get(url=audio_url, timeout=10)
        if response.ok:
            _path: Path = _year_path / file_name
            with _path.open(mode="wb") as _file:
                _file.write(response.content)


_config: dict[str, str | int | float | bool | None] = read_database_config()
if _config:
    _database_connection: MySQLConnection = connect(**_config)
    _dates: list[datetime.date] = retrieve_show_dates(
        database_connection=_database_connection
    )

    if _dates:
        for _date in _dates:
            download_segments(show_date=_date, destination_path=Path("output"))
