from sqlalchemy import create_engine, Column, String, JSON, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Connection URL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/medical_notes"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class for ORM models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Notes ORM Model
class Notes(Base):
    __tablename__ = "notes"

    patient_id = Column(String, primary_key=True, nullable=False)
    doctor_id = Column(String, primary_key=True, nullable=False)
    transcription = Column(String, nullable=False)
    transcription_summary = Column(String, nullable=False)
    analysis_summary = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


def get_notes_from_db(patient_id: str, doctor_id: str):
    """Fetches notes from PostgreSQL based on patient_id and doctor_id."""
    session = SessionLocal()
    try:
        note = session.query(Notes).filter_by(
            patient_id=patient_id,
            doctor_id=doctor_id
        ).first()

        if note:
            return {
                "transcription_summary": note.transcription_summary,
                "patient_id": note.patient_id,
                "doctor_id": note.doctor_id,
                "transcription": note.transcription,
                "analysis_summary": note.analysis_summary
            }
        return None  # No record found
    except Exception as e:
        print(f"❌ Error retrieving notes: {e}")
        return None
    finally:
        session.close()

def save_notes_to_db(patient_id, doctor_id, transcription, nlp_results, transcription_summary):
    """Saves generated notes to PostgreSQL."""
    session = SessionLocal()
    try:
        new_note = Notes(
            patient_id=patient_id,
            doctor_id=doctor_id,
            transcription_summary=transcription_summary,
            transcription=transcription,
            analysis_summary=nlp_results
        )
        session.add(new_note)
        session.commit()
        print(f"Saved notes for Patient {patient_id} - Doctor {doctor_id}")
    except Exception as e:
        session.rollback()
        print(f"Error saving notes: {e}")
    finally:
        session.close()

# Create table if it doesn't exist
Base.metadata.create_all(engine)
