from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String , ForeignKey , Boolean 
from ..config.db import Base

class Session(Base):

    __tablename__ = "sessions"

    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False, index=True
    )
    refresh_token_hash : Mapped[str] = mapped_column(String,nullable=False)
    is_revoked : Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)