from datetime import datetime

from beanie import Document


class Timestamp(Document):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()