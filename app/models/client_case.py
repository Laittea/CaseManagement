from app.database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


class ClientCase(Base):
    """SQLAlchemy model for client cases in the database."""

    __tablename__ = "client_cases"

    client_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    employment_assistance = Column(Boolean)
    life_stabilization = Column(Boolean)
    retention_services = Column(Boolean)
    specialized_services = Column(Boolean)
    employment_related_financial_supports = Column(Boolean)
    employer_financial_supports = Column(Boolean)
    enhanced_referrals = Column(Boolean)
    success_rate = Column(
        Integer, CheckConstraint("success_rate >= 0 AND success_rate <= 100")
    )

    # Relationships
    client = relationship("Client", back_populates="cases")
    user = relationship("User", back_populates="cases")
