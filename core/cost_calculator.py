"""
💰 COST CALCULATOR

Estimate costs for:
- Cloud hosting (Vercel, AWS, etc.)
- LLM API usage
- Database
- Third-party services
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# PRICING MODELS
# ============================================================================

class CloudProvider(Enum):
    VERCEL = "vercel"
    NETLIFY = "netlify"
    AWS = "aws"
    RAILWAY = "railway"
    DIGITALOCEAN = "digitalocean"
    HEROKU = "heroku"


class DatabaseType(Enum):
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    REDIS = "redis"
    MYSQL = "mysql"


@dataclass
class CostEstimate:
    """Cost estimate result."""
    category: str
    item: str
    monthly_cost: float
    details: str


# ============================================================================
# COST CALCULATOR
# ============================================================================

class CostCalculator:
    """Calculate project costs."""
    
    def __init__(self):
        self.pricing = self._load_pricing()
    
    def _load_pricing(self) -> Dict:
        """Load pricing data."""
        return {
            # Cloud Hosting
            "vercel": {
                "pro": {"price": 20, "features": ["unlimited projects", "analytics"]},
                "team": {"price": 150, "features": ["SSO", "audit log"]},
                "enterprise": {"price": 600, "features": ["SLA", "support"]},
            },
            "railway": {
                "starter": {"price": 5, "resources": "1GB RAM, 1 CPU"},
                "pro": {"price": 20, "resources": "4GB RAM, 2 CPU"},
                "team": {"price": 50, "resources": "8GB RAM, 4 CPU"},
            },
            "aws": {
                "ec2": {"price": 0.023, "unit": "per hour (t3.micro)"},
                "rds": {"price": 0.017, "unit": "per hour (db.t3.micro)"},
                "s3": {"price": 0.023, "unit": "per GB/month"},
            },
            # Databases
            "postgresql": {
                "vercel": {"price": 0.007, "unit": "per hour"},
                "railway": {"price": 5, "unit": "per month"},
                "neon": {"price": 0, "unit": "free tier"},
                "supabase": {"price": 0, "unit": "free tier"},
            },
            "mongodb": {
                "atlas": {"price": 0, "unit": "free tier"},
            },
            "redis": {
                "upstash": {"price": 0, "unit": "free tier"},
                "rediscloud": {"price": 0, "unit": "free tier"},
            },
            # LLM Pricing (per 1M tokens)
            "llm": {
                "gpt-4o": {"input": 5.0, "output": 15.0},
                "gpt-4": {"input": 30.0, "output": 60.0},
                "gpt-3.5": {"input": 0.5, "output": 1.5},
                "claude-3.5": {"input": 3.0, "output": 15.0},
                "claude-3": {"input": 15.0, "output": 75.0},
                "gemini-1.5": {"input": 1.25, "output": 5.0},
                "ollama": {"price": 0, "unit": "free (local)"},
            },
        }
    
    def calculate_hosting(
        self,
        provider: str,
        tier: str,
        monthly_visitors: int = 10000,
    ) -> List[CostEstimate]:
        """Calculate hosting costs."""
        estimates = []
        
        if provider == "vercel":
            base_price = self.pricing["vercel"].get(tier, {}).get("price", 0)
            bandwidth = max(0, (monthly_visitors - 1000) * 0.1)  # $0.10 per GB over 1GB
            
            estimates.append(CostEstimate(
                category="hosting",
                item=f"Vercel {tier.capitalize()}",
                monthly_cost=base_price + bandwidth,
                details=f"Base: ${base_price}/mo + bandwidth: ${bandwidth:.2f}"
            ))
        
        elif provider == "railway":
            base_price = self.pricing["railway"].get(tier, {}).get("price", 5)
            estimates.append(CostEstimate(
                category="hosting",
                item=f"Railway {tier.capitalize()}",
                monthly_cost=base_price,
                details=self.pricing["railway"].get(tier, {}).get("resources", "")
            ))
        
        elif provider == "aws":
            ec2_price = 0.023 * 730  # ~$17/month
            rds_price = 0.017 * 730  # ~$12/month
            
            estimates.append(CostEstimate(
                category="hosting",
                item="AWS EC2 (t3.micro)",
                monthly_cost=ec2_price,
                details="~730 hours/month"
            ))
            estimates.append(CostEstimate(
                category="database",
                item="AWS RDS (t3.micro)",
                monthly_cost=rds_price,
                details="~730 hours/month"
            ))
        
        return estimates
    
    def calculate_database(
        self,
        db_type: str,
        provider: str,
        storage_gb: float = 1,
    ) -> List[CostEstimate]:
        """Calculate database costs."""
        estimates = []
        
        if db_type == "postgresql":
            if provider == "neon":
                estimates.append(CostEstimate(
                    category="database",
                    item="Neon (PostgreSQL)",
                    monthly_cost=0,
                    details="Free tier: 0.5GB storage"
                ))
            elif provider == "supabase":
                estimates.append(CostEstimate(
                    category="database",
                    item="Supabase (PostgreSQL)",
                    monthly_cost=0,
                    details="Free tier: 500MB storage"
                ))
            elif provider == "railway":
                estimates.append(CostEstimate(
                    category="database",
                    item="Railway PostgreSQL",
                    monthly_cost=5,
                    details="~1GB storage"
                ))
        
        elif db_type == "redis":
            if provider == "upstash":
                estimates.append(CostEstimate(
                    category="database",
                    item="Upstash (Redis)",
                    monthly_cost=0,
                    details="Free tier: 10K commands"
                ))
        
        return estimates
    
    def calculate_llm(
        self,
        provider: str,
        model: str,
        input_tokens: int = 100000,
        output_tokens: int = 50000,
    ) -> List[CostEstimate]:
        """Calculate LLM API costs."""
        estimates = []
        
        # Get pricing
        llm_pricing = self.pricing.get("llm", {}).get(model, {})
        
        input_cost = (input_tokens / 1_000_000) * llm_pricing.get("input", 0)
        output_cost = (output_tokens / 1_000_000) * llm_pricing.get("output", 0)
        total_monthly = (input_cost + output_cost) * 30  # Daily usage * 30 days
        
        estimates.append(CostEstimate(
            category="llm",
            item=f"{provider}/{model}",
            monthly_cost=total_monthly,
            details=f"Input: {input_tokens:,}/mo, Output: {output_tokens:,}/mo"
        ))
        
        return estimates
    
    def calculate_third_party(
        self,
        services: List[str],
    ) -> List[CostEstimate]:
        """Calculate third-party service costs."""
        estimates = []
        
        service_costs = {
            "stripe": 0,  # Free for first $X
            "sendgrid": 0,  # Free tier
            "resend": 0,  # Free tier
            "sentry": 0,  # Free tier
            "logrocket": 0,  # Free tier
            "mixpanel": 0,  # Free tier
        }
        
        for service in services:
            if service in service_costs:
                estimates.append(CostEstimate(
                    category="third_party",
                    item=service.capitalize(),
                    monthly_cost=service_costs[service],
                    details="Free tier available"
                ))
        
        return estimates
    
    def calculate_total(
        self,
        hosting_provider: str = "vercel",
        hosting_tier: str = "pro",
        monthly_visitors: int = 10000,
        db_type: str = "postgresql",
        db_provider: str = "supabase",
        llm_provider: str = "ollama",
        llm_model: str = "llama3",
        input_tokens: int = 100000,
        output_tokens: int = 50000,
        third_party: List[str] = None,
    ) -> Dict:
        """Calculate total monthly cost."""
        all_estimates = []
        
        # Hosting
        all_estimates.extend(self.calculate_hosting(
            hosting_provider, hosting_tier, monthly_visitors
        ))
        
        # Database
        all_estimates.extend(self.calculate_database(
            db_type, db_provider
        ))
        
        # LLM (skip if free)
        if llm_provider != "ollama":
            all_estimates.extend(self.calculate_llm(
                llm_provider, llm_model, input_tokens, output_tokens
            ))
        else:
            all_estimates.append(CostEstimate(
                category="llm",
                item="Ollama (Local)",
                monthly_cost=0,
                details="Running locally - no API costs!"
            ))
        
        # Third party
        if third_party:
            all_estimates.extend(self.calculate_third_party(third_party))
        
        # Calculate totals
        total = sum(e.monthly_cost for e in all_estimates)
        
        # By category
        by_category = {}
        for e in all_estimates:
            if e.category not in by_category:
                by_category[e.category] = 0
            by_category[e.category] += e.monthly_cost
        
        return {
            "estimates": [e.to_dict() for e in all_estimates],
            "total_monthly": total,
            "total_yearly": total * 12,
            "by_category": by_category,
            "recommendations": self._get_recommendations(total),
        }
    
    def _get_recommendations(self, total: float) -> List[str]:
        """Get cost optimization recommendations."""
        recommendations = []
        
        if total > 100:
            recommendations.append("Consider using Ollama (free local models) instead of paid APIs")
        
        if total > 50:
            recommendations.append("Switch to Supabase/Neon for free PostgreSQL")
            recommendations.append("Use Upstash for free Redis")
        
        if total > 20:
            recommendations.append("Vercel free tier may be sufficient")
        
        if total == 0:
            recommendations.append("🎉 You can run this project for FREE!")
        
        return recommendations
    
    def format_report(self, result: Dict) -> str:
        """Format cost report."""
        lines = [
            "\n" + "="*60,
            "💰 COST ESTIMATE REPORT",
            "="*60 + "\n",
        ]
        
        lines.append("📊 Monthly Breakdown:\n")
        for e in result["estimates"]:
            cost_str = f"${e['monthly_cost']:.2f}" if e['monthly_cost'] > 0 else "FREE"
            lines.append(f"  {e['item']:<30} {cost_str:>10}/mo")
            lines.append(f"    └─ {e['details']}")
        
        lines.append(f"\n💵 TOTAL: ${result['total_monthly']:.2f}/month")
        lines.append(f"   = ${result['total_yearly']:.2f}/year")
        
        if result["recommendations"]:
            lines.append("\n💡 RECOMMENDATIONS:")
            for r in result["recommendations"]:
                lines.append(f"  • {r}")
        
        lines.append("\n" + "="*60)
        
        return "\n".join(lines)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def demo():
    """Demo the cost calculator."""
    calc = CostCalculator()
    
    # Example: Paid LLM
    result = calc.calculate_total(
        hosting_provider="vercel",
        hosting_tier="pro",
        db_type="postgresql",
        db_provider="supabase",
        llm_provider="openai",
        llm_model="gpt-4o",
        input_tokens=100000,
        output_tokens=50000,
    )
    
    print(calc.format_report(result))
    
    # Example: Free tier
    result2 = calc.calculate_total(
        hosting_provider="vercel",
        hosting_tier="pro",
        db_type="postgresql",
        db_provider="supabase",
        llm_provider="ollama",
        llm_model="llama3",
    )
    
    print(calc.format_report(result2))


# ============================================================================
# EXPORTS
# ============================================================================

calculator = CostCalculator()


__all__ = [
    "CostCalculator",
    "CostEstimate",
    "CloudProvider",
    "DatabaseType",
    "calculator",
]