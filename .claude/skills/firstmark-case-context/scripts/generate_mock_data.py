#!/usr/bin/env python3
"""
Generate mock data for FirstMark Talent Signal Agent case study.

This script creates realistic synthetic data matching the case requirements:
- mock_guilds.csv: FirstMark Guild members (CTO, CFO)
- exec_network.csv: Extended network contacts
- open_roles.csv: Portfolio company open positions
- executive_bios.json: Biographical text for executives
- job_descriptions/: Text files with role descriptions

Usage:
    python generate_mock_data.py --output ./data
"""

import csv
import json
import random
from pathlib import Path
from typing import List
import argparse


# Data for generating realistic mock executives
FIRST_NAMES = [
    "Sarah",
    "Marcus",
    "Elena",
    "David",
    "Priya",
    "James",
    "Maya",
    "Robert",
    "Aisha",
    "Michael",
    "Jennifer",
    "Alex",
    "Keisha",
    "Daniel",
    "Lisa",
]
LAST_NAMES = [
    "Chen",
    "Johnson",
    "Rodriguez",
    "Kim",
    "Patel",
    "Williams",
    "Thompson",
    "Garcia",
    "Anderson",
    "Lee",
    "Martinez",
    "Brown",
    "Taylor",
    "Davis",
]

# Real FirstMark portfolio companies (use some for realism)
CURRENT_COMPANIES = [
    "Stripe",
    "Plaid",
    "DataDog",
    "Ramp",
    "Astronomer",
    "Betterment",
    "Narmi",
    "Contentful",
    "TechCorp",
    "ScaleUp Inc",
    "CloudFlow",
    "DataWorks",
    "FinTech Solutions",
    "InfraCo",
    "DevTools Inc",
    "PaymentsCo",
]

PORTFOLIO_COMPANIES = ["AcmeCo", "DataFlow", "FinanceStream", "CloudScale", "PayNow"]

LOCATIONS = [
    "New York",
    "San Francisco",
    "Austin",
    "Boston",
    "Seattle",
    "Chicago",
    "Remote",
]

INDUSTRIES = [
    "FinTech",
    "Data Infrastructure",
    "SaaS",
    "Developer Tools",
    "Consumer",
    "B2B",
]

STAGES = ["Series A", "Series B", "Series C", "Series D"]


def generate_guilds_csv(output_dir: Path, num_cto: int = 10, num_cfo: int = 8):
    """Generate mock_guilds.csv with FirstMark Guild members."""

    filepath = output_dir / "mock_guilds.csv"

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "current_company",
                "current_title",
                "location",
                "seniority",
                "function",
                "linkedin_url",
                "guild",
            ],
        )
        writer.writeheader()

        # Generate CTO Guild members
        for i in range(num_cto):
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            writer.writerow(
                {
                    "name": name,
                    "current_company": random.choice(CURRENT_COMPANIES),
                    "current_title": random.choice(
                        ["CTO", "VP Engineering", "Head of Engineering"]
                    ),
                    "location": random.choice(LOCATIONS),
                    "seniority": random.choice(["VP", "C-Suite"]),
                    "function": "Engineering",
                    "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '')}",
                    "guild": "CTO Guild",
                }
            )

        # Generate CFO Guild members
        for i in range(num_cfo):
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            writer.writerow(
                {
                    "name": name,
                    "current_company": random.choice(CURRENT_COMPANIES),
                    "current_title": random.choice(
                        ["CFO", "VP Finance", "Head of Finance"]
                    ),
                    "location": random.choice(LOCATIONS),
                    "seniority": random.choice(["VP", "C-Suite"]),
                    "function": "Finance",
                    "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '')}",
                    "guild": "CFO Guild",
                }
            )

    print(f"✓ Created {filepath} ({num_cto + num_cfo} guild members)")


def generate_exec_network_csv(output_dir: Path, num_execs: int = 12):
    """Generate exec_network.csv with extended network contacts."""

    filepath = output_dir / "exec_network.csv"

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "current_title",
                "current_company",
                "role_type",
                "location",
                "linkedin_url",
                "connection_source",
            ],
        )
        writer.writeheader()

        sources = ["Partner Network", "Event Attendee", "LinkedIn", "Referral"]
        role_types = ["CTO", "CFO", "VP Engineering", "VP Finance"]

        for i in range(num_execs):
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            role_type = random.choice(role_types)

            writer.writerow(
                {
                    "name": name,
                    "current_title": role_type,
                    "current_company": random.choice(CURRENT_COMPANIES),
                    "role_type": "CTO"
                    if "CTO" in role_type or "Engineering" in role_type
                    else "CFO",
                    "location": random.choice(LOCATIONS),
                    "linkedin_url": f"https://linkedin.com/in/{name.lower().replace(' ', '')}",
                    "connection_source": random.choice(sources),
                }
            )

    print(f"✓ Created {filepath} ({num_execs} extended network contacts)")


def generate_open_roles_csv(output_dir: Path):
    """Generate open_roles.csv with portfolio company open positions."""

    filepath = output_dir / "open_roles.csv"

    roles = [
        {
            "role_id": "CFO_001",
            "company": "AcmeCo",
            "role_title": "Chief Financial Officer",
            "role_type": "CFO",
            "location": "New York",
            "stage": "Series B",
            "industry": "FinTech",
            "required_experience": "10+ years finance; Series B+ fundraising exp; team building",
            "nice_to_have": "Consumer fintech background; IPO experience",
        },
        {
            "role_id": "CTO_002",
            "company": "DataFlow",
            "role_title": "Chief Technology Officer",
            "role_type": "CTO",
            "location": "San Francisco",
            "stage": "Series C",
            "industry": "Data Infrastructure",
            "required_experience": "15+ years engineering; scaled 50+ eng teams; distributed systems",
            "nice_to_have": "Open source contributions; prior CTO experience",
        },
        {
            "role_id": "CFO_003",
            "company": "CloudScale",
            "role_title": "VP Finance (CFO track)",
            "role_type": "CFO",
            "location": "Austin",
            "stage": "Series A",
            "industry": "SaaS",
            "required_experience": "8+ years finance; startup experience; FP&A expertise",
            "nice_to_have": "SaaS metrics experience; prior fundraising",
        },
    ]

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=roles[0].keys())
        writer.writeheader()
        writer.writerows(roles)

    print(f"✓ Created {filepath} ({len(roles)} open roles)")


def generate_executive_bios_json(output_dir: Path, names: List[str]):
    """Generate executive_bios.json with biographical text."""

    filepath = output_dir / "executive_bios.json"

    bio_templates = {
        "CTO": [
            "{name} is {title} at {company}, where they lead a team of {team_size}+ engineers building {focus}. Prior to {company}, {name} was {prev_role} at {prev_company}, scaling the platform from {stage}. {education}. {achievement}.",
            "{name} serves as {title} at {company}, overseeing all technology and engineering operations. They joined {company} {timing} and have been instrumental in {accomplishment}. Previously, {name} held engineering leadership roles at {prev_company}. {education}.",
        ],
        "CFO": [
            "{name} serves as {title} at {company}, overseeing all financial operations and strategic planning. They joined {company} {timing} and helped raise {amount}M in funding. Previously, {name} was {prev_role} at {prev_company} during {phase}. {education}.",
            "{name} is {title} at {company}, leading all finance, accounting, and investor relations. Prior to this role, {name} spent {years} years at {prev_company} where they {accomplishment}. {education}. {achievement}.",
        ],
    }

    companies = CURRENT_COMPANIES
    prev_companies = [
        "Square",
        "Robinhood",
        "Coinbase",
        "Snowflake",
        "Databricks",
        "Airbnb",
    ]

    bios = []

    for name in names[:15]:  # Generate bios for subset of executives
        role_type = random.choice(["CTO", "CFO"])
        template = random.choice(bio_templates[role_type])

        if role_type == "CTO":
            bio_text = template.format(
                name=name.split()[0],
                title=random.choice(["CTO", "VP Engineering", "Head of Engineering"]),
                company=random.choice(companies),
                team_size=random.choice([50, 100, 200, 300]),
                focus=random.choice(
                    [
                        "payment infrastructure",
                        "data platforms",
                        "developer tools",
                        "cloud infrastructure",
                    ]
                ),
                prev_role=random.choice(
                    [
                        "Director of Engineering",
                        "Engineering Manager",
                        "Principal Engineer",
                    ]
                ),
                prev_company=random.choice(prev_companies),
                stage="Series B through IPO"
                if random.random() > 0.5
                else "Series A to Series C",
                education=random.choice(
                    [
                        "They hold a BS in Computer Science from Stanford",
                        "They earned an MS in Computer Engineering from MIT",
                        "They studied Computer Science at UC Berkeley",
                    ]
                ),
                timing="pre-Series B" if random.random() > 0.5 else "at Series A",
                accomplishment=random.choice(
                    [
                        "scaling the engineering team from 10 to 100+ engineers",
                        "architecting the company's core platform",
                        "leading the migration to microservices architecture",
                    ]
                ),
                achievement=random.choice(
                    [
                        f"{name.split()[0]} is passionate about building diverse engineering teams",
                        f"{name.split()[0]} has spoken at conferences like QCon and Strange Loop",
                        f"{name.split()[0]} has been recognized in Forbes 30 Under 30",
                    ]
                ),
            )
        else:  # CFO
            bio_text = template.format(
                name=name.split()[0],
                title=random.choice(["CFO", "VP Finance"]),
                company=random.choice(companies),
                timing="pre-Series B" if random.random() > 0.5 else "at Series A",
                amount=random.choice([25, 45, 75, 125, 425]),
                prev_role=random.choice(
                    ["VP Finance", "Director of FP&A", "Finance Manager"]
                ),
                prev_company=random.choice(prev_companies),
                phase=random.choice(
                    ["hypergrowth", "Series B and C fundraising", "the IPO process"]
                ),
                education=random.choice(
                    [
                        "They hold an MBA from Wharton and a BA in Economics from Yale",
                        "They earned a degree in Finance from Harvard Business School",
                        "They hold a BA in Economics from Stanford and an MBA from MIT Sloan",
                    ]
                ),
                years=random.choice([5, 7, 10, 12]),
                accomplishment=random.choice(
                    [
                        "led the Series B and C fundraising processes",
                        "built the finance organization from the ground up",
                        "established financial controls for rapid growth",
                    ]
                ),
                achievement=random.choice(
                    [
                        f"{name.split()[0]} started their career in investment banking at Goldman Sachs",
                        f"{name.split()[0]} is a certified CPA",
                        f"{name.split()[0]} has been featured in CFO Magazine",
                    ]
                ),
            )

        bios.append(
            {
                "name": name,
                "bio": bio_text,
                "source": "LinkedIn About + Press"
                if random.random() > 0.5
                else "Company bio + LinkedIn",
            }
        )

    with open(filepath, "w") as f:
        json.dump(bios, f, indent=2)

    print(f"✓ Created {filepath} ({len(bios)} executive bios)")


def generate_job_descriptions(output_dir: Path):
    """Generate job description text files."""

    jd_dir = output_dir / "job_descriptions"
    jd_dir.mkdir(exist_ok=True)

    job_descriptions = [
        {
            "filename": "CFO_AcmeCo.txt",
            "content": """Chief Financial Officer - AcmeCo

AcmeCo is a fast-growing FinTech startup revolutionizing consumer payments. We've raised $45M Series B and are scaling rapidly (150% YoY growth).

We're seeking an experienced CFO to:
- Lead all financial planning and analysis
- Manage Series C fundraising ($75M+ target)
- Build finance team from 3 to 15+ people
- Establish financial controls and reporting for growth stage
- Partner with CEO and board on strategic planning

Requirements:
- 10+ years progressive finance experience
- Experience as CFO or VP Finance at Series B+ startup
- Track record of successful fundraising (Series B, C, or later)
- Built finance teams from scratch
- FinTech or consumer tech background preferred
- Comfort with high-growth, fast-paced environment

Nice to Have:
- Consumer fintech experience
- IPO experience or preparation
- Investor relations experience

Compensation: $250-350K base + equity
Location: New York (hybrid, 3 days in office)
Reports to: CEO
""",
        },
        {
            "filename": "CTO_DataFlow.txt",
            "content": """Chief Technology Officer - DataFlow

DataFlow is building the next generation of data infrastructure for modern companies. Series C funded ($80M raised), we're powering data pipelines for 500+ companies.

We're looking for an experienced CTO to:
- Lead product and platform engineering (50+ engineers today, scaling to 150+)
- Define technical vision and architecture roadmap
- Build and scale distributed systems handling petabytes of data
- Establish engineering culture and best practices
- Partner with CEO and customers on product strategy

Requirements:
- 15+ years engineering experience with 5+ years in leadership
- Experience scaling engineering teams from 30 to 100+ people
- Deep expertise in distributed systems and data infrastructure
- Track record as CTO, VP Engineering, or equivalent at growth-stage company
- Experience with open source communities

Nice to Have:
- Prior CTO experience at infrastructure or developer tools company
- Published research or significant open source contributions
- Experience taking a product from Series B to Series D or beyond

Compensation: $300-400K base + significant equity
Location: San Francisco (flexible hybrid)
Reports to: CEO
""",
        },
        {
            "filename": "CFO_CloudScale.txt",
            "content": """VP Finance (CFO Track) - CloudScale

CloudScale is a fast-growing SaaS company helping businesses optimize cloud infrastructure costs. We've raised $15M Series A and are scaling from $5M to $25M ARR.

We're hiring our first finance leader to:
- Own all FP&A, budgeting, and forecasting
- Prepare for Series B fundraising (12-18 months)
- Build finance and accounting operations from scratch
- Implement financial systems and processes
- Partner with CEO and board on strategic planning

Requirements:
- 8+ years progressive finance experience
- Prior experience at high-growth startup (ideally Series A/B)
- Strong FP&A skills and SaaS metrics expertise
- Experience implementing financial systems and controls
- Fundraising experience (as participant or leader)

Nice to Have:
- Prior CFO or VP Finance experience
- SaaS or infrastructure software background
- Experience with unit economics and SaaS metrics
- Big 4 accounting or investment banking background

Compensation: $180-240K base + equity
Location: Austin, TX (hybrid)
Reports to: CEO
""",
        },
    ]

    for jd in job_descriptions:
        filepath = jd_dir / jd["filename"]
        filepath.write_text(jd["content"])

    print(f"✓ Created {len(job_descriptions)} job descriptions in {jd_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Generate mock data for FirstMark Talent Signal Agent case study"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./data"),
        help="Output directory for generated files (default: ./data)",
    )
    parser.add_argument(
        "--num-guild-cto",
        type=int,
        default=10,
        help="Number of CTO Guild members to generate (default: 10)",
    )
    parser.add_argument(
        "--num-guild-cfo",
        type=int,
        default=8,
        help="Number of CFO Guild members to generate (default: 8)",
    )
    parser.add_argument(
        "--num-network",
        type=int,
        default=12,
        help="Number of extended network contacts to generate (default: 12)",
    )

    args = parser.parse_args()

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    print(f"\nGenerating mock data in: {args.output}\n")

    # Generate all data files
    generate_guilds_csv(args.output, args.num_guild_cto, args.num_guild_cfo)
    generate_exec_network_csv(args.output, args.num_network)
    generate_open_roles_csv(args.output)

    # Collect all names for bio generation
    all_names = [
        f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        for _ in range(args.num_guild_cto + args.num_guild_cfo + args.num_network)
    ]

    generate_executive_bios_json(args.output, all_names)
    generate_job_descriptions(args.output)

    print(f"\n✓ All mock data generated successfully in {args.output}/\n")
    print("Files created:")
    print("  - mock_guilds.csv")
    print("  - exec_network.csv")
    print("  - open_roles.csv")
    print("  - executive_bios.json")
    print("  - job_descriptions/ (3 files)")
    print("\nYou can now use this data for your case study prototype.")


if __name__ == "__main__":
    main()
