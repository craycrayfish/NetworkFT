"""Test covalent transaction parsing functions and node"""
import pandas as pd
import pytest

from networkft.nodes.covalent_txs import parse_covalent_txs, parse_tx_data


@pytest.fixture
def test_params():
    return [
        {"name": "from", "type": "address", "indexed": True, "value": "test_address_1"},
        {"name": "to", "type": "address", "indexed": True, "value": "test_address_2"},
        {"name": "value", "type": "uint256", "indexed": True, "value": 1234},
    ]


@pytest.fixture
def test_txs(test_params):
    return [
        {
            "block_signed_at": "2022-01-12T04:17:28Z",
            "block_height": 123456,
            "decoded": {"name": "Transfer", "params": test_params},
        }
    ]


@pytest.fixture
def test_collections(test_txs):
    return {
        "collection_1": {
            "id_1": {"updated_at": "2022-06-12T08:37:19.634079643Z", "txs": test_txs}
        },
        "collection_2": {
            "id_2": {"updated_at": "2022-06-12T08:37:19.634079643Z", "txs": test_txs}
        },
    }


@pytest.fixture
def tx_metadata():
    return ["block_signed_at"]


@pytest.fixture
def tx_params():
    return ["from", "to", "value"]


def test_parse_covalent_txs(test_collections, tx_metadata, tx_params):
    df = parse_covalent_txs(test_collections, tx_metadata, tx_params)

    expected_df = pd.DataFrame(
        {
            "collection": ["collection_1", "collection_2"],
            "token_id": ["id_1", "id_2"],
            "block_signed_at": ["2022-01-12T04:17:28Z"] * 2,
            "from": ["test_address_1"] * 2,
            "to": ["test_address_2"] * 2,
            "value": [1234] * 2,
            "name": ["Transfer"] * 2,
        }
    )

    pd.testing.assert_frame_equal(df, expected_df)


def test_parse_tx_data(test_txs, tx_metadata, tx_params):

    parsed_data = parse_tx_data(test_txs, tx_metadata, tx_params)

    expected_data = [
        {
            "block_signed_at": "2022-01-12T04:17:28Z",
            "from": "test_address_1",
            "to": "test_address_2",
            "value": 1234,
            "name": "Transfer",
        }
    ]

    assert parsed_data == expected_data
