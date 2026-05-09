from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Maintainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str


class Source(BaseModel):
    model_config = ConfigDict(extra="allow")

    mode: Literal["manual", "artifact", "cherri", "jelly"]
    entrypoint: str | None = None


class ShortcutManifest(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    version: str
    summary: str
    category: str
    status: Literal["experimental", "stable", "deprecated", "archived"]
    license: str
    maintainers: list[Maintainer] = Field(min_length=1)
    source: Source
    declared_permissions: dict[str, Any]
    compatibility: dict[str, Any] | None = None
    security: dict[str, Any] | None = None
    tests: dict[str, Any] | None = None
    release: dict[str, Any] | None = None


class ActionEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    risk_tier: Literal["low", "interactive", "sensitive", "high", "critical"]
    permissions: list[str]
    notes: str | None = None
    docs_url: str | None = None
    detectors: list[str] = Field(default_factory=list)
    remediation: str | None = None


class ActionDB(BaseModel):
    model_config = ConfigDict(extra="allow")

    version: str
    actions: list[ActionEntry]


class Finding(BaseModel):
    id: str
    title: str
    severity: Literal["info", "low", "medium", "high", "critical"]
    status: Literal["declared", "detected", "unknown", "reviewed", "mismatch"]
    detail: str
    path: str | None = None
    remediation: str | None = None
    review_required: str | None = None
    evidence: list[str] = Field(default_factory=list)


class SecurityAudit(BaseModel):
    package_id: str
    actiondb_version: str
    strict: bool
    passed: bool
    summary: dict[str, Any] = Field(default_factory=dict)
    findings: list[Finding]


class AdapterCapabilities(BaseModel):
    build: bool = False
    export: bool = False
    inspect: bool = False
    test: bool = False
    license: str


class AdapterInfo(BaseModel):
    id: str
    name: str
    binary: str | None = None
    available: bool
    capabilities: AdapterCapabilities
    install: str | None = None
    notes: str


class BuildMetadata(BaseModel):
    package_id: str
    adapter_id: str
    adapter_version: str | None = None
    command: list[str] = Field(default_factory=list)
    environment: dict[str, str] = Field(default_factory=dict)
    source_hash: str
    artifact_path: str | None = None
    status: Literal["built", "manual", "skipped", "unavailable"]
    message: str


class RuntimeTestResult(BaseModel):
    package_id: str
    status: Literal["passed", "failed", "skipped", "disabled"]
    requires_macos: bool
    command: list[str] = Field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    message: str


class ReleaseMetadata(BaseModel):
    package_id: str
    version: str
    source_commit: str | None = None
    manifest: dict[str, Any]
    audit: SecurityAudit
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    build: BuildMetadata | None = None
