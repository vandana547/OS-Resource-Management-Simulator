import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportsUI:

    def __init__(self, parent):
        self.parent = parent
        self.build_ui()

    def build_ui(self):

        container = tk.Frame(self.parent, bg="#f1f5f9")
        container.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(container, bg="white", bd=1, relief="solid")
        header.pack(fill="x", padx=20, pady=10)

        tk.Label(
            header,
            text="Performance Analytics & Reports",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        tk.Label(
            header,
            text="Analyse algorithms and generate system reports",
            font=("Arial", 10),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # Summary section
        summary = tk.Frame(container, bg="#f1f5f9")
        summary.pack(fill="x", padx=20, pady=10)

        cards = [
            ("CPU", "Scheduling"),
            ("MEMORY", "Allocation"),
            ("DEADLOCK", "Safety Analysis"),
            ("DISK", "Scheduling")
        ]

        for i, (title, subtitle) in enumerate(cards):

            card = tk.Frame(
                summary,
                bg="white",
                bd=1,
                relief="solid"
            )

            card.grid(
                row=0,
                column=i,
                padx=5,
                pady=5,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#0f766e"
            ).pack(pady=(15, 5))

            tk.Label(
                card,
                text=subtitle,
                font=("Arial", 10),
                bg="white",
                fg="#64748b"
            ).pack(pady=(0, 15))

            summary.columnconfigure(i, weight=1)

        # Analytics section
        analytics = tk.Frame(container, bg="white", bd=1, relief="solid")
        analytics.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            analytics,
            text="CPU Scheduling Performance Comparison",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        tk.Label(
            analytics,
            text="Illustrative sample data (not live simulation results)",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w", padx=15)

        self.create_chart(analytics)

        # Actions
        actions = tk.Frame(container, bg="#f1f5f9")
        actions.pack(fill="x", padx=20, pady=10)

        tk.Button(
            actions,
            text="Export Report",
            command=self.export_report,
            bg="#0f766e",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="View Activity Logs",
            command=self.view_logs,
            bg="#14213d",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side="left", padx=5)

    # -------------------------------------
    # Chart creation
    # -------------------------------------

    def create_chart(self, parent):

        self.fig, self.ax = plt.subplots(figsize=(7, 4))

        algorithms = ["FCFS", "SJF", "Priority", "Round Robin"]

        # Illustrative values for demonstration purposes
        waiting_time = [8, 5, 7, 10]
        turnaround_time = [15, 11, 14, 18]

        x = range(len(algorithms))
        width = 0.35

        self.ax.bar(
            [i - width / 2 for i in x],
            waiting_time,
            width,
            label="Waiting Time"
        )

        self.ax.bar(
            [i + width / 2 for i in x],
            turnaround_time,
            width,
            label="Turnaround Time"
        )

        self.ax.set_xticks(list(x))
        self.ax.set_xticklabels(algorithms)

        self.ax.set_ylabel("Time Units")
        self.ax.set_title("Scheduling Algorithm Comparison")
        self.ax.legend()

        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=parent
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # -------------------------------------
    # Export report
    # -------------------------------------

    def export_report(self):

        os.makedirs("reports", exist_ok=True)

        filename = (
            "reports/performance_report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        report = f"""
OS RESOURCE MANAGEMENT SIMULATOR
PERFORMANCE ANALYTICS REPORT

Generated: {datetime.now()}

========================================
PROJECT MODULES
========================================

1. CPU Scheduling
2. Memory Management
3. Deadlock Management
4. Disk Scheduling
5. System Tools
6. Performance Analytics

========================================
ILLUSTRATIVE CPU SCHEDULING DATA
========================================

FCFS:
Average Waiting Time: 8
Average Turnaround Time: 15

SJF:
Average Waiting Time: 5
Average Turnaround Time: 11

Priority:
Average Waiting Time: 7
Average Turnaround Time: 14

Round Robin:
Average Waiting Time: 10
Average Turnaround Time: 18

NOTE:
These are illustrative sample values.
They are not generated from a live simulation.

========================================
CONCLUSION
========================================

This simulator demonstrates major operating
system resource management concepts.

CPU scheduling algorithms can be compared
using waiting time and turnaround time.

Memory allocation strategies demonstrate
resource allocation and fragmentation.

Deadlock management demonstrates safety
analysis using the Banker's algorithm.

Disk scheduling demonstrates optimization
of disk head movement.

Python and Bash integration provides
system information and utility functions.
"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        messagebox.showinfo(
            "Report Exported",
            f"Report saved successfully:\n{filename}"
        )

    # -------------------------------------
    # View logs
    # -------------------------------------

    def view_logs(self):

        log_files = []

        if os.path.exists("logs"):

            log_files = [
                f for f in os.listdir("logs")
                if f.endswith(".log")
            ]

        window = tk.Toplevel(self.parent)
        window.title("Activity Logs")
        window.geometry("750x500")
        window.configure(bg="#f1f5f9")

        tk.Label(
            window,
            text="Activity Logs",
            font=("Arial", 16, "bold"),
            bg="#f1f5f9"
        ).pack(pady=10)

        text = tk.Text(
            window,
            bg="#0f172a",
            fg="#e2e8f0",
            font=("Consolas", 10)
        )

        text.pack(fill="both", expand=True, padx=15, pady=15)

        if not log_files:

            text.insert(
                tk.END,
                "No log files found in the logs folder."
            )

        else:

            for filename in log_files:

                filepath = os.path.join("logs", filename)

                text.insert(
                    tk.END,
                    f"\n{'=' * 60}\n"
                    f"FILE: {filename}\n"
                    f"{'=' * 60}\n"
                )

                try:

                    with open(
                        filepath,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        text.insert(tk.END, f.read() + "\n")

                except Exception as e:

                    text.insert(
                        tk.END,
                        f"Unable to read file: {e}\n"
                    )

        text.config(state="disabled")