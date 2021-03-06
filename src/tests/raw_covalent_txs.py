RAW_TXS = {
    "0": {
        "updated_at": "2022-01-01T08:37:19.634079643Z",
        "txs": [
            {
                "block_signed_at": "2022-01-01T01:23:45Z",
                "block_height": 13988541,
                "tx_offset": 224,
                "log_offset": 359,
                "tx_hash": "0xc208fdb2f133bda64522fececd6518a565aaa6e8801b0a776f2f93c922fe9420",
                "raw_log_topics": [
                    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                    "0x0000000000000000000000000000000000000000000000000000000000000000",
                    "0x000000000000000000000000d45058bf25bbd8f586124c479d384c8c708ce23a",
                    "0x00000000000000000000000000000000000000000000000000000000000000c7",
                ],
                "sender_contract_decimals": None,
                "sender_name": None,
                "sender_contract_ticker_symbol": None,
                "sender_address": "0xed5af388653567af2f388e6224dc7c4b3241c544",
                "sender_address_label": None,
                "sender_logo_url": None,
                "raw_log_data": None,
                "decoded": {
                    "name": "Transfer",
                    "signature": "Transfer(indexed address from, indexed address to, uint256 value)",
                    "params": [
                        {
                            "name": "from",
                            "type": "address",
                            "indexed": True,
                            "decoded": True,
                            "value": "0xed5af388653567af2f388e6224dc7c4b3241c544",
                        },
                        {
                            "name": "to",
                            "type": "address",
                            "indexed": True,
                            "decoded": True,
                            "value": "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
                        },
                        {
                            "name": "value",
                            "type": "uint256",
                            "indexed": False,
                            "decoded": False,
                            "value": None,
                        },
                    ],
                },
            }
        ],
    },
    "1": {
        "updated_at": "2022-01-01T08:37:19.634079643Z",
        "txs": [
            {
                "block_signed_at": "2022-12-31T01:23:45Z",
                "block_height": 13988541,
                "tx_offset": 224,
                "log_offset": 359,
                "tx_hash": "0xc208fdb2f133bda64522fececd6518a565aaa6e8801b0a776f2f93c922fe9420",
                "raw_log_topics": [
                    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                    "0x0000000000000000000000000000000000000000000000000000000000000000",
                    "0x000000000000000000000000d45058bf25bbd8f586124c479d384c8c708ce23a",
                    "0x00000000000000000000000000000000000000000000000000000000000000c7",
                ],
                "sender_contract_decimals": None,
                "sender_name": None,
                "sender_contract_ticker_symbol": None,
                "sender_address": "0xed5af388653567af2f388e6224dc7c4b3241c544",
                "sender_address_label": None,
                "sender_logo_url": None,
                "raw_log_data": None,
                "decoded": {
                    "name": "Test",
                    "signature": "Test(indexed address from, indexed address to, uint256 value)",
                    "params": [
                        {
                            "name": "from",
                            "type": "address",
                            "indexed": True,
                            "decoded": True,
                            "value": "0x0000000000000000000000000000000000000000",
                        },
                        {
                            "name": "to",
                            "type": "address",
                            "indexed": True,
                            "decoded": True,
                            "value": "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
                        },
                        {
                            "name": "value",
                            "type": "uint256",
                            "indexed": False,
                            "decoded": False,
                            "value": "1000000000000000000",
                        },
                    ],
                },
            }
        ],
    },
}
