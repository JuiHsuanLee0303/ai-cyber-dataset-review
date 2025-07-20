from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List, Any, Dict
from datetime import datetime
import re

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    role: str # Keep it simple as string for now

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    password: Optional[str] = None
    role: Optional[str] = None

    @field_validator('password')
    def password_complexity_optional(cls, v):
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

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
    model_name: Optional[str] = None  # 新增：生成使用的模型名稱

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


# --- FinalDataset Schemas ---
class FinalDatasetBase(BaseModel):
    original_input: str
    final_output: str
    raw_dataset_id: int
    model_name: Optional[str] = None

class FinalDatasetCreate(FinalDatasetBase):
    pass

class FinalDataset(FinalDatasetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Review Schemas ---
class ReviewCreate(BaseModel):
    result: str # "ACCEPT" or "REJECT"
    comment: Optional[str] = None # For custom, detailed text
    rejection_reason_ids: Optional[List[int]] = [] # List of IDs for common reasons

# --- Rejection Reason Schemas ---
class RejectionReasonBase(BaseModel):
    label: str
    description: Optional[str] = None
    category: str

class RejectionReasonCreate(RejectionReasonBase):
    pass

class RejectionReason(RejectionReasonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- ReviewLog Schema for Rejection Info ---
class RejectionInfo(BaseModel):
    id: int
    comment: Optional[str] = None
    rejection_reasons: List[RejectionReason] = [] # Use the new schema
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
    ollama_models: List[str]  # 修改：從單一模型改為多模型列表
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

class ModelStats(BaseModel):
    model_name: str
    total_datasets: int
    total_reviews: int
    total_accepts: int
    total_rejects: int
    acceptance_rate: float

class DashboardStats(BaseModel):
    global_stats: GlobalStats
    review_activity: List[ReviewActivity]
    top_reviewers: List[TopReviewer]
    common_rejection_reasons: List[CommonRejectionReason]
    model_stats: List[ModelStats]  # 新增：按模型分類的統計

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
    model_name: Optional[str] = None  # 新增：指定使用的模型名稱

class GeneratedDataset(BaseModel):
    instruction: str
    input: Optional[str] = None
    output: str
    system: Optional[str] = None
    history: List[Dict[str, str]] = []
    source: List[str] = []
    model_name: Optional[str] = None  # 新增：生成使用的模型名稱
