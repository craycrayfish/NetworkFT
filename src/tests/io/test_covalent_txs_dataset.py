"""Unit test for CovalentDataSet"""

from pathlib import Path

from networkft.io.covalent_txs_dataset import CovalentDataSet

TEST_TXS_DIRECTORY = str(
    Path(__file__).resolve().parents[1] / "test_data" / "covalent_txs"
)


def test_covalent_txs_dataset():
    """Test that CovalentDataSet is able to read nft_txs json files correctly"""
    dataset = CovalentDataSet(TEST_TXS_DIRECTORY)
    txs = dataset._load()
    assert type(txs) is dict
    assert list(txs["test"]["0"]) == ["updated_at", "txs"]
