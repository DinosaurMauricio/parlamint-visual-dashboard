DATA_PATH = "assets/parlamint_preprocessed.parquet"
TEXT_DATA_PATH = "assets/parlamint_full_texts.parquet"
SPACY_PREPROCESSED = "assets/preprocessed_texts.parquet"
LANG_MODEL = "en_core_web_sm"
FILTERS = [
    ("Years", "year"),
    ("Topics", "Topic"),
    ("Orientations", "Party_orientation"),
]
