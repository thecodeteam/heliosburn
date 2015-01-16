### SQLAlchemy models, NOT django model definitions
import datetime
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    update_at = Column(DateTime, default=datetime.datetime.utcnow)
    sessions = relationship("Session", backref="user")


class HttpRequest(Base):
    __tablename__ = "http_request"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    http_protocol = Column(String, nullable=False)
    method = Column(String, nullable=False)
    url = Column(String, nullable=False)
    response_id = Column(Integer, ForeignKey('http_response.id'), nullable=True)


class HttpRequestHeaders(Base):
    __tablename__ = "http_request_headers"

    id = Column(Integer, primary_key=True)
    request = Column(Integer, ForeignKey('http_request.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class HttpResponse(Base):
    __tablename__ = "http_response"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    http_protocol = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    status_description = Column(String, nullable=False)


class HttpResponseHeaders(Base):
    __tablename__ = "http_response_headers"

    id = Column(Integer, primary_key=True)
    response = Column(Integer, ForeignKey('http_response.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class HttpHeader(Base):
    __tablename__ = "http_header"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String)


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    testplan = relationship("TestPlan", uselist=False, backref="session")
    testplan_id = Column(Integer, ForeignKey('testplan.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)
    session_executions = relationship("SessionExecution", backref="session")


class SessionExecution(Base):
    __tablename__ = "session_execution"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    session_traffic = relationship("SessionTraffic", backref="session_execution")
    matches = relationship("Match", backref="session_execution")


class SessionTraffic(Base):
    __tablename__ = "session_traffic"

    id = Column(Integer, primary_key=True)
    session_execution_id = Column(Integer, ForeignKey('session_execution.id'), nullable=False)
    http_request_id = Column(Integer, ForeignKey('http_request.id'), nullable=False)


class TestPlan(Base):
    __tablename__ = "testplan"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    latency_enabled = Column(Boolean, default=False)
    client_latency = Column(Integer)
    server_latency = Column(Integer)
    rules = relationship("Rule", backref="testplan")


class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    rule_type = Column(String, nullable=False)  # "request" or "response"
    filter = relationship("Filter", uselist=False, backref="rule")
    action = relationship("Action", uselist=False, backref="rule")
    testplan_id = Column(Integer, ForeignKey('testplan.id'), nullable=False)


# TODO: Should we have a unified Filter table or 2 (request and response)?
class Filter(Base):
    __tablename__ = "filter"

    id = Column(Integer, primary_key=True)
    method = Column(String)
    status_code = Column(String)
    url = Column(String)
    protocol = Column(String)
    rule_id = Column(Integer, ForeignKey('rule.id'), nullable=False)
    filter_headers = relationship("FilterHeaders", backref="filter")


class FilterHeaders(Base):
    __tablename__ = "filter_headers"

    id = Column(Integer, primary_key=True)
    filter_id= Column(Integer, ForeignKey('filter.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "request" or "response"
    rule_id = Column(Integer, ForeignKey('rule.id'), nullable=False)


class ActionResponse(Action):
    __tablename__ = "action_response"

    id = Column(Integer, ForeignKey('action.id'), primary_key=True)
    http_protocol = Column(String)
    status_code = Column(Integer)
    status_description = Column(String)
    payload = Column(String)


class ActionRequest(Action):
    __tablename__ = "action_request"

    id = Column(Integer, ForeignKey('action.id'), primary_key=True)
    http_protocol = Column(String)
    method = Column(String)
    url = Column(String)
    payload = Column(String)


class ActionHeaders(Base):
    __tablename__ = "action_headers"

    id = Column(Integer, primary_key=True)
    action = Column(Integer, ForeignKey('action.id'), nullable=False)
    header = Column(Integer, ForeignKey('http_header.id'), nullable=False)


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True)
    session_execution_id = Column(Integer, ForeignKey('session_execution.id'), nullable=False)
    rule_id = Column(Integer, ForeignKey('rule.id'), nullable=False)
    http_request = Column(Integer, ForeignKey('http_request.id'), nullable=False)


class Recording(Base):
    __tablename__ = "recording"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    session_traffic = relationship("RecordingTraffic", backref="recording")


class RecordingTraffic(Base):
    __tablename__ = "recording_traffic"

    id = Column(Integer, primary_key=True)
    recording_id = Column(Integer, ForeignKey('recording.id'), nullable=False)
    http_request = Column(Integer, ForeignKey('http_request.id'), nullable=False)


def init_db():
    """Returns dbsession"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm.session import sessionmaker

    dbsession = scoped_session(sessionmaker())
    engine = create_engine("postgresql://postgres:postgres@localhost/heliosburn")
    dbsession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return dbsession
