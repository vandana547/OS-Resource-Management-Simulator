
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def schedule(processes, algorithm, quantum=2):
    procs = [p.copy() for p in processes]
    n = len(procs)

    if algorithm == "FCFS":
        order = sorted(procs, key=lambda p: (p["at"], p["pid"]))
    else:
        order = None

    results = {}
    gantt = []
    time = 0
    completed = set()

    if algorithm in ("FCFS", "SJF", "Priority"):

        while len(completed) < n:

            available = [
                p for p in procs
                if p["pid"] not in completed and p["at"] <= time
            ]

            if not available:
                next_at = min(
                    p["at"] for p in procs
                    if p["pid"] not in completed
                )

                if time < next_at:
                    gantt.append(("Idle", time, next_at))
                    time = next_at

                continue

            if algorithm == "FCFS":
                p = min(available, key=lambda x: (x["at"], x["pid"]))

            elif algorithm == "SJF":
                p = min(available, key=lambda x: (x["bt"], x["at"], x["pid"]))

            else:
                p = min(
                    available,
                    key=lambda x: (x["priority"], x["at"], x["pid"])
                )

            start = time
            time += p["bt"]
            ct = time
            tat = ct - p["at"]
            wt = tat - p["bt"]
            rt = start - p["at"]

            gantt.append((p["pid"], start, time))

            results[p["pid"]] = {
                "ct": ct,
                "tat": tat,
                "wt": wt,
                "rt": rt
            }

            completed.add(p["pid"])

    elif algorithm == "Round Robin":

        queue = []
        remaining = {p["pid"]: p["bt"] for p in procs}
        first_start = {}
        arrival_sorted = sorted(procs, key=lambda p: (p["at"], p["pid"]))
        idx = 0

        while len(completed) < n:

            while idx < n and arrival_sorted[idx]["at"] <= time:
                queue.append(arrival_sorted[idx])
                idx += 1

            if not queue:
                next_at = arrival_sorted[idx]["at"]

                if time < next_at:
                    gantt.append(("Idle", time, next_at))
                    time = next_at

                continue

            p = queue.pop(0)
            pid = p["pid"]

            if pid not in first_start:
                first_start[pid] = time

            start = time
            run = min(quantum, remaining[pid])
            time += run
            remaining[pid] -= run

            gantt.append((pid, start, time))

            while idx < n and arrival_sorted[idx]["at"] <= time:
                queue.append(arrival_sorted[idx])
                idx += 1

            if remaining[pid] > 0:
                queue.append(p)
            else:
                completed.add(pid)
                ct = time
                tat = ct - p["at"]
                wt = tat - p["bt"]
                rt = first_start[pid] - p["at"]

                results[pid] = {
                    "ct": ct,
                    "tat": tat,
                    "wt": wt,
                    "rt": rt
                }

    avg_wt = sum(r["wt"] for r in results.values()) / n
    avg_tat = sum(r["tat"] for r in results.values()) / n
    avg_rt = sum(r["rt"] for r in results.values()) / n

    return results, gantt, avg_wt, avg_tat, avg_rt


class CPUSchedulingUI:

    def __init__(self, parent):
        self.parent = parent
        self.processes = []
        self.build_ui()

    def build_ui(self):

        container = tk.Frame(self.parent, bg="#f1f5f9")
        container.pack(fill="both", expand=True)

        # Input section
        input_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        input_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            input_card,
            text="Process Input",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        form = tk.Frame(input_card, bg="white")
        form.pack(fill="x", padx=15, pady=5)

        tk.Label(form, text="Arrival Time", bg="white").grid(row=0, column=0)
        tk.Label(form, text="Burst Time", bg="white").grid(row=0, column=1)
        tk.Label(form, text="Priority", bg="white").grid(row=0, column=2)

        self.at_entry = tk.Entry(form, width=15)
        self.bt_entry = tk.Entry(form, width=15)
        self.priority_entry = tk.Entry(form, width=15)

        self.at_entry.grid(row=1, column=0, padx=10, pady=10)
        self.bt_entry.grid(row=1, column=1, padx=10, pady=10)
        self.priority_entry.grid(row=1, column=2, padx=10, pady=10)

        self.at_entry.insert(0, "0,1,2,3")
        self.bt_entry.insert(0, "5,3,8,6")
        self.priority_entry.insert(0, "2,1,4,3")

        tk.Button(
            form,
            text="Load Processes",
            command=self.load_processes,
            bg="#0f766e",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).grid(row=1, column=3, padx=10)

        # Algorithm selection
        algorithm_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        algorithm_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            algorithm_card,
            text="Algorithm Selection",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        controls = tk.Frame(algorithm_card, bg="white")
        controls.pack(fill="x", padx=15, pady=10)

        self.algorithm = ttk.Combobox(
            controls,
            values=["FCFS", "SJF", "Priority", "Round Robin"],
            state="readonly",
            width=20
        )
        self.algorithm.set("FCFS")
        self.algorithm.pack(side="left", padx=10)

        tk.Label(
            controls,
            text="Quantum:",
            bg="white"
        ).pack(side="left")

        self.quantum_entry = tk.Entry(controls, width=8)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side="left", padx=10)

        tk.Button(
            controls,
            text="Run Simulation",
            command=self.run_simulation,
            bg="#14213d",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=10)

        # Results section
        result_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        result_card.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            result_card,
            text="Simulation Results",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        self.table = ttk.Treeview(
            result_card,
            columns=("PID", "AT", "BT", "CT", "TAT", "WT", "RT"),
            show="headings",
            height=6
        )

        headings = {
            "PID": "Process",
            "AT": "Arrival",
            "BT": "Burst",
            "CT": "Completion",
            "TAT": "Turnaround",
            "WT": "Waiting",
            "RT": "Response"
        }

        for col, heading in headings.items():
            self.table.heading(col, text=heading)
            self.table.column(col, width=90, anchor="center")

        self.table.pack(fill="x", padx=10, pady=10)

        self.summary = tk.Label(
            result_card,
            text="Load processes and run a simulation.",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#0f766e"
        )
        self.summary.pack(pady=10)

        self.chart_frame = tk.Frame(result_card, bg="white")
        self.chart_frame.pack(fill="both", expand=True)

    def load_processes(self):

        try:
            ats = list(map(int, self.at_entry.get().split(",")))
            bts = list(map(int, self.bt_entry.get().split(",")))
            priorities = list(map(int, self.priority_entry.get().split(",")))

            if not ats or len(ats) != len(bts) or len(ats) != len(priorities):
                raise ValueError("Input lists must have equal lengths.")

            if any(x < 0 for x in ats):
                raise ValueError("Arrival times cannot be negative.")

            if any(x <= 0 for x in bts):
                raise ValueError("Burst times must be positive.")

            self.processes = []

            for i in range(len(ats)):
                self.processes.append({
                    "pid": f"P{i+1}",
                    "at": ats[i],
                    "bt": bts[i],
                    "priority": priorities[i]
                })

            messagebox.showinfo(
                "Success",
                f"{len(self.processes)} processes loaded successfully."
            )

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def run_simulation(self):

        if not self.processes:
            messagebox.showerror(
                "Error",
                "Load processes before running simulation."
            )
            return

        algorithm = self.algorithm.get()

        try:
            quantum = int(self.quantum_entry.get())

            if quantum <= 0:
                raise ValueError("Quantum must be positive.")

        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid quantum.")
            return

        results, gantt, avg_wt, avg_tat, avg_rt = schedule(
            self.processes,
            algorithm,
            quantum
        )

        for row in self.table.get_children():
            self.table.delete(row)

        for p in self.processes:

            r = results[p["pid"]]

            self.table.insert(
                "",
                "end",
                values=(
                    p["pid"],
                    p["at"],
                    p["bt"],
                    r["ct"],
                    r["tat"],
                    r["wt"],
                    r["rt"]
                )
            )

        self.summary.config(
            text=(
                f"Average WT: {avg_wt:.2f}    |    "
                f"Average TAT: {avg_tat:.2f}    |    "
                f"Average RT: {avg_rt:.2f}"
            )
        )

        self.draw_gantt(gantt)

    def draw_gantt(self, gantt):

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(8, 2.4), dpi=100)
        ax = fig.add_subplot(111)

        for i, (pid, start, end) in enumerate(gantt):

            ax.barh(
                0,
                end - start,
                left=start,
                height=0.5
            )

            ax.text(
                (start + end) / 2,
                0,
                pid,
                ha="center",
                va="center",
                fontsize=9
            )

            ax.text(
                start,
                -0.35,
                str(start),
                ha="center",
                fontsize=8
            )

        if gantt:
            ax.text(
                gantt[-1][2],
                -0.35,
                str(gantt[-1][2]),
                ha="center",
                fontsize=8
            )

        ax.set_yticks([])
        ax.set_xlabel("Time")
        ax.set_title("Gantt Chart")
        ax.grid(axis="x", linestyle="--", alpha=0.4)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
