from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    DateTime,
    Text,
    JSON,
    Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .base import Base


class UserRole(str, enum.Enum):
    EXPERT = "expert"
    ADMIN = "admin"


class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    DONE = "done"
    REGENERATING = "regenerating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


# Association table for the many-to-many relationship between ReviewLog and RejectionReason
review_log_rejection_reason_association = Table(
    'review_log_rejection_reason_association', Base.metadata,
    Column('review_log_id', Integer, ForeignKey('review_logs.id'), primary_key=True),
    Column('rejection_reason_id', Integer, ForeignKey('rejection_reasons.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EXPERT, nullable=False)

    review_logs = relationship("ReviewLog", back_populates="reviewer")


class RawDataset(Base):
    __tablename__ = "raw_dataset"
    id = Column(Integer, primary_key=True, index=True)
    
    instruction = Column(Text, nullable=True)
    input = Column(Text, nullable=True)
    output = Column(Text, nullable=False)
    system = Column(Text, nullable=True)
    history = Column(JSON, default=[])
    source = Column(JSON, default=[])
    model_name = Column(String, nullable=True)

    review_status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)
    accept_count = Column(Integer, default=0)
    reject_count = Column(Integer, default=0)
    
    review_logs = relationship("ReviewLog", back_populates="dataset", cascade="all, delete-orphan")


class FinalDataset(Base):
    __tablename__ = "final_dataset"
    id = Column(Integer, primary_key=True, index=True)
    original_input = Column(Text, nullable=False)
    final_output = Column(Text, nullable=False)
    raw_dataset_id = Column(Integer, ForeignKey("raw_dataset.id"))
    model_name = Column(String, nullable=True)


class ReviewLog(Base):
    __tablename__ = "review_logs"
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("raw_dataset.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    result = Column(Enum("ACCEPT", "REJECT", name="review_result_enum"), nullable=False)
    comment = Column(Text) # Renamed from detailed_reason, used for custom comments
    model_name = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    reviewer = relationship("User", back_populates="review_logs")
    dataset = relationship("RawDataset", back_populates="review_logs")
    
    # Many-to-many relationship with RejectionReason
    rejection_reasons = relationship(
        "RejectionReason",
        secondary=review_log_rejection_reason_association,
        back_populates="review_logs"
    )


class RejectionReason(Base):
    __tablename__ = "rejection_reasons"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)

    review_logs = relationship(
        "ReviewLog",
        secondary=review_log_rejection_reason_association,
        back_populates="rejection_reasons"
    )


class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(JSON, nullable=False)


class LegalArticle(Base):
    __tablename__ = "legal_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    number = Column(String, nullable=False)
    content = Column(Text, nullable=False)
