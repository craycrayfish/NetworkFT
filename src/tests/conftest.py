import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest
from kedro.io import DataCatalog

from networkft.utils.reshape import flatten_dict
from tests.raw_covalent_txs import RAW_TXS

DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@pytest.fixture(scope="module")
def temp_dir():
    return tempfile.mkdtemp()


@pytest.fixture(scope="module")
def raw_dataset(temp_dir):
    json_path = os.path.join(temp_dir, "test_txs.json")
    with open(json_path, "w") as f:
        json.dump(RAW_TXS, f)
    return temp_dir


@pytest.fixture(scope="module")
def catalog_config(temp_dir, raw_dataset):
    config = {
        "raw_covalent_txs": {
            "type": "networkft.io.covalent_txs_dataset.CovalentDataSet",
            "filepath": raw_dataset,
            "load_args": {"suffix": "txs"},
        },
        "int_covalent_txs": {
            "type": "pandas.ParquetDataSet",
            "filepath": os.path.join(temp_dir, "int.parquet"),
            "save_args": {"compression": "GZIP", "index": "false"},
        },
    }
    return config


@pytest.fixture(scope="module")
def params():
    params = {
        "covalent": {
            "type": "kedro.io.AbstractDataSet",
            "tx_metadata": ["block_signed_at"],
            "tx_params": ["from", "to", "value"],
            "convert_wei": ["value"],
            "convert_timestamp": ["block_signed_at"],
            "rename_columns": {"block_signed_at": "timestamp"},
        }
    }
    return flatten_dict(params)


@pytest.fixture(scope="module")
def test_catalog(catalog_config, params):
    io = DataCatalog.from_config(catalog_config)
    io.add_feed_dict({f"params:{key}": value for key, value in params.items()})
    return io


@pytest.fixture(scope="module")
def df_tx():
    return pd.DataFrame(
        {
            "collection": ["test", "test"],
            "token_id": ["0", "1"],
            "timestamp": [
                datetime.strptime("2022-01-01T01:23:45Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-12-31T01:23:45Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
            ],
            "from": [
                "0xed5af388653567af2f388e6224dc7c4b3241c544",
                "0x0000000000000000000000000000000000000000",
            ],
            "to": [
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
            ],
            "value": [0.0, 1.0],
            "name": ["Transfer", "Test"],
        }
    )


@pytest.fixture(scope="module")
def df_tx_graph():
    return pd.DataFrame(
        {
            "timestamp": [0] * 7,
            "collection": ["A", "B", "C", "D", "A", "B", "D"],
            "entity": [1] * 4 + [2] * 3,
            "direction": ["in", "in", "out", "out", "in", "in", "out"],
            "value": [5, 10, 8, 14, 3, 5, 3],
        }
    )
