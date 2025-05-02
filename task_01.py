from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes the 3D printing queue according to priorities and printer constraints

    Args:
        print_jobs: List of print jobs
        constraints: Printer constraints

    Returns:
        Dict with print order and total time
    """
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Sort by priority (from 1 to 3), then by print time in descending order
    jobs.sort(key=lambda job: (job.priority, -job.print_time))

    print_order = []
    total_time = 0
    i = 0

    while i < len(jobs):
        group = []
        group_volume = 0

        j = i
        while j < len(jobs) and len(group) < printer.max_items:
            if group_volume + jobs[j].volume <= printer.max_volume:
                group.append(jobs[j])
                group_volume += jobs[j].volume
                jobs[j] = None  # Mark as used
            j += 1

        # If nothing could be grouped (e.g., one job exceeds the constraint) — take it separately
        if not group:
            for k in range(i, len(jobs)):
                if jobs[k] is not None:
                    group = [jobs[k]]
                    jobs[k] = None
                    break

        # Add group to the print queue
        print_order.extend([job.id for job in group])
        total_time += max(job.print_time for job in group)

        # Remove used jobs
        jobs = [job for job in jobs if job is not None]

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Testing
def test_printing_optimization():
    # Test 1: Models with the same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Test 2: Models with different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # lab work
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # thesis project
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # personal project
    ]

    # Test 3: Exceeding volume constraints
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Test 1 (same priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\nTest 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\nTest 3 (exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

if __name__ == "__main__":
    test_printing_optimization()

