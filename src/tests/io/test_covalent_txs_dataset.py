"""Unit test for CovalentDataSet"""
import shutil

from networkft.io.covalent_txs_dataset import CovalentDataSet


def test_covalent_txs_dataset(raw_dataset):
    """Test that CovalentDataSet is able to read nft_txs json files
    correctly
    """
    dataset = CovalentDataSet(raw_dataset)
    txs = dataset._load()

    shutil.rmtree(raw_dataset)

    assert type(txs) is dict
    assert list(txs["test"]["0"]) == ["updated_at", "txs"]
