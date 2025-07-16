from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    role: str # Keep it simple as string for now

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# --- RawDataset Schemas ---
class RawDatasetBase(BaseModel):
    instruction: Optional[str] = None
    input: Optional[str] = None
    output: str
    system: Optional[str] = None
    source: Optional[List[str]] = []
    history: Optional[List[Any]] = []

class RawDatasetCreate(RawDatasetBase):
    pass

class RawDatasetUpdate(RawDatasetBase):
    pass

class RawDataset(RawDatasetBase):
    id: int
    review_status: str
    # history is already in Base
    model_config = ConfigDict(from_attributes=True)

class ReviewLogInDB(BaseModel):
    reviewer_id: int
    
    model_config = ConfigDict(from_attributes=True)

class RawDatasetWithStats(RawDataset):
    accept_count: int
    reject_count: int
    review_logs: List[ReviewLogInDB] = []


# --- Review Schemas ---
class ReviewCreate(BaseModel):
    result: str # "ACCEPT" or "REJECT"
    comment: Optional[str] = None
    common_reasons: Optional[List[str]] = None  # 新增：常見拒絕理由列表
    detailed_reason: Optional[str] = None  # 新增：詳細拒絕理由

# --- Common Rejection Reasons Schema ---
class CommonRejectionReason(BaseModel):
    id: str
    label: str
    description: str
    category: str

# --- ReviewLog Schema for Rejection Info ---
class RejectionInfo(BaseModel):
    id: int
    comment: Optional[str] = None
    common_reasons: Optional[List[str]] = None  # 新增
    detailed_reason: Optional[str] = None  # 新增
    timestamp: datetime
    reviewer_username: str
    model_config = ConfigDict(from_attributes=True)

# --- System Settings Schemas ---

class SystemSetting(BaseModel):
    key: str
    value: Any
    model_config = ConfigDict(from_attributes=True)

class SystemSettingsUpdate(BaseModel):
    settings: Dict[str, Any]


# --- All Settings Schema ---
class AllSettings(BaseModel):
    rejection_threshold: int
    approval_threshold: int
    ollama_model: str
    ollama_url: str

# --- Ollama Schemas ---
class OllamaPullRequest(BaseModel):
    model_name: str

class OllamaTestRequest(BaseModel):
    url: str

# --- Stats Schemas ---

class GlobalStats(BaseModel):
    total_datasets: int
    total_reviews: int
    total_accepts: int
    total_rejects: int

class ReviewActivity(BaseModel):
    date: str
    count: int

class TopReviewer(BaseModel):
    username: str
    review_count: int

class CommonRejectionReason(BaseModel):
    reason: str
    count: int

class DashboardStats(BaseModel):
    global_stats: GlobalStats
    review_activity: List[ReviewActivity]
    top_reviewers: List[TopReviewer]
    common_rejection_reasons: List[CommonRejectionReason]

# --- Legal Article Schemas ---

class LegalArticleBase(BaseModel):
    title: str
    number: str
    content: str

class LegalArticleCreate(LegalArticleBase):
    pass

class LegalArticle(LegalArticleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Dataset Generation Schemas ---

class GenerateFromRegulationsRequest(BaseModel):
    selected_article_ids: List[int]

class GeneratedDataset(BaseModel):
    instruction: str
    input: Optional[str] = None
    output: str
    system: Optional[str] = None
    history: List[Dict[str, str]] = []
    source: List[str] = []
