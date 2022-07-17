import pytest
import pandas as pd
import json
import tempfile
import os
from pathlib import Path
from web3 import Web3
from kedro.io import DataCatalog
from kedro.config import ConfigLoader
from kedro.framework.project import settings

TEST_DATA_DIR = Path().cwd() / "src/tests/test_data"


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
def conf_loader():
    conf_path = str(Path.cwd() / settings.CONF_SOURCE)
    conf_loader = ConfigLoader(conf_source=conf_path, env="local")
    return conf_loader


@pytest.fixture(scope="module")
def test_catalog(catalog_config):
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
            "block_signed_at": ["2022-01-01T01:23:45Z", "2022-12-31T01:23:45Z"],
            "from": [
                "0xed5af388653567af2f388e6224dc7c4b3241c544",
                "0x0000000000000000000000000000000000000000",
            ],
            "to": [
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
            ],
            "value": [None, Web3.toWei(1, "ether")],
            "name": ["Transfer", "Test"],
        }
    )

