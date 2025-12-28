"""
Assessment Module

Manages assessment results and report generation.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Assessment:
    """Complete ethical assessment result."""
    project_name: str
    overall_score: float
    category_scores: Dict[str, float]
    violations: List[Dict[str, Any]]
    risks: List[Any]
    compliance_status: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def high_priority_risks(self) -> List[Any]:
        """Get high priority (critical and high) risks."""
        return [
            risk for risk in self.risks
            if risk.level.value in ["critical", "high"]
        ]
    
    @property
    def critical_violations(self) -> List[Dict[str, Any]]:
        """Get critical severity violations."""
        return [
            v for v in self.violations
            if v.get("severity") == "critical"
        ]
    
    def get_category_status(self, category: str) -> str:
        """Get status label for a category score."""
        score = self.category_scores.get(category, 0)
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "needs_work"
        else:
            return "critical"
    
    def get_top_recommendations(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get top N recommendations based on violation severity.
        
        Args:
            n: Number of recommendations to return
            
        Returns:
            List of recommendation dictionaries
        """
        # Sort violations by severity
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        sorted_violations = sorted(
            self.violations,
            key=lambda v: severity_order.get(v.get("severity", "low"), 1),
            reverse=True
        )
        
        recommendations = []
        for violation in sorted_violations[:n]:
            strategies = violation.get("mitigation_strategies", [])
            if strategies:
                best_strategy = max(strategies, key=lambda s: s.get("effectiveness", 0))
                recommendations.append({
                    "priority": violation.get("severity"),
                    "principle": violation.get("principle_name"),
                    "issue": violation.get("description"),
                    "action": best_strategy.get("description"),
                    "difficulty": best_strategy.get("difficulty"),
                    "effectiveness": best_strategy.get("effectiveness")
                })
        
        return recommendations
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert assessment to dictionary."""
        return {
            "project_name": self.project_name,
            "overall_score": self.overall_score,
            "category_scores": self.category_scores,
            "violations": self.violations,
            "risks": [r.to_dict() for r in self.risks],
            "compliance_status": self.compliance_status,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "summary": {
                "total_violations": len(self.violations),
                "critical_violations": len(self.critical_violations),
                "high_priority_risks": len(self.high_priority_risks),
                "status": self._determine_overall_status()
            }
        }
    
    def _determine_overall_status(self) -> str:
        """Determine overall project status."""
        if self.overall_score >= 85 and len(self.critical_violations) == 0:
            return "excellent"
        elif self.overall_score >= 70 and len(self.critical_violations) == 0:
            return "good"
        elif self.overall_score >= 50:
            return "needs_improvement"
        else:
            return "critical_issues"
    
    def export_json(self, filepath: str):
        """Export assessment to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class AssessmentReport:
    """Generate formatted assessment reports."""
    
    @staticmethod
    def generate(assessment: Assessment, format: str = "text") -> str:
        """
        Generate assessment report in specified format.
        
        Args:
            assessment: Assessment to report on
            format: Report format (text, json, html, markdown)
            
        Returns:
            Formatted report string
        """
        if format == "json":
            return AssessmentReport._generate_json(assessment)
        elif format == "html":
            return AssessmentReport._generate_html(assessment)
        elif format == "markdown":
            return AssessmentReport._generate_markdown(assessment)
        else:
            return AssessmentReport._generate_text(assessment)
    
    @staticmethod
    def _generate_text(assessment: Assessment) -> str:
        """Generate plain text report."""
        report = []
        report.append("=" * 80)
        report.append("EAIFCH ETHICAL ASSESSMENT REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Project: {assessment.project_name}")
        report.append(f"Assessment Date: {assessment.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Overall Score: {assessment.overall_score:.1f}/100")
        report.append("")
        
        # Category scores
        report.append("-" * 80)
        report.append("CATEGORY SCORES")
        report.append("-" * 80)
        for category, score in assessment.category_scores.items():
            status = assessment.get_category_status(category)
            report.append(f"  {category.replace('_', ' ').title():30} {score:6.1f}/100  [{status.upper()}]")
        report.append("")
        
        # Violations
        if assessment.violations:
            report.append("-" * 80)
            report.append(f"VIOLATIONS DETECTED ({len(assessment.violations)})")
            report.append("-" * 80)
            for i, violation in enumerate(assessment.violations, 1):
                report.append(f"\n{i}. [{violation['severity'].upper()}] {violation['principle_name']}")
                report.append(f"   {violation['description']}")
                if violation.get('mitigation_strategies'):
                    report.append("   Recommended Actions:")
                    for strategy in violation['mitigation_strategies'][:2]:
                        report.append(f"     - {strategy['name']}: {strategy['description']}")
        else:
            report.append("✓ No violations detected!")
        
        report.append("")
        
        # Risks
        if assessment.high_priority_risks:
            report.append("-" * 80)
            report.append(f"HIGH PRIORITY RISKS ({len(assessment.high_priority_risks)})")
            report.append("-" * 80)
            for risk in assessment.high_priority_risks:
                report.append(f"\n• {risk.title} [{risk.level.value.upper()}]")
                report.append(f"  {risk.description}")
                report.append(f"  Risk Score: {risk.risk_score:.1f}/100")
        
        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    @staticmethod
    def _generate_json(assessment: Assessment) -> str:
        """Generate JSON report."""
        return json.dumps(assessment.to_dict(), indent=2, ensure_ascii=False)
    
    @staticmethod
    def _generate_markdown(assessment: Assessment) -> str:
        """Generate Markdown report."""
        report = []
        report.append("# EAIFCH Ethical Assessment Report")
        report.append("")
        report.append(f"**Project:** {assessment.project_name}  ")
        report.append(f"**Date:** {assessment.timestamp.strftime('%Y-%m-%d %H:%M:%S')}  ")
        report.append(f"**Overall Score:** {assessment.overall_score:.1f}/100")
        report.append("")
        
        # Category scores
        report.append("## Category Scores")
        report.append("")
        report.append("| Category | Score | Status |")
        report.append("|----------|-------|--------|")
        for category, score in assessment.category_scores.items():
            status = assessment.get_category_status(category)
            emoji = {"excellent": "✅", "good": "👍", "needs_work": "⚠️", "critical": "❌"}
            report.append(f"| {category.replace('_', ' ').title()} | {score:.1f}/100 | {emoji.get(status, '')} {status.title()} |")
        report.append("")
        
        # Violations
        if assessment.violations:
            report.append(f"## Violations ({len(assessment.violations)})")
            report.append("")
            for i, violation in enumerate(assessment.violations, 1):
                severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
                report.append(f"### {i}. {severity_emoji.get(violation['severity'], '')} {violation['principle_name']}")
                report.append(f"**Severity:** {violation['severity'].upper()}  ")
                report.append(f"**Issue:** {violation['description']}")
                report.append("")
                if violation.get('mitigation_strategies'):
                    report.append("**Recommended Actions:**")
                    for strategy in violation['mitigation_strategies']:
                        report.append(f"- **{strategy['name']}**: {strategy['description']}")
                    report.append("")
        
        # Risks
        if assessment.high_priority_risks:
            report.append(f"## High Priority Risks ({len(assessment.high_priority_risks)})")
            report.append("")
            for risk in assessment.high_priority_risks:
                report.append(f"### {risk.title}")
                report.append(f"**Level:** {risk.level.value.upper()}  ")
                report.append(f"**Risk Score:** {risk.risk_score:.1f}/100  ")
                report.append(f"**Description:** {risk.description}")
                report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def _generate_html(assessment: Assessment) -> str:
        """Generate HTML report."""
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append("<title>EAIFCH Assessment Report</title>")
        html.append("<style>")
        html.append("""
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 40px auto; padding: 20px; }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            .score-card { background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }
            .score-large { font-size: 48px; font-weight: bold; color: #3498db; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #34495e; color: white; }
            .violation { border-left: 4px solid #e74c3c; padding-left: 15px; margin: 15px 0; }
            .critical { border-left-color: #c0392b; }
            .high { border-left-color: #e67e22; }
            .medium { border-left-color: #f39c12; }
            .low { border-left-color: #3498db; }
            .badge { padding: 4px 8px; border-radius: 4px; color: white; font-size: 12px; }
            .badge-critical { background-color: #c0392b; }
            .badge-high { background-color: #e67e22; }
            .badge-medium { background-color: #f39c12; }
            .badge-low { background-color: #3498db; }
        """)
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        html.append("<h1>EAIFCH Ethical Assessment Report</h1>")
        html.append(f"<p><strong>Project:</strong> {assessment.project_name}</p>")
        html.append(f"<p><strong>Date:</strong> {assessment.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        html.append("<div class='score-card'>")
        html.append("<div class='score-large'>{:.1f}/100</div>".format(assessment.overall_score))
        html.append("<div>Overall Ethical Compliance Score</div>")
        html.append("</div>")
        
        # Category scores table
        html.append("<h2>Category Scores</h2>")
        html.append("<table>")
        html.append("<tr><th>Category</th><th>Score</th><th>Status</th></tr>")
        for category, score in assessment.category_scores.items():
            status = assessment.get_category_status(category)
            html.append(f"<tr><td>{category.replace('_', ' ').title()}</td><td>{score:.1f}/100</td><td>{status.title()}</td></tr>")
        html.append("</table>")
        
        # Violations
        if assessment.violations:
            html.append(f"<h2>Violations ({len(assessment.violations)})</h2>")
            for violation in assessment.violations:
                severity = violation['severity']
                html.append(f"<div class='violation {severity}'>")
                html.append(f"<span class='badge badge-{severity}'>{severity.upper()}</span>")
                html.append(f"<h3>{violation['principle_name']}</h3>")
                html.append(f"<p>{violation['description']}</p>")
                html.append("</div>")
        
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
