"""
Command Line Interface for EAIFCH

Provides CLI commands for ethical assessment and framework management.
"""

import click
import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from eaifch import (
    EthicalFramework,
    CulturalHeritageProject,
    __version__
)

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    EAIFCH - Ethical AI Framework for Cultural Heritage
    
    Command-line interface for ethical assessment of AI projects
    in cultural heritage management.
    """
    pass


@cli.command()
@click.argument('project_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for assessment report')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'html', 'markdown']), 
              default='text', help='Report format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def assess(project_file: str, output: Optional[str], format: str, verbose: bool):
    """
    Assess a cultural heritage AI project.
    
    PROJECT_FILE: JSON file containing project details
    
    Example:
        eaifch assess project.json -o report.txt -f text
    """
    console.print("\n[bold cyan]EAIFCH Ethical Assessment[/bold cyan]\n")
    
    try:
        # Load project data
        console.print(f"[yellow]Loading project from {project_file}...[/yellow]")
        with open(project_file, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        # Create project
        project = CulturalHeritageProject(**project_data)
        console.print(f"[green]✓[/green] Loaded project: [bold]{project.name}[/bold]\n")
        
        # Initialize framework
        if verbose:
            console.print("[yellow]Initializing EAIFCH framework...[/yellow]")
        framework = EthicalFramework()
        
        # Perform assessment
        console.print("[yellow]Running ethical assessment...[/yellow]")
        with console.status("[bold green]Analyzing project...", spinner="dots"):
            assessment = framework.assess(project)
        
        console.print("[green]✓[/green] Assessment complete!\n")
        
        # Display results
        _display_assessment_summary(assessment)
        
        # Generate and save report
        if output:
            report = framework.generate_report(assessment, format)
            output_path = Path(output)
            output_path.write_text(report.content, encoding='utf-8')
            console.print(f"\n[green]✓[/green] Report saved to: [bold]{output}[/bold]")
        
        # Show recommendations
        if verbose:
            _display_recommendations(assessment)
        
        # Exit code based on score
        if assessment.overall_score < 50:
            console.print("\n[red]⚠️  Critical ethical issues detected![/red]")
            raise click.exceptions.Exit(1)
        elif assessment.overall_score < 70:
            console.print("\n[yellow]⚠️  Some ethical concerns found.[/yellow]")
        else:
            console.print("\n[green]✓ Project meets ethical standards.[/green]")
        
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {project_file}[/red]")
        raise click.exceptions.Exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON in {project_file}[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise click.exceptions.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise click.exceptions.Exit(1)


@cli.command()
@click.argument('output_file', type=click.Path())
def template(output_file: str):
    """
    Generate a project template file.
    
    OUTPUT_FILE: Path for the template JSON file
    
    Example:
        eaifch template my_project.json
    """
    template_data = {
        "name": "My Cultural Heritage AI Project",
        "description": "Project description here",
        "location": "Museum/Site location",
        "heritage_type": "tangible",
        "ai_techniques": ["computer_vision", "nlp"],
        "stakeholders": ["Museum staff", "Curators", "IT team"],
        
        "data_encryption": False,
        "bias_testing": False,
        "indigenous_consultation": False,
        "model_explainability": False,
        "human_oversight": True,
        "environmental_impact_assessed": False,
        "gdpr_compliant": False,
        "accessibility_wcag": False,
        "cultural_expert_review": False,
        
        "contains_sensitive_data": False,
        "data_collection_justified": True,
        "access_control_implemented": False,
        "uses_training_data": False,
        "dataset_diversity_assessed": False,
        "documentation_complete": False,
        "access_barriers_assessed": False,
        "involves_indigenous_heritage": False,
        "contains_sacred_content": False,
        "religious_authority_approval": False,
        "processes_personal_data": False,
        "ip_rights_cleared": True,
        
        "budget": 100000,
        "timeline_months": 12,
        "team_size": 5
    }
    
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]✓[/green] Template created: [bold]{output_file}[/bold]")
    console.print("\nEdit this file with your project details, then run:")
    console.print(f"  [cyan]eaifch assess {output_file}[/cyan]")


@cli.command()
def principles():
    """
    List all 24 ethical principles.
    
    Example:
        eaifch principles
    """
    console.print("\n[bold cyan]EAIFCH Ethical Principles (24)[/bold cyan]\n")
    
    framework = EthicalFramework()
    
    for category_name, category in framework.taxonomy.categories.items():
        console.print(f"\n[bold yellow]{category.display_name}[/bold yellow] ({len(category.principles)} principles)")
        console.print(f"[dim]{category.description}[/dim]\n")
        
        for principle in category.principles:
            severity_color = {
                "critical": "red",
                "high": "orange3",
                "medium": "yellow",
                "low": "blue"
            }.get(principle.severity.value, "white")
            
            console.print(f"  [{severity_color}]●[/{severity_color}] [bold]{principle.name}[/bold] "
                         f"[dim]({principle.id})[/dim]")
            console.print(f"    {principle.description}\n")


@cli.command()
@click.argument('category', required=False)
def info(category: Optional[str]):
    """
    Display information about the framework or a specific category.
    
    CATEGORY: Optional category name (e.g., privacy_security)
    
    Example:
        eaifch info
        eaifch info privacy_security
    """
    framework = EthicalFramework()
    
    if category:
        # Show specific category
        cat = framework.taxonomy.get_category(category)
        if not cat:
            console.print(f"[red]Error: Unknown category '{category}'[/red]")
            console.print("\nAvailable categories:")
            for name in framework.taxonomy.categories.keys():
                console.print(f"  - {name}")
            raise click.exceptions.Exit(1)
        
        console.print(f"\n[bold cyan]{cat.display_name}[/bold cyan]\n")
        console.print(f"[dim]{cat.description}[/dim]\n")
        console.print(f"Weight: {cat.weight * 100:.1f}%")
        console.print(f"Principles: {len(cat.principles)}\n")
        
        for principle in cat.principles:
            console.print(f"[bold]{principle.name}[/bold] [{principle.severity.value}]")
            console.print(f"  {principle.description}\n")
    else:
        # Show framework overview
        stats = framework.get_statistics()
        
        console.print("\n[bold cyan]EAIFCH Framework Overview[/bold cyan]\n")
        console.print(f"Version: [bold]{__version__}[/bold]")
        console.print(f"Total Principles: [bold]{stats['total_principles']}[/bold]")
        console.print(f"Categories: [bold]{stats['total_categories']}[/bold]\n")
        
        table = Table(title="Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Principles", justify="center")
        table.add_column("Weight", justify="right")
        
        for name, info in stats['categories'].items():
            table.add_row(
                name.replace("_", " ").title(),
                str(info['principle_count']),
                f"{info['weight']*100:.1f}%"
            )
        
        console.print(table)


@cli.command()
@click.argument('assessment_files', nargs=-1, type=click.Path(exists=True))
def compare(assessment_files: tuple):
    """
    Compare multiple assessment results.
    
    ASSESSMENT_FILES: JSON files with assessment results
    
    Example:
        eaifch compare project1.json project2.json
    """
    if len(assessment_files) < 2:
        console.print("[red]Error: Need at least 2 assessment files to compare[/red]")
        raise click.exceptions.Exit(1)
    
    console.print("\n[bold cyan]Assessment Comparison[/bold cyan]\n")
    
    framework = EthicalFramework()
    assessments = []
    
    # Load and assess all projects
    for file in assessment_files:
        with open(file, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        project = CulturalHeritageProject(**project_data)
        assessment = framework.assess(project)
        assessments.append((project.name, assessment))
    
    # Create comparison table
    table = Table(title="Overall Scores")
    table.add_column("Project", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Status", justify="center")
    
    for name, assessment in assessments:
        score = assessment.overall_score
        status = "✓" if score >= 70 else "⚠️"
        color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
        table.add_row(name, f"[{color}]{score:.1f}/100[/{color}]", status)
    
    console.print(table)
    
    # Category comparison
    console.print("\n[bold]Category Comparison:[/bold]\n")
    
    categories = list(assessments[0][1].category_scores.keys())
    cat_table = Table()
    cat_table.add_column("Category", style="cyan")
    
    for name, _ in assessments:
        cat_table.add_column(name[:20], justify="right")
    
    for category in categories:
        row = [category.replace("_", " ").title()]
        for _, assessment in assessments:
            score = assessment.category_scores[category]
            color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
            row.append(f"[{color}]{score:.1f}[/{color}]")
        cat_table.add_row(*row)
    
    console.print(cat_table)


@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(host: str, port: int, reload: bool):
    """
    Start the EAIFCH API server.
    
    Example:
        eaifch serve
        eaifch serve --port 8080 --reload
    """
    console.print(f"\n[bold cyan]Starting EAIFCH API Server[/bold cyan]\n")
    console.print(f"Host: {host}")
    console.print(f"Port: {port}")
    console.print(f"URL: [bold]http://{host}:{port}[/bold]\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "eaifch.api:app",
            host=host,
            port=port,
            reload=reload
        )
    except ImportError:
        console.print("[red]Error: uvicorn not installed[/red]")
        console.print("Install API dependencies: pip install eaifch[api]")
        raise click.exceptions.Exit(1)


def _display_assessment_summary(assessment):
    """Display assessment summary."""
    # Overall score
    score_color = "green" if assessment.overall_score >= 70 else "yellow" if assessment.overall_score >= 50 else "red"
    console.print(Panel(
        f"[{score_color} bold]{assessment.overall_score:.1f}/100[/{score_color} bold]",
        title="Overall Ethical Compliance Score",
        border_style=score_color
    ))
    
    # Category table
    table = Table(title="\nCategory Breakdown")
    table.add_column("Category", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Status", justify="center")
    
    for category, score in assessment.category_scores.items():
        status = "✓" if score >= 70 else "⚠️" if score >= 50 else "✗"
        color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
        table.add_row(
            category.replace("_", " ").title(),
            f"[{color}]{score:.1f}[/{color}]",
            status
        )
    
    console.print(table)
    
    # Violations summary
    if assessment.violations:
        console.print(f"\n[bold red]⚠️  {len(assessment.violations)} Issues Found[/bold red]")
        critical = len([v for v in assessment.violations if v['severity'] == 'critical'])
        high = len([v for v in assessment.violations if v['severity'] == 'high'])
        if critical > 0:
            console.print(f"  • [red]{critical} Critical[/red]")
        if high > 0:
            console.print(f"  • [orange3]{high} High Priority[/orange3]")
    else:
        console.print("\n[green]✓ No violations detected![/green]")


def _display_recommendations(assessment):
    """Display recommendations."""
    recommendations = assessment.get_top_recommendations(5)
    
    if recommendations:
        console.print("\n[bold cyan]Top Recommendations:[/bold cyan]\n")
        for i, rec in enumerate(recommendations, 1):
            priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
            console.print(f"{priority_icon.get(rec['priority'], '')} [bold]{i}. {rec['principle']}[/bold]")
            console.print(f"   {rec['action']}")
            console.print(f"   Difficulty: {rec['difficulty']} | Effectiveness: {rec['effectiveness']*100:.0f}%\n")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
