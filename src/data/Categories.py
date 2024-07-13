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
    RUST = "Rust"
    GO = "Go"
    C_DIALECT = "CDialect"
    RUBY = "Ruby"
    PHP = "PHP"
    ON_PREMISE = "OnPremise"


class SecurityAspect(Enum):
    AUTHENTICATION = "Authentication"
    AUTHORIZATION = "Authorization"
    DATA_ENCRYPTION = "DataEncryption"
    INPUT_VALIDATION = "InputValidation"
    XSS = "CrossSiteScripting"
    SQL_INJECTION = "SQLInjection"
    CommandInjection = "CommandInjection"
    CRYPTOGRAPHY = "Cryptography"
    LOGGING = "Logging"
    CONFIGURATION = "Configuration"


class SeverityLevel(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class RemediationType(Enum):
    CODE_FIX = "CodeFix"
    CONFIGURATION_CHANGE = "ConfigurationChange"
    DEPENDENCY_UPDATE = "DependencyUpdate"
    ARCHITECTURE_CHANGE = "ArchitectureChange"
    SECURITY_TRAINING = "SecurityTraining"
    PROCESS_IMPROVEMENT = "ProcessImprovement"


class AffectedComponent(Enum):
    USER_INTERFACE = "UserInterface"
    API = "API"
    DATABASE = "Database"
    NETWORK = "Network"
    THIRD_PARTY_INTEGRATION = "ThirdPartyIntegration"
    AUTHENTICATION_SERVICE = "AuthenticationService"
    LOGGING_SYSTEM = "LoggingSystem"
    CACHING_LAYER = "CachingLayer"
    ORCHESTRATION= "Orchestration"


class Compliance(Enum):
    GDPR = "GDPR"
    PCI_DSS = "PCI_DSS"
    HIPAA = "HIPAA"
    ISO27001 = "ISO27001"
    SOC2 = "SOC2"
    NIST = "NIST"


class Environment(Enum):
    DOCKER = "Docker"`Ω
    KUBERNETES = "Kubernetes"
    SERVERLESS = "Serverless"
    VIRTUAL_MACHINE = "VirtualMachine"
    BARE_METAL = "BareMetal"


# class Location # TODO: Add Location class

# TODO: add kmeans clustering for categories based on solution


class Category(BaseModel):
    technology_stack: Optional[List[TechnologyStack]] = None
    security_aspect: Optional[List[SecurityAspect]] = None
    severity_level: Optional[SeverityLevel] = None
    remediation_type: Optional[List[RemediationType]] = None
    affected_component: Optional[List[AffectedComponent]] = None
    compliance: Optional[List[Compliance]] = None
    environment: Optional[List[Environment]] = None

    def __str__(self):
        my_str = ""
        if self.technology_stack:
            my_str += f"Technology Stack: {self.technology_stack.value}\n"
        if self.security_aspect:
            my_str += f"Security Aspect: {self.security_aspect.value}\n"
        if self.severity_level:
            my_str += f"Severity Level: {self.severity_level.value}\n"
        if self.remediation_type:
            my_str += f"Remediation Type: {self.remediation_type.value}\n"
        if self.affected_component:
            my_str += f"Affected Component: {self.affected_component.value}\n"
        if self.compliance:
            my_str += f"Compliance: {self.compliance.value}\n"
        if self.environment:
            my_str += f"Environment: {self.environment.value}\n"
        return my_str

    def to_dict(self):
        my_dict = {}
        if self.technology_stack:
            my_dict["technology_stack"] = self.technology_stack.value
        if self.security_aspect:
            my_dict["security_aspect"] = self.security_aspect.value
        if self.severity_level:
            my_dict["severity_level"] = self.severity_level.value
        if self.remediation_type:
            my_dict["remediation_type"] = self.remediation_type.value
        if self.affected_component:
            my_dict["affected_component"] = self.affected_component.value
        if self.compliance:
            my_dict["compliance"] = self.compliance.value
        if self.environment:
            my_dict["environment"] = self.environment.value
        return my_dict
