import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('DATABASE_URL')
print('DATABASE_URL_SET', bool(url))
if url:
    engine = create_engine(url, echo=False)
    try:
        with engine.connect() as conn:
            result = conn.execute(text('select current_database(), current_user'))
            print(result.fetchone())
        print('SQLALCHEMY_OK')
    except Exception as exc:
        print(type(exc).__name__)
        print(str(exc))
