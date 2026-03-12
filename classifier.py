KEYWORDS = {
    "Technology": ["technology", "software", "data", "ai", "digital", "cyber", "it ", "engineering", "developer", "computing"],
    "Engineering": ["engineering", "mechanical", "electrical", "civil", "structural", "aerospace", "chemical"],
    "Finance": ["finance", "financial", "banking", "investment", "markets", "trading", "risk", "wealth", "consumer", "lending"],
    "Accounting/Audit": ["audit", "accounting", "tax", "assurance", "actuarial"],
    "Legal": ["law", "legal", "solicitor", "barrister", "compliance"],
    "Human Resources": ["human resources", "hr", "people", "talent", "recruitment", "organisational", "psychology"],
    "Consulting": ["consulting", "consultant", "advisory", "strategy"],
    "Marketing": ["marketing", "brand", "communications", "digital marketing", "media", "advertising"],
    "Science": ["science", "research", "laboratory", "biology", "chemistry", "physics", "clinical"],
    "Government/Public Sector": ["government", "public sector", "policy", "intelligence", "civil service", "ministry", "security"],
    "Media": ["media", "journalism", "publishing", "broadcasting", "content", "editorial"],
    "Business": ["business"]
}

def classifier(scheme_name):
    industry = []
    
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in str(scheme_name)  .lower():
                industry.append(category)
                break
    if not industry:
        return "Unknown"
    
    return industry


    
