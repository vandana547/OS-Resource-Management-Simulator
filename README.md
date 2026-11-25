# OS Resource Management Simulator

## Overview
The OS Resource Management Simulator is a Python-based desktop application designed to simulate and visualize major operating system resource-management concepts. It provides an interactive graphical interface for understanding CPU scheduling, memory allocation, deadlock management, disk scheduling and system utilities.

## Features

### 1. CPU Scheduling
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin
- Performance metrics:
  - Completion Time
  - Turnaround Time
  - Waiting Time
  - Response Time

### 2. Memory Management
- Memory allocation simulation
- First Fit
- Best Fit
- Worst Fit
- Allocation status
- Internal fragmentation analysis
- Memory block visualization

### 3. Deadlock Management
- Banker's Algorithm
- Allocation Matrix
- Maximum Matrix
- Need Matrix
- Available Resources
- Safe Sequence detection
- System safety analysis

### 4. Disk Scheduling
- Disk scheduling algorithm simulation
- Head movement analysis
- Algorithm comparison and visualization

### 5. System Tools
- Python and Bash integration
- Operating system utilities
- System information and command execution

### 6. Reports and Analytics
- Performance visualization
- CPU scheduling comparison charts
- Report export
- Activity log viewing

## Technologies Used
- Python
- Tkinter
- Matplotlib
- Bash
- Operating System Algorithms

## Project Structure

```text
OS_Resource_Management_Simulator/
│
├── main.py
├── requirements.txt
│
├── modules/
│   ├── cpu_scheduling.py
│   ├── memory_management.py
│   ├── deadlock_management.py
│   ├── disk_scheduling.py
│   ├── system_tools.py
│   └── reports.py
│
├── data/
├── logs/
├── reports/
├── scripts/
├── Screenshots/
└── utils/
```

## Installation

1. Install Python.
2. Clone or download the project repository.
3. Open the project directory in VS Code.
4. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Execution

Run the following command from the project directory:

```bash
python main.py
```

## Objective

The objective of this project is to demonstrate the implementation and analysis of major operating system resource-management algorithms through a user-friendly desktop application.

## Author
OS Resource Management Simulator - Capstone Project
