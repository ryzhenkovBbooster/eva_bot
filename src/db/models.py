from sqlalchemy import Column, Integer, Text, BigInteger, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db.database import Base


class Auth(Base):
    __tablename__ = 'tg_auth'
    id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, unique=True)
    username = Column(Text, unique=False, nullable=False)
    access = Column(Boolean, unique=False, nullable=False)

    chats = relationship("Chat", backref="june_username", foreign_keys="Chat.username")
    chat_user_id = relationship("Chat", backref="chat_user_id", foreign_keys="Chat.user_chat_id")
    curator = relationship("CourseJune", backref="auth_curator", foreign_keys="CourseJune.curator")
    manager = relationship("CourseJune", backref="auth_manager", foreign_keys="CourseJune.manager")

    def __str__(self) -> str:
        return f"<USER: {self.user_id, self.username, self.access}>"

class Chat(Base):
    __tablename__ = 'tg_chat'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    chatname = Column(Text, unique=False, nullable=False)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    active_chat = Column(Boolean, unique=False, nullable=False, default=False)
    add_or_left = Column(Boolean, unique=False, nullable=False)
    user_chat_id = Column(BigInteger, ForeignKey("tg_auth.user_id"), nullable=True)
    username = Column(Text, ForeignKey("tg_auth.username"), nullable=False)


    chat = relationship("CourseJune", backref='course_chat')


class CourseJune(Base):
    __tablename__ = 'course_june'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    chat = Column(BigInteger, ForeignKey("tg_chat.chat_id"), nullable=True, unique=True)
    curator = Column(BigInteger, ForeignKey("tg_auth.user_id"), nullable=True)
    manager = Column(BigInteger, ForeignKey("tg_auth.user_id"), nullable=True)
    # junior = Column(BigInteger, ForeignKey("tg_auth.user_id"), nullable=True)
    create_email = Column(Text, unique=False, nullable=False)
    create_skillup = Column(Text, unique=False, nullable=False)
    create_practical_task = Column(Text, unique=False, nullable=False)
    create_personal_folder = Column(Text, unique=False, nullable=False)
    hr_tests = Column(Text, unique=False, nullable=False)
    rename_email = Column(Text, unique=False, nullable=False)
    user_folder = Column(Text, unique=False, nullable=False)
    personal_folder_link = Column(Text, unique=False, nullable=False)
    time_doctor = Column(Text, unique=False, nullable=False)
    name_june = Column(Text, unique=False, nullable=False)
    getcourse = Column(Text, unique=False, nullable=False)
    lastpass = Column(Text, unique=False, nullable=False)
    tonnus = Column(Text, unique=False, nullable=False)
    user_folder_id = Column(Text, unique=False, nullable=False)
    personal_folder_id = Column(Text, unique=False, nullable=False)
    rang = Column(Text, unique=False, nullable=False)
    ipo_folder_id = Column(Text, unique=False, nullable=False)
    finaly_stage = Column(Text, unique=False, nullable=False)
    test_completed = Column(Text, unique=False, nullable=False)
    check_practical_task = Column(Text, unique=False, nullable=False)
    evaluation_table = Column(Text, unique=False, nullable=False)
    finaly_course = Column(Text, unique=False, nullable=False)
    date_init = Column(Date, unique=False, nullable=False)










