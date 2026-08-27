"""
Phase 4 — Business positioning context.

This is the ONLY source of truth Fix Radar is allowed to treat as "known fact"
about OmniFit that isn't directly observed on the crawled pages. It exists so
the AIO/authority scoring and the AI Recommendation Simulator can check
observed page content against what the business actually claims to be,
without ever inventing credentials, affiliations, or claims that aren't here.

Do NOT add anything to this file that hasn't been explicitly confirmed by the
business owner. If a scoring rule needs a fact that isn't listed here, it
must either look for it on the page (observed evidence) or mark it UNKNOWN.
"""

BUSINESS_NAME = "OmniFit Performance"
BUSINESS_TYPE = "Premium personal training and executive health coaching"
PRIMARY_LOCATION = "San Diego, California"

SERVICE_AREAS = [
    "San Diego",
    "La Jolla",
    "Rancho Santa Fe",
    "Del Mar",
    "Solana Beach",
    "Encinitas",
    "Carlsbad",
    "Carmel Valley",
    "4S Ranch",
    "Santaluz",
    "Fairbanks Ranch",
]

SERVICES = [
    "Private personal training",
    "In-home personal training",
    "Virtual coaching",
    "Corrective exercise",
    "Strength training",
    "Nutrition coaching",
    "Executive health coaching",
]

TARGET_AUDIENCE = "Professionals 30+ who want measurable results"

METHODOLOGY_NAME = "Assess -> Correct -> Build -> Sustain"
METHODOLOGY_STAGES = ["Assess", "Correct", "Build", "Sustain"]

DIFFERENTIATORS = [
    "Measurable, individualized training",
    "Coordinated work with clinical professionals when appropriate",
]

# Explicitly UNKNOWN / not to be fabricated. Any AI or heuristic output that
# would need one of these must say "unknown" rather than invent a value.
UNKNOWN_FACTS = [
    "specific certifications or degrees held by trainers",
    "specific clinical partnerships or affiliations",
    "years in business",
    "number of clients served",
    "press mentions or media features",
    "professional-association memberships",
    "insurance or liability credentials",
    "pricing (must be read from the live rates page, never assumed)",
]


def business_context_summary() -> str:
    return (
        f"{BUSINESS_NAME} is a {BUSINESS_TYPE.lower()} business based in {PRIMARY_LOCATION}. "
        f"Services: {', '.join(SERVICES)}. Target audience: {TARGET_AUDIENCE}. "
        f"Methodology: {METHODOLOGY_NAME}. Differentiators: {', '.join(DIFFERENTIATORS)}. "
        "Any credential, affiliation, or outcome claim not directly observed on a crawled "
        "page must be treated as unknown, not assumed."
    )
