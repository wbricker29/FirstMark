## Structured: Mock_Guilds.csv
  (One row per guild member seat)

  - guild_member_id (string) – unique row id.
  - guild_name (string) – e.g., CTO Guild, CFO Guild.
  - exec_id (string) – stable id used across all tables.
  - exec_name (string).
  - company_name (string).
  - company_domain (string, optional) – acmeco.com.
  - role_title (string) – raw title (SVP Engineering, CFO).
  - function (enum) – CTO, CFO, CPO, etc.
  - seniority_level (enum) – C-Level, VP, Head, Director.
  - location (string) – city/region; can normalize to country.
  - company_stage (enum, optional) – Seed, A, B, C, Growth.
  - sector (enum, optional) – SaaS, Consumer, Fintech, etc.
  - is_portfolio_company (bool) – whether it’s FirstMark portfolio.

## Structured: Exec_Network.csv
  (One row per known executive in the wider network)

  - exec_id (string) – primary key; matches Mock_Guilds.csv.
  - exec_name (string).
  - current_title (string).
  - current_company_name (string).
  - current_company_domain (string, optional).
  - role_type (enum) – normalized function: CTO, CFO, CRO, etc.
  - primary_function (enum, optional) – broader grouping: Engineering, Finance, Revenue.
  - location (string).
  - company_stage (enum, optional) – current company stage.
  - sector (enum, optional).
  - recent_exit_experience (bool, optional) – IPO/M&A in last X years.
  - prior_companies (string, optional) – semi-colon separated list.
  - linkedin_url (string).
  - relationship_type (enum, optional) – Guild, Portfolio Exec, Partner 1st-degree, Event.
  - source_partner (string, optional) – which partner/guild list.


