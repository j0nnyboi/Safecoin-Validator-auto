#!/bin/bash
cd ~
NDEBUG=1 ~/Safecoin/target/release/safecoin-validator \
    --rpc-port 8328 \
    --identity ledger/validator-identity.json \
    --ledger ledger/validator-ledger \
    --vote-account ledger/validator-vote-account.json \
    --authorized-voter ledger/validator-identity.json \
    --expected-genesis-hash HfHmB9nh7EjpqoCL2DDZ559SJW4xN52gxheWPER782jW \
    --wal-recovery-mode skip_any_corrupted_record \
    --trusted-validator GYk4DZFFRm89GDjahqLS6HyXCRMD1bRNRiSYcLBy5RuG \
    --trusted-validator 4BRXtL6nEKDVJdYPEwgGCfAAvEHT4C4Sj5peQz8kHGZu \
    --trusted-validator 9tHQ1tEoBojYrh4J9G2YScdY4DZDDM5hh9PoEavzZrBH \
    --enable-rpc-transaction-history \
    --entrypoint entrypoint.mainnet-beta.safecoin.org:10015 \
    --entrypoint entrypoint2.mainnet-beta.safecoin.org:10015 \
    --entrypoint entrypoint3.mainnet-beta.safecoin.org:10015 \
