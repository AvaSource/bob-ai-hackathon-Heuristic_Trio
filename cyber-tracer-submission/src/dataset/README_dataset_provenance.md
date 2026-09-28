# Dataset Notes — Cyber Fraud Network Analyzer (Mock Test Data)

## What this is
A fully synthetic dataset (accounts.csv, devices.csv, transactions.csv,
call_logs.csv, unstructured_intel.txt) built to structurally mirror the
publicly reported Jamtara-pattern SIM-swap / OTP-vishing fraud network:
one coordinator, multiple mule "collector" accounts each receiving from
several victims, then consolidating funds upward, with device/SIM reuse
as the forensic signature. ground_truth.json records the intended
correct answer so you can test your extraction + hierarchy-detection
pipeline against it before demo day.

## Why it's synthetic (not a real case file)
Real FIRs, bank SARs and telecom CDRs are confidential investigation
records under the IT Act / CrPC and are not publicly releasable — using
real victim/accused data would also be a privacy and legal problem for
a hackathon submission. So the dataset is built from scratch, but every
structural feature (mule fan-in, rapid pass-through timing, shared
IMEI across SIMs, SIM-KYC/bank-KYC name mismatch, layering to
crypto/forex exit points) is modeled on patterns documented in public
sources below — not invented arbitrarily.

## Sources used to model the patterns (cite these if asked)
- National Cyber Crime Reporting Portal (NCRP) / I4C annual & quarterly
  reports on financial fraud typologies: https://cybercrime.gov.in
- Indian Cyber Crime Coordination Centre (I4C) press releases on mule
  account crackdowns and Jamtara-region SIM fraud operations:
  https://www.mha.gov.in/en/divisionofmha/cyber-and-information-security-ci-s-division
- RBI Annual Report / RBI "Report on Trend and Progress of Banking in
  India" — digital payment fraud statistics: https://rbi.org.in/Scripts/AnnualReportPublications.aspx
- NPCI UPI fraud/dispute statistics: https://www.npci.org.in/statistics
- News coverage of the real Jamtara SIM-swap fraud ecosystem (for the
  modus operandi, not for any individual's data): search "Jamtara
  cyber fraud" on The Economic Times, BBC News, Hindustan Times,
  Indian Express — these describe the mule-account + SIM-distribution
  structure this dataset is modeled on.

## Public datasets you can cite as methodological precedent
(structurally similar fraud-network data, used by researchers/Kaggle,
useful if a judge asks "has this kind of data been used before")
- PaySim — synthetic mobile money fraud simulator (Kaggle):
  https://www.kaggle.com/datasets/ealaxi/paysim1
- IEEE-CIS Fraud Detection dataset (Kaggle):
  https://www.kaggle.com/c/ieee-fraud-detection
- Elliptic Bitcoin transaction dataset (illicit network structure,
  useful for citing "graph-based fraud detection" prior art):
  https://www.kaggle.com/datasets/ellipticco/elliptic-data-set

## How to answer "where did you get this dataset?"
Say this, plainly, in the pitch or Q&A:
"This is synthetic test data we built ourselves — real case files
aren't public for legal and privacy reasons. We modeled the structure
on patterns documented in NCRP/I4C reports and public reporting on the
Jamtara fraud ecosystem: one coordinator account, multiple mule
accounts each collecting from several victims, shared devices across
SIMs, and layering to exchange/forex accounts before cash-out. The
extraction and hierarchy-detection logic is data-agnostic — it runs
identically on this mock data or on real anonymized case data, which
is what a deployed version would ingest from actual bank SARs and
telecom CDRs."
