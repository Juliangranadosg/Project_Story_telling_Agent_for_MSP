import json
from datetime import datetime
from pyairtable import Api

from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME

def make_text(value):
    """
    Converts lists/dictionaries into Airtable-safe text.
    """

    if isinstance(value, str):
        return value

    return json.dumps(value, ensure_ascii=False, indent=2)

def get_airtable_table():
    try:
        from pyairtable import Api
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Missing dependency 'pyairtable'. Install project requirements with "
            "'pip install -r requirements.txt' before running the Airtable upload step."
        ) from exc

    api = Api(AIRTABLE_API_KEY)
    return api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)


def prepare_airtable_fields(content_package: dict):
    return {
        "Topic": make_text(content_package.get("topic", "")),
        "Content Angle": make_text(content_package.get("content_angle", "")),
        "Target Audience": make_text(content_package.get("target_audience", "")),
        "Source References": make_text(content_package.get("source_references", "")),
        "Expert Summary": make_text(content_package.get("expert_summary", "")),
        "Public Explanation": make_text(content_package.get("public_explanation", "")),
        "Instagram Caption": make_text(content_package.get("instagram_caption", "")),
        "LinkedIn Post": make_text(content_package.get("linkedin_post", "")),
        "Carousel Slides": make_text(content_package.get("carousel_slides", "")),
        "Reel Idea": make_text(content_package.get("reel_idea", "")),
        "Hooks": make_text(content_package.get("hooks", "")),
        "SEO Keywords": make_text(content_package.get("seo_keywords", "")),
        "Hashtags": make_text(content_package.get("hashtags", "")),
        "CTA": make_text(content_package.get("cta", "")),
        "Simple Exercise": make_text(content_package.get("simple_exercise", "")),
        "Status": "Needs Review",
        "Created Date": datetime.now().strftime("%Y-%m-%d"),
        "Reviewer Notes": ""
    }


def create_airtable_record(content_package: dict):
    table = get_airtable_table()
    fields = prepare_airtable_fields(content_package)

    record = table.create(fields)

    print("\nAirtable record created successfully.")
    print("Record ID:", record["id"])

    return record
