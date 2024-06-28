from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class TechnologyStack(Enum):
    JAVASCRIPT = "JavaScript"
    PYTHON = "Python"
    JAVA = "Java"
    DOTNET = "DotNet"
    SQL = "SQL"
    NOSQL = "NoSQL"
    CLOUD = "Cloud"
    ON_PREMISE = "OnPremise"


class SecurityAspect(Enum):
    AUTHENTICATION = "Authentication"
    AUTHORIZATION = "Authorization"
    DATA_ENCRYPTION = "DataEncryption"
    INPUT_VALIDATION = "InputValidation"
    XSS = "CrossSiteScripting"
    SQL_INJECTION = "SQLInjection"


class SeverityLevel(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class RemediationType(Enum):
    CODE_FIX = "CodeFix"
    CONFIGURATION_CHANGE = "ConfigurationChange"
    DEPENDENCY_UPDATE = "DependencyUpdate"
    ARCHITECTURE_CHANGE = "ArchitectureChange"


class AffectedComponent(Enum):
    USER_INTERFACE = "UserInterface"
    API = "API"
    DATABASE = "Database"
    NETWORK = "Network"
    THIRD_PARTY_INTEGRATION = "ThirdPartyIntegration"


class Compliance(Enum):
    GDPR = "GDPR"
    PCI_DSS = "PCI_DSS"
    HIPAA = "HIPAA"

# class Location # TODO: Add Location class

# TODO: add kmeans clustering for categories based on solution


class Category(BaseModel):
    technology_stack: Optional[List[TechnologyStack]] = Field(default_factory=list)
    security_aspect: Optional[List[SecurityAspect]] = Field(default_factory=list)
    severity_level: Optional[SeverityLevel] = None
    remediation_type: Optional[List[RemediationType]] = Field(default_factory=list)
    affected_component: Optional[List[AffectedComponent]] = Field(default_factory=list)
    compliance: Optional[List[Compliance]] = Field(default_factory=list)
