# Problem Statement

## Background

Digital payment fraud in India — SIM-swap, OTP-vishing and UPI fraud — is dominated by organised rings such as the widely reported "Jamtara" ecosystem. A typical ring has one coordinator, several mule "collector" accounts that each receive money from many victims, rapid pass-through transfers that consolidate funds upward, and reuse of the same handsets (IMEIs) across multiple SIMs. Evidence for a single case arrives from several sources: bank transaction statements, telecom call/CDR logs, device registrations and free-text field or complaint reports (NCRP / I4C).

## The Problem

Investigators have to manually join these sources — usually in spreadsheets — to answer two questions: *who is running the network* and *which accounts are mules that must be frozen*. The unstructured intel (names, aliases, burner numbers, IMEIs buried in prose) is not machine-readable at all. By the time the links are worked out and paperwork is drafted, funds have typically been layered onward and cashed out.

## Who is Affected

- **Cyber-crime cell investigators and analysts** in state police / I4C units handling high volumes of fraud complaints.
- **Bank fraud / AML teams** who need to justify account liens with evidence of mule behaviour.
- Indirectly, **victims**, whose chance of recovery drops sharply with every hour of delay.

## Why It Matters

Recovery of defrauded money depends on freezing mule accounts quickly. Manual correlation takes hours to days per case, and the resulting FIR / case brief must still be written by hand. Faster, evidence-backed identification of the kingpin and mules directly increases the amount that can be frozen and the strength of the case.

## Why Existing Solutions Fall Short

- Spreadsheets and ad-hoc scripts do not show *network structure* — fan-in to mules, shared devices, and layering chains are invisible in row-level views.
- Commercial link-analysis tools are expensive, require manual data modelling, and do not read unstructured field reports.
- None of these produce the statutory case brief investigators actually need to file.
