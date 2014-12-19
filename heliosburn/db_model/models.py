import datetime
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    update_at = Column(DateTime, default=datetime.datetime.utcnow)


class HttpRequest(Base):
    __tablename__ = "http_request"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    http_protocol = Column(String, nullable=False)
    method = Column(String, nullable=False)
    url = Column(String, nullable=False)
    response = Column(Integer, ForeignKey('http_response.id'), nullable=True)


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
    test_plan = Column(Integer, ForeignKey('test_plan.id'))
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)


class SessionTraffic(Base):
    __tablename__ = "session_traffic"

    id = Column(Integer, primary_key=True)
    session = Column(Integer, ForeignKey('session.id'), nullable=False)
    http_request = Column(Integer, ForeignKey('http_request.id'), nullable=False)


class TestPlan(Base):
    __tablename__ = "test_plan"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    latency_enabled = Column(Boolean, default=False)
    client_latency = Column(Integer)
    server_latency = Column(Integer)
    rules = relationship("Rule", backref="test_plan")


class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    rule_type = Column(String, nullable=False)  # "request" or "response"
    filters = relationship("Filter")
    actions = relationship("Action")
    test_plan = Column(Integer, ForeignKey('test_plan.id'), nullable=False)


# TODO: Should we have a unified Filter table or 2 (request and response)?
class Filter(Base):
    __tablename__ = "filter"

    id = Column(Integer, primary_key=True)
    method = Column(String)
    status_code = Column(String)
    url = Column(String)
    protocol = Column(String)
    rule = Column(Integer, ForeignKey('rule.id'), nullable=False)


class FilterHeaders(Base):
    __tablename__ = "filter_headers"

    id = Column(Integer, primary_key=True)
    filter = Column(Integer, ForeignKey('filter.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "request" or "response"
    rule = Column(Integer, ForeignKey('rule.id'), nullable=False)


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
    session = Column(Integer, ForeignKey('session.id'), nullable=False)
    rule = Column(Integer, ForeignKey('rule.id'), nullable=False)
    http_request = Column(Integer, ForeignKey('http_request.id'), nullable=False)


class Recording(Base):
    __tablename__ = "recording"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class RecordingTraffic(Base):
    __tablename__ = "recording_traffic"

    id = Column(Integer, primary_key=True)
    recording = Column(Integer, ForeignKey('recording.id'), nullable=False)
    http_request = Column(Integer, ForeignKey('http_request.id'), nullable=False)