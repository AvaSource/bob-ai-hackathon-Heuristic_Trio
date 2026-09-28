# Cyber Fraud Network Analyzer — Mock Test Dataset

**Dataset type:** SYNTHETIC TEST DATA

This dataset is generated for prototype/testing purposes. It is NOT a database of real people,
real phone numbers, real device identifiers, real bank accounts, or real transactions.

Its structure is inspired by:
- FTC Consumer Sentinel public fraud-report structure/categories
- I4C/NCRP public suspect-identifier categories
- IBM AMLSim transaction/account/entity schema

The records and relationships in these CSVs are synthetic. They are designed to test:
- entity/relationship extraction
- fraud-network visualization
- transaction-chain analysis
- common-device/SIM relationships
- call-network analysis
- suspicious/circular transaction detection
- investigation brief generation

## Files
- cases.csv
- persons.csv
- phones_sims.csv
- devices.csv
- bank_accounts.csv
- transactions.csv
- calls.csv
- locations.csv
- relationships.csv

## Important
Do not describe these records as real incidents in the hackathon submission. If the prototype
uses real public cases later, keep the real source/case identifiers in a separate source mapping
and clearly distinguish source-derived facts from synthetic test records.
