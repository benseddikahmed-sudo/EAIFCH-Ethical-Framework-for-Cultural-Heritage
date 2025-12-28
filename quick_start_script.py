#!/usr/bin/env python
"""
EAIFCH Quick Start Script

This script provides an interactive way to get started with EAIFCH.
It creates a sample project and runs an assessment with explanations.
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress
import time

console = Console()


def print_welcome():
    """Print welcome message."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Welcome to EAIFCH![/bold cyan]\n\n"
        "The Ethical AI Framework for Cultural Heritage\n"
        "Let's assess your first project together! 🏛️🤖",
        border_style="cyan"
    ))


def collect_project_info():
    """Collect basic project information interactively."""
    console.print("\n[bold yellow]Step 1: Tell us about your project[/bold yellow]\n")
    
    project_data = {}
    
    project_data["name"] = Prompt.ask(
        "[cyan]Project name[/cyan]",
        default="My Cultural Heritage AI Project"
    )
    
    project_data["description"] = Prompt.ask(
        "[cyan]Brief description[/cyan]",
        default="AI system for cultural heritage management"
    )
    
    project_data["location"] = Prompt.ask(
        "[cyan]Location[/cyan]",
        default="Museum/Heritage Site"
    )
    
    heritage_type = Prompt.ask(
        "[cyan]Heritage type[/cyan]",
        choices=["tangible", "intangible", "mixed"],
        default="tangible"
    )
    project_data["heritage_type"] = heritage_type
    
    console.print("\n[dim]Great! Now let's check some ethical aspects...[/dim]\n")
    
    return project_data


def collect_ethical_indicators():
    """Collect ethical compliance indicators."""
    console.print("[bold yellow]Step 2: Ethical Compliance Check[/bold yellow]\n")
    
    indicators = {}
    
    questions = [
        ("data_encryption", "Is sensitive data encrypted?", True),
        ("bias_testing", "Have you tested for algorithmic bias?", False),
        ("human_oversight", "Is there human oversight of AI decisions?", True),
        ("cultural_expert_review", "Has a cultural expert reviewed the project?", True),
        ("model_explainability", "Can you explain how the AI makes decisions?", False),
        ("gdpr_compliant", "Is the project GDPR compliant (if applicable)?", True),
        ("accessibility_wcag", "Does it meet WCAG accessibility standards?", False),
        ("indigenous_consultation", "Have you consulted indigenous communities (if relevant)?", False),
    ]
    
    console.print("[dim]Answer these questions about your project:[/dim]\n")
    
    for key, question, default in questions:
        answer = Confirm.ask(f"[cyan]{question}[/cyan]", default=default)
        indicators[key] = answer
    
    return indicators


def run_assessment(project_data, indicators):
    """Run the assessment with progress indication."""
    console.print("\n[bold yellow]Step 3: Running Ethical Assessment[/bold yellow]\n")
    
    # Import here to show installation is complete
    try:
        from eaifch import EthicalFramework, CulturalHeritageProject
    except ImportError:
        console.print("[red]Error: EAIFCH not installed properly[/red]")
        console.print("Run: pip install -e .")
        return None
    
    # Merge data
    full_data = {**project_data, **indicators}
    
    # Add defaults for other fields
    full_data.setdefault("ai_techniques", ["nlp", "computer_vision"])
    full_data.setdefault("contains_sensitive_data", False)
    full_data.setdefault("data_collection_justified", True)
    full_data.setdefault("access_control_implemented", True)
    full_data.setdefault("uses_training_data", True)
    full_data.setdefault("dataset_diversity_assessed", False)
    full_data.setdefault("documentation_complete", True)
    full_data.setdefault("access_barriers_assessed", True)
    
    # Create project
    project = CulturalHeritageProject(**full_data)
    
    # Initialize framework
    framework = EthicalFramework()
    
    # Run assessment with progress bar
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing project...", total=100)
        
        for i in range(100):
            time.sleep(0.02)  # Simulate processing
            progress.update(task, advance=1)
        
        assessment = framework.assess(project)
    
    console.print("\n[green]✓ Assessment complete![/green]\n")
    
    return assessment


def display_results(assessment):
    """Display assessment results."""
    console.print("[bold yellow]Step 4: Results[/bold yellow]\n")
    
    # Overall score
    score = assessment.overall_score
    score_color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
    
    console.print(Panel(
        f"[{score_color} bold]{score:.1f}/100[/{score_color} bold]\n\n"
        f"{'🎉 Excellent!' if score >= 85 else '👍 Good job!' if score >= 70 else '⚠️ Needs improvement' if score >= 50 else '❌ Critical issues'}",
        title="Overall Ethical Compliance Score",
        border_style=score_color
    ))
    
    # Category breakdown
    console.print("\n[bold]Category Breakdown:[/bold]\n")
    
    for category, cat_score in assessment.category_scores.items():
        emoji = "✅" if cat_score >= 70 else "⚠️" if cat_score >= 50 else "❌"
        color = "green" if cat_score >= 70 else "yellow" if cat_score >= 50 else "red"
        console.print(
            f"  {emoji} [{color}]{category.replace('_', ' ').title():30} {cat_score:6.1f}/100[/{color}]"
        )
    
    # Issues found
    if assessment.violations:
        console.print(f"\n[bold red]⚠️  {len(assessment.violations)} Issues Found:[/bold red]\n")
        
        for i, violation in enumerate(assessment.violations[:3], 1):  # Show top 3
            severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
            console.print(
                f"{severity_emoji.get(violation['severity'], '')} "
                f"[bold]{violation['principle_name']}[/bold]"
            )
            console.print(f"   {violation['description']}\n")
        
        if len(assessment.violations) > 3:
            console.print(f"[dim]... and {len(assessment.violations) - 3} more issues[/dim]\n")
    else:
        console.print("\n[green]✓ No violations detected![/green]\n")


def show_recommendations(assessment):
    """Show actionable recommendations."""
    console.print("\n[bold yellow]Step 5: Recommendations[/bold yellow]\n")
    
    recommendations = assessment.get_top_recommendations(3)
    
    if recommendations:
        console.print("[cyan]Top 3 actions to improve your score:[/cyan]\n")
        
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
            console.print(f"{priority_emoji.get(rec['priority'], '')} [bold]{i}. {rec['principle']}[/bold]")
            console.print(f"   [dim]Issue:[/dim] {rec['issue']}")
            console.print(f"   [dim]Action:[/dim] {rec['action']}")
            console.print(f"   [dim]Difficulty:[/dim] {rec['difficulty']} | "
                         f"[dim]Expected improvement:[/dim] +{rec.get('effectiveness', 0)*10:.0f} points\n")
    else:
        console.print("[green]No recommendations needed - excellent work![/green]\n")


def show_next_steps():
    """Show next steps."""
    console.print("\n[bold cyan]What's Next?[/bold cyan]\n")
    
    console.print("📚 [bold]Learn More:[/bold]")
    console.print("   • Read the documentation: docs/")
    console.print("   • Explore examples: python examples/01_basic_assessment.py")
    console.print("   • View all principles: eaifch principles\n")
    
    console.print("🔧 [bold]Try the CLI:[/bold]")
    console.print("   • Create template: eaifch template my_project.json")
    console.print("   • Run assessment: eaifch assess my_project.json")
    console.print("   • Generate report: eaifch assess project.json -o report.html -f html\n")
    
    console.print("🚀 [bold]Start API Server:[/bold]")
    console.print("   • eaifch serve")
    console.print("   • Access at: http://localhost:8000\n")
    
    console.print("🤝 [bold]Contribute:[/bold]")
    console.print("   • Star us on GitHub!")
    console.print("   • Report issues or suggest features")
    console.print("   • Share your use cases\n")


def main():
    """Main quick start flow."""
    print_welcome()
    
    # Check if user wants interactive mode
    if not Confirm.ask("\n[cyan]Would you like to run an interactive assessment?[/cyan]", default=True):
        console.print("\n[yellow]No problem! Here are some quick commands to get started:[/yellow]\n")
        console.print("  eaifch template my_project.json")
        console.print("  eaifch assess my_project.json")
        console.print("  python examples/01_basic_assessment.py\n")
        return
    
    try:
        # Collect information
        project_data = collect_project_info()
        indicators = collect_ethical_indicators()
        
        # Run assessment
        assessment = run_assessment(project_data, indicators)
        
        if assessment:
            # Display results
            display_results(assessment)
            show_recommendations(assessment)
            
            # Save report?
            if Confirm.ask("\n[cyan]Would you like to save a detailed report?[/cyan]", default=True):
                filename = Prompt.ask(
                    "[cyan]Filename[/cyan]",
                    default="assessment_report.txt"
                )
                
                from eaifch.core.assessment import AssessmentReport
                report = AssessmentReport.generate(assessment, "text")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                console.print(f"\n[green]✓ Report saved to {filename}[/green]")
            
            # Show next steps
            show_next_steps()
            
            console.print("\n[bold cyan]Thank you for using EAIFCH![/bold cyan]")
            console.print("[dim]Together, we can ensure ethical AI in cultural heritage. 🏛️✨[/dim]\n")
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Assessment cancelled. Run the script again anytime![/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        console.print("[yellow]Please check the installation and try again.[/yellow]\n")


if __name__ == "__main__":
    main()
