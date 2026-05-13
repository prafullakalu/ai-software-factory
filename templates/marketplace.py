"""
🏪 TEMPLATE MARKETPLACE

Local template marketplace with sharing capabilities.
Features:
- Browse templates
- Search templates
- Rate templates
- Categories
- Import/Export
"""

import os
import json
import shutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ============================================================================
# TEMPLATE TYPES
# ============================================================================

class TemplateCategory(Enum):
    SAAS = "saas"
    FINTECH = "fintech"
    ECOMMERCE = "ecommerce"
    API = "api"
    DASHBOARD = "dashboard"
    BLOG = "blog"
    PORTFOLIO = "portfolio"
    MOBILE = "mobile"
    CUSTOM = "custom"


class TemplatePricing(Enum):
    FREE = "free"
    PAID = "paid"


class TemplateRating(Enum):
    UNRATED = 0
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5


# ============================================================================
# TEMPLATE MODEL
# ============================================================================

@dataclass
class Template:
    """Template model."""
    id: str
    name: str
    description: str
    category: TemplateCategory
    
    # Metadata
    author: str
    version: str
    tags: List[str]
    
    # Tech stack
    frontend: List[str]
    backend: List[str]
    database: List[str]
    
    # Features
    features: List[str]
    
    # Rating
    rating: float = 0.0
    downloads: int = 0
    
    # Pricing
    pricing: TemplatePricing = TemplatePricing.FREE
    price: float = 0.0
    
    # Files
    path: str = ""
    
    # Timestamps
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "author": self.author,
            "version": self.version,
            "tags": self.tags,
            "frontend": self.frontend,
            "backend": self.backend,
            "database": self.database,
            "features": self.features,
            "rating": self.rating,
            "downloads": self.downloads,
            "pricing": self.pricing.value,
            "price": self.price,
            "path": self.path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ============================================================================
# TEMPLATE MARKETPLACE
# ============================================================================

class TemplateMarketplace:
    """Template marketplace manager."""
    
    def __init__(self, marketplace_path: str = "templates/marketplace"):
        self.marketplace_path = marketplace_path
        self.templates: Dict[str, Template] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load templates from marketplace."""
        if not os.path.exists(self.marketplace_path):
            os.makedirs(self.marketplace_path, exist_ok=True)
        
        # Load each template
        for template_dir in os.listdir(self.marketplace_path):
            template_path = os.path.join(self.marketplace_path, template_dir)
            if os.path.isdir(template_path):
                # Try to load metadata
                metadata_file = os.path.join(template_path, "template.json")
                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, "r") as f:
                            data = json.load(f)
                            template = Template(**data)
                            template.path = template_path
                            self.templates[template.id] = template
                    except:
                        pass
    
    def _save_template(self, template: Template):
        """Save template to marketplace."""
        template_path = os.path.join(self.marketplace_path, template.id)
        os.makedirs(template_path, exist_ok=True)
        
        # Save metadata
        metadata_file = os.path.join(template_path, "template.json")
        with open(metadata_file, "w") as f:
            json.dump(template.to_dict(), f, indent=2)
        
        self.templates[template.id] = template
    
    def create(self, template: Template) -> Template:
        """Add new template."""
        self._save_template(template)
        return template
    
    def get(self, template_id: str) -> Optional[Template]:
        """Get template by ID."""
        return self.templates.get(template_id)
    
    def update(self, template_id: str, **kwargs) -> Optional[Template]:
        """Update template."""
        if template_id not in self.templates:
            return None
        
        template = self.templates[template_id]
        for key, value in kwargs.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        template.updated_at = datetime.now()
        self._save_template(template)
        
        return template
    
    def delete(self, template_id: str) -> bool:
        """Delete template."""
        if template_id in self.templates:
            template = self.templates[template_id]
            if template.path and os.path.exists(template.path):
                shutil.rmtree(template.path)
            del self.templates[template_id]
            return True
        return False
    
    def list_all(self, category: TemplateCategory = None) -> List[Template]:
        """List all templates."""
        templates = list(self.templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        return sorted(templates, key=lambda t: t.downloads, reverse=True)
    
    def search(self, query: str) -> List[Template]:
        """Search templates."""
        query = query.lower()
        
        results = []
        for template in self.templates.values():
            # Search in name, description, tags
            if (query in template.name.lower() or
                query in template.description.lower() or
                any(query in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return sorted(results, key=lambda t: t.rating, reverse=True)
    
    def rate(self, template_id: str, rating: float) -> bool:
        """Rate a template."""
        if template_id not in self.templates:
            return False
        
        template = self.templates[template_id]
        
        # Calculate new rating (simple average)
        current_rating = template.rating
        new_rating = (current_rating + rating) / 2
        
        template.rating = new_rating
        template.updated_at = datetime.now()
        
        self._save_template(template)
        
        return True
    
    def download(self, template_id: str, dest_path: str) -> bool:
        """Download template."""
        template = self.get(template_id)
        if not template or not template.path:
            return False
        
        try:
            # Copy template files
            shutil.copytree(template.path, dest_path, dirs_exist_ok=True)
            
            # Increment downloads
            template.downloads += 1
            self._save_template(template)
            
            return True
        except Exception as e:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get marketplace statistics."""
        total = len(self.templates)
        total_downloads = sum(t.downloads for t in self.templates.values())
        avg_rating = sum(t.rating for t in self.templates.values()) / max(total, 1)
        
        # By category
        by_category = {}
        for template in self.templates.values():
            cat = template.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        return {
            "total_templates": total,
            "total_downloads": total_downloads,
            "average_rating": avg_rating,
            "by_category": by_category,
        }


# ============================================================================
# DEFAULT TEMPLATES
# ============================================================================

def create_default_templates(marketplace: TemplateMarketplace):
    """Create default templates."""
    
    templates = [
        Template(
            id="saas-starter",
            name="SaaS Starter Kit",
            description="Complete SaaS application with auth, billing, and dashboard",
            category=TemplateCategory.SAAS,
            author="AI Factory",
            version="1.0.0",
            tags=["saas", "auth", "billing", "dashboard", "nextjs", "fastapi"],
            frontend=["nextjs", "react", "tailwind"],
            backend=["fastapi", "python"],
            database=["postgresql", "redis"],
            features=["authentication", "billing", "dashboard", "multi-tenant"],
            rating=4.8,
            downloads=1250,
            pricing=TemplatePricing.FREE,
        ),
        Template(
            id="fintech-payment",
            name="Payment Gateway",
            description="Complete payment processing solution with Stripe integration",
            category=TemplateCategory.FINTECH,
            author="AI Factory",
            version="1.0.0",
            tags=["fintech", "payments", "stripe", "wallet"],
            frontend=["nextjs", "react", "tailwind"],
            backend=["fastapi", "python"],
            database=["postgresql", "redis"],
            features=["stripe", "wallet", "transactions", "webhooks"],
            rating=4.9,
            downloads=890,
            pricing=TemplatePricing.FREE,
        ),
        Template(
            id="ecommerce-store",
            name="E-commerce Store",
            description="Full-featured online store with cart and checkout",
            category=TemplateCategory.ECOMMERCE,
            author="AI Factory",
            version="1.0.0",
            tags=["ecommerce", "shop", "cart", "checkout"],
            frontend=["nextjs", "react", "tailwind"],
            backend=["fastapi", "python"],
            database=["postgresql"],
            features=["products", "cart", "checkout", "payments", "inventory"],
            rating=4.7,
            downloads=720,
            pricing=TemplatePricing.FREE,
        ),
        Template(
            id="rest-api",
            name="REST API Boilerplate",
            description="Production-ready REST API with auth and documentation",
            category=TemplateCategory.API,
            author="AI Factory",
            version="1.0.0",
            tags=["api", "rest", "openapi", "documentation"],
            frontend=[],
            backend=["fastapi", "python"],
            database=["postgresql"],
            features=["rest", "openapi", "auth", "pagination", "rate-limit"],
            rating=4.6,
            downloads=540,
            pricing=TemplatePricing.FREE,
        ),
        Template(
            id="admin-dashboard",
            name="Admin Dashboard",
            description="Analytics dashboard with charts and data tables",
            category=TemplateCategory.DASHBOARD,
            author="AI Factory",
            version="1.0.0",
            tags=["dashboard", "admin", "charts", "analytics"],
            frontend=["nextjs", "react", "tailwind", "recharts"],
            backend=[],
            database=[],
            features=["charts", "tables", "dark-mode", "responsive"],
            rating=4.5,
            downloads=430,
            pricing=TemplatePricing.FREE,
        ),
        Template(
            id="blog-cms",
            name="Blog CMS",
            description="Content management system for blogs with markdown support",
            category=TemplateCategory.BLOG,
            author="AI Factory",
            version="1.0.0",
            tags=["blog", "cms", "markdown", "seo"],
            frontend=["nextjs", "react", "tailwind"],
            backend=["fastapi", "python"],
            database=["postgresql"],
            features=["markdown", "categories", "tags", "seo", "rss"],
            rating=4.4,
            downloads=320,
            pricing=TemplatePricing.FREE,
        ),
    ]
    
    for template in templates:
        marketplace.create(template)


# ============================================================================
# EXPORTS
# ============================================================================

marketplace = TemplateMarketplace()

# Initialize with default templates if empty
if not marketplace.templates:
    create_default_templates(marketplace)


__all__ = [
    "Template",
    "TemplateCategory",
    "TemplatePricing",
    "TemplateRating",
    "TemplateMarketplace",
    "create_default_templates",
    "marketplace",
]