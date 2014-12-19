import datetime
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HttpRequest(Base):
    __tablename__ = "http_request"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    http_protocol = Column(String)
    method = Column(String)
    url = Column(String)
    response = Column(Integer, ForeignKey('http_response.id'), nullable=True)


class HttpRequestHeaders(Base):
    __tablename__ = "http_request_headers"

    id = Column(Integer, primary_key=True)
    request = Column(Integer, ForeignKey('http_request.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class HttpResponse(Base):
    __tablename__ = "http_response"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    http_protocol = Column(String)
    status_code = Column(Integer)
    status_description = Column(String)


class HttpResponseHeaders(Base):
    __tablename__ = "http_response_headers"

    id = Column(Integer, primary_key=True)
    response = Column(Integer, ForeignKey('http_response.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class HttpHeader(Base):
    __tablename__ = "http_header"

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    test_plan = Column(Integer, ForeignKey('test_plan.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TestPlan(Base):
    __tablename__ = "test_plan"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    latency_enabled = Column(Boolean)
    client_latency = Column(Integer)
    server_latency = Column(Integer)
    rules = relationship("Rule", backref="test_plan")


class SessionExecution(Base):
    __tablename__ = "session_execution"

    id = Column(Integer, primary_key=True)
    session = Column(Integer, ForeignKey('session.id'))
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)


class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rule_type = Column(String)  # "request" or "response"
    filters = relationship("Filter")
    actions = relationship("Action")
    test_plan = Column(Integer, ForeignKey('test_plan.id'))


# TODO: Should we have a unified Filter table or 2 (request and response)?
class Filter(Base):
    __tablename__ = "filter"

    id = Column(Integer, primary_key=True)
    method = Column(String, nullable=True)
    status_code = Column(String, nullable=True)
    url = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    rule = Column(Integer, ForeignKey('rule.id'))


class FilterHeaders(Base):
    __tablename__ = "filter_headers"

    id = Column(Integer, primary_key=True)
    filter = Column(Integer, ForeignKey('filter.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)
    type = Column(String)  # "request" or "response"
    rule = Column(Integer, ForeignKey('rule.id'))


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
    action = Column(Integer, ForeignKey('action.id'))
    header = Column(Integer, ForeignKey('http_header.id'))


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True)
    session_execution = Column(Integer, ForeignKey('session_execution.id'))
    rule = Column(Integer, ForeignKey('rule.id'))
    http_request = Column(Integer, ForeignKey('http_request.id'))
    created_at = Column(DateTime)