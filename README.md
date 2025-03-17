# 👽 Slayer Scripts 

🙌 Pentesting and OSINT scripts coded by myself.

## 🌐 Domain Finder

Requires a word list containing valid domains/subdomains and Shodan/Security Trails API Keys, performs a passive scan in order to gather more information about them. (Services running, Registrant...)
<p align="center">
    <img src="/assets/DomainFinder.png">
</p>

## 🔑 Key Finder
Performs searches based on a wordlist in order to look for password leaks in a 2021 database, ideal for Pentesting / Red Team exercises where we want to perform a quick check without paying (Limited to 100 results per query).
<p align="center">
    <img src="/assets/KeyFinder.png">
</p>

## 🔑 Pass Generator
Generates wordlists based on a organization name and year, current permutations:
```
python3 pass_generator.py -o mercadona -y 2023 2024 2025 > passwords.txt

✅ Org + Year: OrgYYYY, YYYYOrg, Org-YYYY, Org_YYYY
✅ Org + Common Numbers: OrgYYYY123, OrgYYYY789
✅ Org + Common Words: OrgAdminYYYY, OrgSecureYYYY, OrgPassYYYY (uppercase, lowercase and capitalized)
✅ Org + Seasons of the year (Spanish, can be easily modified): PrimaveraYYYY, OrgPrimaveraYYYY, PrimaveraOrgYYYY
✅ Org + Special Chars: OrgYYYY!, OrgYYYY@#*, OrgAdminYYYY!*
✅ Common Words (Hardcoded, can be easily modified): OrgadminYYYY!, OrgrootYYYY@#*, OrgAdminYYYYsupport!*
```
