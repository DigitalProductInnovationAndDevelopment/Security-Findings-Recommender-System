from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class VulnerabilityType(Enum):
    INJECTION = "Injection"
    BROKEN_AUTHENTICATION = "Broken Authentication"
    SENSITIVE_DATA_EXPOSURE = "Sensitive Data Exposure"
    XML_EXTERNAL_ENTITIES = "XML External Entities (XXE)"
    BROKEN_ACCESS_CONTROL = "Broken Access Control"
    SECURITY_MISCONFIGURATION = "Security Misconfiguration"
    CROSS_SITE_SCRIPTING = "Cross-Site Scripting (XSS)"
    INSECURE_DESERIALIZATION = "Insecure Deserialization"
    USING_COMPONENTS_WITH_KNOWN_VULNERABILITIES = "Using Components with Known Vulnerabilities"
    INSUFFICIENT_LOGGING_AND_MONITORING = "Insufficient Logging & Monitoring"


class AffectedComponent(Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    DATABASE = "Database"
    API = "API"
    AUTHENTICATION_SERVICE = "Authentication Service"
    THIRD_PARTY_SERVICE = "Third-Party Service"
    NETWORK = "Network"
    CONFIGURATION = "Configuration"


class ImpactLevel(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class RemediationComplexity(Enum):
    SIMPLE = "Simple"
    MODERATE = "Moderate"
    COMPLEX = "Complex"


class Category(BaseModel):
    vulnerability_type: List[VulnerabilityType] = Field(default_factory=list)
    affected_components: List[AffectedComponent] = Field(default_factory=list)
    impact_level: Optional[ImpactLevel] = None
    remediation_complexity: Optional[RemediationComplexity] = None
