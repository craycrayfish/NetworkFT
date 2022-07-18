from datetime import datetime
import pytest
import pandas as pd
import json
import tempfile
import os
from pathlib import Path
from kedro.io import DataCatalog


TEST_DATA_DIR = Path().cwd() / "src/tests/test_data"
DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@pytest.fixture(scope="module")
def temp_dir():
    return tempfile.mkdtemp()


@pytest.fixture(scope="module")
def catalog_config(temp_dir):
    config = {
        "raw_covalent_txs": {
            "type": "networkft.io.covalent_txs_dataset.CovalentDataSet",
            "filepath": str(TEST_DATA_DIR / "covalent_txs/test_txs.json"),
            "load_args": {"suffix": "txs"}
        },
        "int_covalent_txs": {
            "type": "pandas.ParquetDataSet",
            "filepath": os.path.join(temp_dir, "int.parquet"),
            "save_args": {
                "compression": "GZIP",
                "index": "false"
            }
        }
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
            "convert_timestamp": ["block_signed_at"]
        }
    }
    return params


@pytest.fixture(scope="module")
def test_catalog(catalog_config, params):
    catalog_config.update(
        {
            f"params:{key}": value for key, value in params.items()
        }
    )
    io = DataCatalog.from_config(catalog_config)
    return io


@pytest.fixture(scope="module")
def raw_tx_path():
    return str(TEST_DATA_DIR/"covalent_txs/test_txs.json")


@pytest.fixture(scope="module")
def raw_tx(raw_tx_path):
    with open(raw_tx_path) as f:
        tx = json.load(f)
    return tx


@pytest.fixture(scope="module")
def df_tx():
    return pd.DataFrame(
        {
            "collection": ["test", "test"],
            "token_id": ["0", "1"],
            "block_signed_at": [
                datetime.strptime("2022-01-01T01:23:45Z", DT_FORMAT),
                datetime.strptime("2022-12-31T01:23:45Z", DT_FORMAT)
            ],
            "from": [
                "0xed5af388653567af2f388e6224dc7c4b3241c544",
                "0x0000000000000000000000000000000000000000",
            ],
            "to": [
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
            ],
            "value": [0, 1],
            "name": ["Transfer", "Test"],
        }
    )
