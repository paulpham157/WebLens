"""
Pydantic Models for Browser Use API

This module contains structured data models used by the Browser Use API.
"""
from pydantic import BaseModel
from typing import List, Optional

class SocialMediaCompany(BaseModel):
    name: str
    market_cap: float
    headquarters: str
    founded_year: int


class SocialMediaCompanies(BaseModel):
    companies: List[SocialMediaCompany]


class WebsiteAnalysis(BaseModel):
    title: str
    meta_description: str
    main_content: str
    links_count: int
    images_count: int
    load_time: float
    accessibility_score: int


class PriceComparison(BaseModel):
    product_name: str
    price: float
    currency: str
    store_name: str
    availability: str
    rating: float


class PriceComparisonResults(BaseModel):
    products: List[PriceComparison]
    cheapest_price: float
    most_expensive_price: float


class NewsArticle(BaseModel):
    title: str
    summary: str
    author: str
    published_date: str
    source: str
    category: str


class NewsCollection(BaseModel):
    articles: List[NewsArticle]
    total_count: int
