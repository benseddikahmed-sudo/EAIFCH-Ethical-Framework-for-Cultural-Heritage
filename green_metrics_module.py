# ============================================================================
# Fichier: module_1_ethical_assessment/core/green_metrics.py
# ============================================================================

"""
Tracking de métriques environnementales (Green Coding).
Mesure de l'empreinte carbone et énergétique des opérations.
"""

import psutil
import time
from typing import Dict, Optional, List
from datetime import datetime
from functools import wraps
import json


class GreenMetricsTracker:
    """
    Tracker de métriques environnementales pour Green Coding.
    
    Mesure:
    - Consommation CPU
    - Usage mémoire
    - Temps d'exécution
    - Estimation CO₂
    - Comparaisons Python vs Rust
    """
    
    # Facteurs de conversion (moyennes globales)
    CO2_PER_KWH = 0.475  # kg CO₂ par kWh (moyenne mondiale)
    CPU_TDP_WATTS = 65   # TDP moyen CPU (watts)
    
    def __init__(self, enable_logging: bool = True):
        """
        Initialiser le tracker.
        
        Args:
            enable_logging: Activer logging des métriques
        """
        self.enable_logging = enable_logging
        self.metrics_history: List[Dict] = []
        self.session_start = datetime.now()
        
    def measure_operation(self, operation_name: str):
        """
        Décorateur pour mesurer automatiquement une opération.
        
        Usage:
            @tracker.measure_operation("assessment_scoring")
            def calculate_score(...):
                ...
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Mesures avant
                process = psutil.Process()
                cpu_start = process.cpu_percent(interval=0.1)
                mem_start = process.memory_info().rss / 1024 / 1024  # MB
                time_start = time.perf_counter()
                
                # Exécuter fonction
                result = func(*args, **kwargs)
                
                # Mesures après
                time_end = time.perf_counter()
                cpu_end = process.cpu_percent(interval=0.1)
                mem_end = process.memory_info().rss / 1024 / 1024  # MB
                
                # Calculer métriques
                duration = time_end - time_start
                cpu_avg = (cpu_start + cpu_end) / 2
                mem_used = mem_end - mem_start
                
                # Estimer consommation énergétique
                energy_wh = self._estimate_energy(duration, cpu_avg)
                co2_g = self._estimate_co2(energy_wh)
                
                metrics = {
                    'operation': operation_name,
                    'timestamp': datetime.now().isoformat(),
                    'duration_seconds': round(duration, 6),
                    'cpu_percent': round(cpu_avg, 2),
                    'memory_mb': round(mem_used, 2),
                    'energy_wh': round(energy_wh, 6),
                    'co2_grams': round(co2_g, 6),
                    'function': func.__name__
                }
                
                if self.enable_logging:
                    self.metrics_history.append(metrics)
                
                return result
            
            return wrapper
        return decorator
    
    def _estimate_energy(self, duration_seconds: float, cpu_percent: float) -> float:
        """
        Estimer la consommation énergétique en Wh.
        
        Args:
            duration_seconds: Durée de l'opération
            cpu_percent: Utilisation CPU moyenne
            
        Returns:
            Énergie consommée en Wh
        """
        # Puissance = TDP × (CPU% / 100)
        power_watts = self.CPU_TDP_WATTS * (cpu_percent / 100)
        
        # Énergie = Puissance × Temps (en heures)
        energy_wh = power_watts * (duration_seconds / 3600)
        
        return energy_wh
    
    def _estimate_co2(self, energy_wh: float) -> float:
        """
        Estimer les émissions CO₂ en grammes.
        
        Args:
            energy_wh: Énergie en Wh
            
        Returns:
            CO₂ en grammes
        """
        # Convertir Wh en kWh
        energy_kwh = energy_wh / 1000
        
        # CO₂ = énergie × facteur
        co2_kg = energy_kwh * self.CO2_PER_KWH
        co2_g = co2_kg * 1000
        
        return co2_g
    
    def get_session_summary(self) -> Dict:
        """
        Obtenir un résumé des métriques de la session.
        
        Returns:
            Dictionnaire avec statistiques agrégées
        """
        if not self.metrics_history:
            return {
                'message': 'No metrics recorded',
                'operations_count': 0
            }
        
        total_duration = sum(m['duration_seconds'] for m in self.metrics_history)
        total_energy = sum(m['energy_wh'] for m in self.metrics_history)
        total_co2 = sum(m['co2_grams'] for m in self.metrics_history)
        avg_cpu = sum(m['cpu_percent'] for m in self.metrics_history) / len(self.metrics_history)
        max_memory = max(m['memory_mb'] for m in self.metrics_history)
        
        return {
            'session_start': self.session_start.isoformat(),
            'session_duration': (datetime.now() - self.session_start).total_seconds(),
            'operations_count': len(self.metrics_history),
            'total_duration_seconds': round(total_duration, 3),
            'total_energy_wh': round(total_energy, 6),
            'total_co2_grams': round(total_co2, 6),
            'average_cpu_percent': round(avg_cpu, 2),
            'peak_memory_mb': round(max_memory, 2),
            'operations': self.metrics_history
        }
    
    def compare_implementations(
        self,
        python_metrics: Dict,
        rust_metrics: Dict
    ) -> Dict:
        """
        Comparer les métriques Python vs Rust.
        
        Args:
            python_metrics: Métriques implémentation Python
            rust_metrics: Métriques implémentation Rust
            
        Returns:
            Rapport de comparaison détaillé
        """
        speedup = python_metrics['duration_seconds'] / rust_metrics['duration_seconds']
        energy_reduction = ((python_metrics['energy_wh'] - rust_metrics['energy_wh']) / 
                           python_metrics['energy_wh']) * 100
        co2_reduction = ((python_metrics['co2_grams'] - rust_metrics['co2_grams']) / 
                        python_metrics['co2_grams']) * 100
        memory_reduction = ((python_metrics['memory_mb'] - rust_metrics['memory_mb']) / 
                           python_metrics['memory_mb']) * 100
        
        return {
            'comparison_date': datetime.now().isoformat(),
            'operation': python_metrics.get('operation', 'unknown'),
            
            'python': python_metrics,
            'rust': rust_metrics,
            
            'improvements': {
                'speedup_factor': round(speedup, 2),
                'energy_reduction_percent': round(energy_reduction, 2),
                'co2_reduction_percent': round(co2_reduction, 2),
                'memory_reduction_percent': round(memory_reduction, 2)
            },
            
            'annual_impact_10k_users': {
                'co2_saved_kg': round((python_metrics['co2_grams'] - rust_metrics['co2_grams']) * 10000 / 1000, 2),
                'energy_saved_kwh': round((python_metrics['energy_wh'] - rust_metrics['energy_wh']) * 10000 / 1000, 2),
                'equivalent_km_car': round((python_metrics['co2_grams'] - rust_metrics['co2_grams']) * 10000 / 1000 / 0.2, 0)
            },
            
            'recommendation': 'Use Rust implementation' if speedup > 2 else 'Python acceptable'
        }
    
    def export_metrics(self, filepath: str, format: str = 'json'):
        """
        Exporter les métriques vers un fichier.
        
        Args:
            filepath: Chemin du fichier de sortie
            format: Format d'export ('json' ou 'csv')
        """
        summary = self.get_session_summary()
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump(summary, f, indent=2)
        elif format == 'csv':
            import csv
            with open(filepath, 'w', newline='') as f:
                if self.metrics_history:
                    writer = csv.DictWriter(f, fieldnames=self.metrics_history[0].keys())
                    writer.writeheader()
                    writer.writerows(self.metrics_history)
    
    def reset(self):
        """Réinitialiser les métriques."""
        self.metrics_history = []
        self.session_start = datetime.now()
    
    def get_carbon_intensity_estimate(self, region: str = 'global') -> float:
        """
        Obtenir l'intensité carbone pour une région.
        
        Args:
            region: Région géographique
            
        Returns:
            Intensité carbone en kg CO₂/kWh
        """
        # Intensités carbone par région (2024)
        intensities = {
            'global': 0.475,
            'france': 0.057,
            'germany': 0.338,
            'uk': 0.233,
            'usa': 0.389,
            'china': 0.555,
            'india': 0.708,
            'australia': 0.610,
            'brazil': 0.082,
            'canada': 0.120
        }
        
        return intensities.get(region.lower(), 0.475)
    
    def benchmark_operation(
        self,
        func,
        iterations: int = 100,
        warmup: int = 10
    ) -> Dict:
        """
        Benchmarker une opération avec plusieurs itérations.
        
        Args:
            func: Fonction à benchmarker
            iterations: Nombre d'itérations
            warmup: Nombre d'itérations de chauffe
            
        Returns:
            Statistiques de benchmark
        """
        # Warm-up
        for _ in range(warmup):
            func()
        
        # Mesures
        durations = []
        energies = []
        co2s = []
        
        for _ in range(iterations):
            process = psutil.Process()
            cpu_start = process.cpu_percent(interval=0.01)
            time_start = time.perf_counter()
            
            func()
            
            time_end = time.perf_counter()
            cpu_end = process.cpu_percent(interval=0.01)
            
            duration = time_end - time_start
            cpu_avg = (cpu_start + cpu_end) / 2
            energy = self._estimate_energy(duration, cpu_avg)
            co2 = self._estimate_co2(energy)
            
            durations.append(duration)
            energies.append(energy)
            co2s.append(co2)
        
        import numpy as np
        
        return {
            'iterations': iterations,
            'duration': {
                'mean': round(np.mean(durations), 6),
                'median': round(np.median(durations), 6),
                'std': round(np.std(durations), 6),
                'min': round(np.min(durations), 6),
                'max': round(np.max(durations), 6)
            },
            'energy_wh': {
                'mean': round(np.mean(energies), 8),
                'total': round(np.sum(energies), 6)
            },
            'co2_grams': {
                'mean': round(np.mean(co2s), 8),
                'total': round(np.sum(co2s), 6)
            }
        }


# ============================================================================
# Exemple d'utilisation
# ============================================================================

if __name__ == "__main__":
    import numpy as np
    
    # Créer tracker
    tracker = GreenMetricsTracker()
    
    # Exemple 1: Mesurer une opération
    @tracker.measure_operation("example_computation")
    def compute_something():
        """Simulation de calcul."""
        data = np.random.rand(1000, 1000)
        result = np.linalg.inv(data)
        return result
    
    print("🌱 Green Metrics Tracker Demo")
    print("=" * 60)
    
    # Exécuter opération
    result = compute_something()
    print("\n✅ Opération exécutée")
    
    # Résumé
    summary = tracker.get_session_summary()
    print(f"\n📊 Session Summary:")
    print(f"  Operations: {summary['operations_count']}")
    print(f"  Total duration: {summary['total_duration_seconds']:.3f}s")
    print(f"  Total energy: {summary['total_energy_wh']:.6f} Wh")
    print(f"  Total CO₂: {summary['total_co2_grams']:.6f} g")
    print(f"  Avg CPU: {summary['average_cpu_percent']:.2f}%")
    print(f"  Peak memory: {summary['peak_memory_mb']:.2f} MB")
    
    # Exemple 2: Comparaison Python vs Rust (simulée)
    python_metrics = {
        'operation': 'sensitivity_scoring',
        'duration_seconds': 0.047,
        'energy_wh': 0.0008,
        'co2_grams': 0.00038,
        'memory_mb': 23.5
    }
    
    rust_metrics = {
        'operation': 'sensitivity_scoring',
        'duration_seconds': 0.000014,
        'energy_wh': 0.0000013,
        'co2_grams': 0.00000062,
        'memory_mb': 2.1
    }
    
    comparison = tracker.compare_implementations(python_metrics, rust_metrics)
    print(f"\n🦀 Python vs Rust Comparison:")
    print(f"  Speedup: {comparison['improvements']['speedup_factor']}x")
    print(f"  Energy reduction: {comparison['improvements']['energy_reduction_percent']:.1f}%")
    print(f"  CO₂ reduction: {comparison['improvements']['co2_reduction_percent']:.1f}%")
    print(f"  Memory reduction: {comparison['improvements']['memory_reduction_percent']:.1f}%")
    print(f"\n🌍 Annual Impact (10K users):")
    print(f"  CO₂ saved: {comparison['annual_impact_10k_users']['co2_saved_kg']} kg")
    print(f"  Equivalent km car avoided: {comparison['annual_impact_10k_users']['equivalent_km_car']:,.0f} km")
    
    # Exporter métriques
    tracker.export_metrics('green_metrics_report.json')
    print(f"\n💾 Metrics exported to: green_metrics_report.json")
