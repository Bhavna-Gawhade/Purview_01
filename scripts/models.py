from typing import List, Optional
from pydantic import BaseModel

####################################################################
# scanning.operations.DataSourcesOperations.create_or_update
####################################################################

class DiagnosticDetails(BaseModel):
    code: Optional[str]
    details: Optional[List["DiagnosticDetails"]]
    message: Optional[str]
    target: Optional[str]

class DiagnosticNotification(BaseModel):
    code: Optional[int]
    message: Optional[str]

class Diagnostic(BaseModel):
    exceptionCountMap: Optional[dict]
    notifications: Optional[List[DiagnosticNotification]]

class ScanResult(BaseModel):
    assetsClassified: Optional[float]
    assetsDiscovered: Optional[float]
    dataSourceType: Optional[str]
    diagnostics: Optional[Diagnostic]
    endTime: Optional[str]
    error: Optional[DiagnosticDetails]
    errorMessage: Optional[str]
    id: Optional[str]
    parentId: Optional[str]
    pipelineStartTime: Optional[str]
    queuedTime: Optional[str]
    resourceId: Optional[str]
    runType: Optional[str]
    scanLevelType: Optional[str]
    scanRulesetType: Optional[str]
    scanRulesetVersion: Optional[int]
    startTime: Optional[str]
    status: Optional[str]

class Scan(BaseModel):
    id: Optional[str]
    name: Optional[str]
    scanResults: Optional[List[ScanResult]]

class DataSource(BaseModel):
    id: Optional[str]
    name: Optional[str]
    scans: Optional[List[Scan]]

class Body(BaseModel):
    id: Optional[str]
    name: Optional[str]
    scans: Optional[List[Scan]]
    kind: Optional[str]

####################################################################
# catalog.aio.operations.EntityOperations.add_classifications
####################################################################

####################################################################
# catalog.aio.operations.EntityOperations.add_label
####################################################################

####################################################################
# catalog.aio.operations.EntityOperations.add_or_update_business_metadata
####################################################################

####################################################################
# catalog.aio.operations.EntityOperations.add_or_update_business_metadata_attributes
####################################################################

####################################################################
# catalog.aio.operations.EntityOperations.create_or_update_entities
####################################################################

####################################################################
# catalog.aio.operations.EntityOperations.set_classifications
####################################################################



####################################################################
# purview.catalog.aio.operations.GlossaryOperations.assign_term_to_entities
####################################################################