"""Demographic seeds for the V0.8 generator pilot.

Ten seeds covering states, castes, religions, literacy levels NOT in the
five hand-curated fixtures. Each is a fully-specified Demographic plus a
short occupation string. The generator turns each into a full Persona by
calling Gemini Pro and validating the result against the Pydantic schema.

V1: this hand-list becomes a stratified Census-2011 sampler (state ×
district-type × age × religion × caste × MPCE × education) producing
5,000 seeds. V2: 50,000.
"""
from __future__ import annotations

from dataclasses import dataclass

from akhada.persona_registry.schema import Demographic


@dataclass(frozen=True)
class PersonaSeed:
    seed_id: str  # "akh-p-gen-001" etc.
    demographic: Demographic
    notes: str  # optional flavour note for the generator prompt


SEEDS: list[PersonaSeed] = [
    PersonaSeed(
        seed_id="akh-p-gen-001",
        demographic=Demographic(
            state="Uttar Pradesh", district_type="urban", age_band="25-34",
            gender="male", religion="muslim", caste_cat="other_minority",
            mpce_quintile=4, education="postgraduate",
            occupation="software engineer at a domestic IT services firm",
            urban_rural="urban",
        ),
        notes="Lucknow-raised; first-generation college; reads English + Urdu.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-002",
        demographic=Demographic(
            state="Tamil Nadu", district_type="urban", age_band="35-44",
            gender="female", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="secondary",
            occupation="garment-factory line operator",
            urban_rural="urban",
        ),
        notes="Chennai outskirts; union member; functional literate in Tamil.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-003",
        demographic=Demographic(
            state="West Bengal", district_type="urban", age_band="65-74",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=4, education="doctorate",
            occupation="retired economics professor (Presidency / Calcutta U.)",
            urban_rural="urban",
        ),
        notes="Kolkata Bhadralok; CPI(M)-leaning in youth, sceptical now.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-004",
        demographic=Demographic(
            state="Gujarat", district_type="urban", age_band="25-34",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="graduate",
            occupation="chartered-accountant junior at a mid-size firm",
            urban_rural="urban",
        ),
        notes="Ahmedabad Patel family; observant; reads Gujarati press.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-005",
        demographic=Demographic(
            state="Rajasthan", district_type="rural", age_band="45-54",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="primary",
            occupation="small landowner (~5 acres, mustard + bajra)",
            urban_rural="rural",
        ),
        notes="Jodhpur district; Rajput; functional literate in Hindi.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-006",
        demographic=Demographic(
            state="Assam", district_type="rural", age_band="25-34",
            gender="male", religion="christian", caste_cat="st",
            mpce_quintile=1, education="secondary",
            occupation="tea-garden labourer (permanent worker)",
            urban_rural="rural",
        ),
        notes="Upper Assam; Adivasi descent; bilingual Sadri + Asamiya.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-007",
        demographic=Demographic(
            state="Telangana", district_type="rural", age_band="35-44",
            gender="female", religion="hindu", caste_cat="sc",
            mpce_quintile=2, education="graduate",
            occupation="Anganwadi worker (ICDS)",
            urban_rural="rural",
        ),
        notes="Mahbubnagar district; first SC graduate in her family.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-008",
        demographic=Demographic(
            state="Odisha", district_type="rural", age_band="55-64",
            gender="male", religion="hindu", caste_cat="st",
            mpce_quintile=1, education="primary",
            occupation="marine fisherman (mechanised boat crew)",
            urban_rural="rural",
        ),
        notes="Ganjam coast; Kondh-adjacent ST; oral-tradition literate.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-009",
        demographic=Demographic(
            state="Delhi", district_type="urban", age_band="25-34",
            gender="female", religion="sikh", caste_cat="general",
            mpce_quintile=4, education="postgraduate",
            occupation="political journalist at an English-language daily",
            urban_rural="urban",
        ),
        notes="Trilokpuri family; first cohort post-1984 trauma.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-010",
        demographic=Demographic(
            state="Haryana", district_type="rural", age_band="45-54",
            gender="male", religion="hindu", caste_cat="obc",
            mpce_quintile=3, education="secondary",
            occupation="dairy farmer (mid-size, ~25 cattle)",
            urban_rural="rural",
        ),
        notes="Sonipat district; Yadav; Khap-aware but pragmatic.",
    ),
    # ---- second-wave seeds (V0.9): 35 more covering remaining states ----
    PersonaSeed(
        seed_id="akh-p-gen-011",
        demographic=Demographic(
            state="Andhra Pradesh", district_type="rural", age_band="35-44",
            gender="male", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="secondary",
            occupation="weaver (handloom cooperative member)",
            urban_rural="rural",
        ),
        notes="Krishna district; Padmasali community; Pochampally weaving tradition.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-012",
        demographic=Demographic(
            state="Madhya Pradesh", district_type="rural", age_band="55-64",
            gender="female", religion="hindu", caste_cat="st",
            mpce_quintile=1, education="none",
            occupation="forest-produce gatherer (tendu leaves, mahua)",
            urban_rural="rural",
        ),
        notes="Mandla district; Gond Adivasi; matrilineal traditions; lived through 2002 forest rights agitation.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-013",
        demographic=Demographic(
            state="Jharkhand", district_type="rural", age_band="25-34",
            gender="male", religion="hindu", caste_cat="st",
            mpce_quintile=1, education="upper_primary",
            occupation="coal-mine contract worker (Coal India subsidiary)",
            urban_rural="rural",
        ),
        notes="Dhanbad-adjacent village; Santhal; cousins displaced by mine expansion.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-014",
        demographic=Demographic(
            state="Chhattisgarh", district_type="rural", age_band="45-54",
            gender="female", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="primary",
            occupation="paddy farmer (small landholder, ~2 acres)",
            urban_rural="rural",
        ),
        notes="Bilaspur district; Kurmi community; SHG-active; member of mahila kisan group.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-015",
        demographic=Demographic(
            state="Uttarakhand", district_type="rural", age_band="65-74",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=2, education="secondary",
            occupation="retired primary-school teacher; pension recipient",
            urban_rural="rural",
        ),
        notes="Tehri Garhwal hills; Brahmin; Chipko movement memory.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-016",
        demographic=Demographic(
            state="Himachal Pradesh", district_type="rural", age_band="35-44",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="graduate",
            occupation="apple orchard owner-operator (small holding, 4 hectares)",
            urban_rural="rural",
        ),
        notes="Kinnaur district; Rajput; first-gen graduate; works with HPMC mandi.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-017",
        demographic=Demographic(
            state="Goa", district_type="urban", age_band="25-34",
            gender="female", religion="christian", caste_cat="general",
            mpce_quintile=4, education="postgraduate",
            occupation="hospitality-industry HR manager (5-star resort)",
            urban_rural="urban",
        ),
        notes="Bardez taluka; Catholic Bamonn family; Konkani at home, English at work.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-018",
        demographic=Demographic(
            state="Manipur", district_type="urban", age_band="35-44",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="postgraduate",
            occupation="civil-society researcher (Imphal-based NGO on women's rights)",
            urban_rural="urban",
        ),
        notes="Meitei community; Imphal valley; Meira Paibi tradition shaped activism.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-019",
        demographic=Demographic(
            state="Mizoram", district_type="rural", age_band="45-54",
            gender="male", religion="christian", caste_cat="st",
            mpce_quintile=2, education="secondary",
            occupation="jhum (shifting) cultivator transitioning to oil-palm",
            urban_rural="rural",
        ),
        notes="Lunglei district; Mizo Presbyterian; church-mediated community life.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-020",
        demographic=Demographic(
            state="Meghalaya", district_type="rural", age_band="25-34",
            gender="female", religion="christian", caste_cat="st",
            mpce_quintile=2, education="graduate",
            occupation="village-council secretary (Khasi dorbar shnong)",
            urban_rural="rural",
        ),
        notes="East Khasi Hills; matrilineal Khasi; Catholic; English-medium college grad.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-021",
        demographic=Demographic(
            state="Nagaland", district_type="rural", age_band="55-64",
            gender="male", religion="christian", caste_cat="st",
            mpce_quintile=2, education="secondary",
            occupation="village headman (gaon bura) and small farmer",
            urban_rural="rural",
        ),
        notes="Kohima district; Angami Naga; Baptist church elder; Naga Hoho member.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-022",
        demographic=Demographic(
            state="Tripura", district_type="rural", age_band="35-44",
            gender="female", religion="hindu", caste_cat="st",
            mpce_quintile=2, education="upper_primary",
            occupation="rubber tapper (TRPC scheme beneficiary)",
            urban_rural="rural",
        ),
        notes="South Tripura; Tripuri; lived through 1980s ethnic insurgency in childhood.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-023",
        demographic=Demographic(
            state="Arunachal Pradesh", district_type="rural", age_band="25-34",
            gender="male", religion="buddhist", caste_cat="st",
            mpce_quintile=2, education="graduate",
            occupation="schoolteacher in a state-government high school",
            urban_rural="rural",
        ),
        notes="Tawang district; Monpa; Tibetan-Buddhist monastery-trained childhood.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-024",
        demographic=Demographic(
            state="Sikkim", district_type="urban", age_band="45-54",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=4, education="postgraduate",
            occupation="state-government department officer (rural development cadre)",
            urban_rural="urban",
        ),
        notes="Gangtok; Nepali-speaking; pro-organic-farming since the state mandate.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-025",
        demographic=Demographic(
            state="Jammu and Kashmir", district_type="rural", age_band="35-44",
            gender="male", religion="muslim", caste_cat="other_minority",
            mpce_quintile=2, education="graduate",
            occupation="apple orchard farmer (own 3 hectares)",
            urban_rural="rural",
        ),
        notes="Shopian district; Kashmiri-speaking; Article 370 abrogation and lockdown lived.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-026",
        demographic=Demographic(
            state="Chandigarh", district_type="urban", age_band="25-34",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=5, education="postgraduate",
            occupation="commercial-litigation lawyer at Punjab & Haryana High Court",
            urban_rural="urban",
        ),
        notes="Chandigarh-born; Khatri; bilingual Punjabi-Hindi; LSE-educated.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-027",
        demographic=Demographic(
            state="Puducherry", district_type="urban", age_band="55-64",
            gender="female", religion="christian", caste_cat="general",
            mpce_quintile=3, education="graduate",
            occupation="Aurobindo Ashram-affiliated guesthouse manager",
            urban_rural="urban",
        ),
        notes="French-Indian heritage family; Tamil + French; pre-Auroville Pondy resident.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-028",
        demographic=Demographic(
            state="Maharashtra", district_type="rural", age_band="35-44",
            gender="male", religion="buddhist", caste_cat="sc",
            mpce_quintile=2, education="graduate",
            occupation="agricultural extension worker; Ambedkarite organiser",
            urban_rural="rural",
        ),
        notes="Marathwada; Mahar/Buddhist (post-1956 conversion lineage); reads Ambedkar in Marathi.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-029",
        demographic=Demographic(
            state="Maharashtra", district_type="rural", age_band="25-34",
            gender="female", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="secondary",
            occupation="sugarcane cutter (seasonal migrant from Beed to Kolhapur)",
            urban_rural="rural",
        ),
        notes="Beed district; Vanjari; uterus-removal-as-debt-relief case-study cohort.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-030",
        demographic=Demographic(
            state="Uttar Pradesh", district_type="rural", age_band="55-64",
            gender="male", religion="hindu", caste_cat="sc",
            mpce_quintile=1, education="primary",
            occupation="landless agricultural labourer (MGNREGA + share-cropping)",
            urban_rural="rural",
        ),
        notes="Eastern UP (Azamgarh); Pasi caste; lived through 1990 Mandal protests.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-031",
        demographic=Demographic(
            state="Uttar Pradesh", district_type="urban", age_band="45-54",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=4, education="postgraduate",
            occupation="university-college professor of history (Lucknow University)",
            urban_rural="urban",
        ),
        notes="Kayastha; Lucknow Adab tradition; secular-liberal family.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-032",
        demographic=Demographic(
            state="Karnataka", district_type="urban", age_band="25-34",
            gender="male", religion="hindu", caste_cat="obc",
            mpce_quintile=4, education="postgraduate",
            occupation="machine-learning engineer at a global SaaS multinational",
            urban_rural="urban",
        ),
        notes="Bengaluru; Vokkaliga; first-gen tech wealth; reads Kannada and English.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-033",
        demographic=Demographic(
            state="Tamil Nadu", district_type="rural", age_band="65-74",
            gender="male", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="secondary",
            occupation="retired teacher; small landholder (~3 acres paddy)",
            urban_rural="rural",
        ),
        notes="Madurai district; Thevar; Periyarist-leaning; reads Murasoli.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-034",
        demographic=Demographic(
            state="Kerala", district_type="rural", age_band="55-64",
            gender="male", religion="muslim", caste_cat="other_minority",
            mpce_quintile=3, education="secondary",
            occupation="cardamom-plantation small owner; ex-Gulf returnee",
            urban_rural="rural",
        ),
        notes="Idukki district; Mappila Muslim; 22 years in Saudi before returning.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-035",
        demographic=Demographic(
            state="Bihar", district_type="urban", age_band="25-34",
            gender="female", religion="muslim", caste_cat="other_minority",
            mpce_quintile=3, education="graduate",
            occupation="public-health worker (state TB-elimination programme)",
            urban_rural="urban",
        ),
        notes="Patna; Sheikh Muslim; first woman in family to work outside home.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-036",
        demographic=Demographic(
            state="West Bengal", district_type="rural", age_band="35-44",
            gender="female", religion="hindu", caste_cat="sc",
            mpce_quintile=2, education="upper_primary",
            occupation="domestic worker (commutes daily to Kolkata)",
            urban_rural="rural",
        ),
        notes="South 24 Parganas; Namasudra; Trinamool-aware; lived through Aila cyclone 2009.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-037",
        demographic=Demographic(
            state="Gujarat", district_type="rural", age_band="55-64",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=3, education="primary",
            occupation="cotton farmer (Bt cotton; AMUL dairy-board member on side)",
            urban_rural="rural",
        ),
        notes="Saurashtra; Patidar; survived 2001 Bhuj earthquake.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-038",
        demographic=Demographic(
            state="Rajasthan", district_type="urban", age_band="25-34",
            gender="female", religion="muslim", caste_cat="other_minority",
            mpce_quintile=3, education="graduate",
            occupation="block-printing micro-entrepreneur (Sanganeri textiles)",
            urban_rural="urban",
        ),
        notes="Jaipur; Chhipa community; runs an Instagram-driven D2C business.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-039",
        demographic=Demographic(
            state="Odisha", district_type="urban", age_band="35-44",
            gender="female", religion="hindu", caste_cat="sc",
            mpce_quintile=3, education="postgraduate",
            occupation="state-cadre IAS officer (rural development department)",
            urban_rural="urban",
        ),
        notes="Bhubaneswar; first-gen administrator; Hindi belt-trained.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-040",
        demographic=Demographic(
            state="Telangana", district_type="urban", age_band="45-54",
            gender="male", religion="muslim", caste_cat="other_minority",
            mpce_quintile=4, education="postgraduate",
            occupation="electrical-engineering professor at JNTU Hyderabad",
            urban_rural="urban",
        ),
        notes="Old City Hyderabad; Hyderabadi-Urdu speaking; Aligarh-educated.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-041",
        demographic=Demographic(
            state="Punjab", district_type="rural", age_band="25-34",
            gender="female", religion="sikh", caste_cat="sc",
            mpce_quintile=2, education="graduate",
            occupation="village ASHA worker (state health-department contract)",
            urban_rural="rural",
        ),
        notes="Mansa district; Mazhabi Sikh; first graduate in family.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-042",
        demographic=Demographic(
            state="Delhi", district_type="urban", age_band="55-64",
            gender="male", religion="hindu", caste_cat="general",
            mpce_quintile=5, education="postgraduate",
            occupation="retired senior IAS officer (former Cabinet Secretariat)",
            urban_rural="urban",
        ),
        notes="South Delhi; UP migrant family; LBSNAA Mussoorie 1989 batch.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-043",
        demographic=Demographic(
            state="Maharashtra", district_type="urban", age_band="55-64",
            gender="female", religion="hindu", caste_cat="general",
            mpce_quintile=4, education="doctorate",
            occupation="senior fellow at a Pune-based public-policy think tank",
            urban_rural="urban",
        ),
        notes="Pune; Chitpavan Brahmin; centrist-liberal; FRBM-Act-era debater.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-044",
        demographic=Demographic(
            state="Bihar", district_type="rural", age_band="25-34",
            gender="male", religion="hindu", caste_cat="obc",
            mpce_quintile=2, education="graduate",
            occupation="mid-sized FPO (Farmer-Producer Organisation) office-bearer",
            urban_rural="rural",
        ),
        notes="Saran district; Mallah (EBC subdivision under OBC); UPSC aspirant turned FPO operator.",
    ),
    PersonaSeed(
        seed_id="akh-p-gen-045",
        demographic=Demographic(
            state="Karnataka", district_type="rural", age_band="55-64",
            gender="male", religion="muslim", caste_cat="other_minority",
            mpce_quintile=2, education="secondary",
            occupation="silk-weaving cooperative member; mulberry farmer",
            urban_rural="rural",
        ),
        notes="Mysuru district; Muslim weaving caste; Ramanagara silk-mandi participant.",
    ),
]
