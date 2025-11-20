"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Apex Performance Nexus schemas

class Vector3D(BaseModel):
    x: float
    y: float
    z: float

class EEGFrequency(BaseModel):
    alpha: float = Field(ge=0)
    beta: float = Field(ge=0)
    gamma: float = Field(ge=0)
    delta: float = Field(ge=0)
    theta: float = Field(ge=0)

class EMGData(BaseModel):
    channels: List[float] = Field(default_factory=list, description="EMG channel amplitudes")

class BioMetrics(BaseModel):
    """Biometric snapshot for an athlete session.
    Collection name: "biometrics"
    """
    heartRate: List[float] = Field(default_factory=list, description="Recent HR samples")
    emgSignals: EMGData
    motionCapture: Vector3D
    oxygenSaturation: float
    lactateThreshold: float
    neuralActivity: EEGFrequency
    athleteId: Optional[str] = None
    sessionId: Optional[str] = None
