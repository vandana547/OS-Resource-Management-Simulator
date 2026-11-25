
import tkinter as tk
from tkinter import ttk, messagebox


class DeadlockManagementUI:

    def __init__(self, parent):
        self.parent = parent
        self.build_ui()

    def build_ui(self):

        container = tk.Frame(self.parent, bg="#f1f5f9")
        container.pack(fill="both", expand=True)

        # Input card
        input_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        input_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            input_card,
            text="Banker's Algorithm Input",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        tk.Label(
            input_card,
            text="Available Resources (comma separated)",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor="w", padx=15)

        self.available_entry = tk.Entry(input_card, font=("Arial", 11))
        self.available_entry.pack(fill="x", padx=15, pady=5)
        self.available_entry.insert(0, "3,3,2")

        matrices = tk.Frame(input_card, bg="white")
        matrices.pack(fill="both", expand=True, padx=15, pady=10)

        # Allocation Matrix
        allocation_frame = tk.Frame(matrices, bg="white")
        allocation_frame.pack(side="left", expand=True, fill="both", padx=5)

        tk.Label(
            allocation_frame,
            text="Allocation Matrix",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.allocation_text = tk.Text(
            allocation_frame,
            height=6,
            width=25,
            font=("Consolas", 10)
        )
        self.allocation_text.pack(fill="both", expand=True, pady=5)

        self.allocation_text.insert(
            "1.0",
            "0 1 0\n"
            "2 0 0\n"
            "3 0 2\n"
            "2 1 1\n"
            "0 0 2"
        )

        # Maximum Matrix
        maximum_frame = tk.Frame(matrices, bg="white")
        maximum_frame.pack(side="left", expand=True, fill="both", padx=5)

        tk.Label(
            maximum_frame,
            text="Maximum Matrix",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.maximum_text = tk.Text(
            maximum_frame,
            height=6,
            width=25,
            font=("Consolas", 10)
        )
        self.maximum_text.pack(fill="both", expand=True, pady=5)

        self.maximum_text.insert(
            "1.0",
            "7 5 3\n"
            "3 2 2\n"
            "9 0 2\n"
            "4 2 2\n"
            "5 3 3"
        )

        # Buttons
        button_frame = tk.Frame(input_card, bg="white")
        button_frame.pack(fill="x", padx=15, pady=10)

        tk.Button(
            button_frame,
            text="Check Safety",
            command=self.check_safety,
            bg="#14213d",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Reset",
            command=self.reset,
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        # Results
        result_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        result_card.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            result_card,
            text="Safety Analysis",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        self.result_label = tk.Label(
            result_card,
            text="Enter the resource matrices and click Check Safety.",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0f766e",
            wraplength=800,
            justify="left"
        )
        self.result_label.pack(anchor="w", padx=15, pady=10)

        # Need Matrix
        tk.Label(
            result_card,
            text="Need Matrix (Maximum - Allocation)",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.need_text = tk.Text(
            result_card,
            height=6,
            font=("Consolas", 10),
            state="disabled"
        )
        self.need_text.pack(fill="x", padx=15, pady=5)

        # Execution steps
        tk.Label(
            result_card,
            text="Safety Algorithm Execution",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.steps_text = tk.Text(
            result_card,
            height=8,
            font=("Consolas", 10),
            state="disabled"
        )
        self.steps_text.pack(fill="both", expand=True, padx=15, pady=5)

    def parse_matrix(self, text):

        rows = []

        for line in text.strip().splitlines():

            line = line.strip()

            if not line:
                continue

            row = list(map(int, line.replace(",", " ").split()))
            rows.append(row)

        return rows

    def check_safety(self):

        try:

            available = list(
                map(int, self.available_entry.get().replace(",", " ").split())
            )

            allocation = self.parse_matrix(
                self.allocation_text.get("1.0", tk.END)
            )

            maximum = self.parse_matrix(
                self.maximum_text.get("1.0", tk.END)
            )

            if not available or not allocation or not maximum:
                raise ValueError("Inputs cannot be empty.")

            if len(allocation) != len(maximum):
                raise ValueError(
                    "Allocation and Maximum matrices must have equal rows."
                )

            if any(len(row) != len(available) for row in allocation):
                raise ValueError(
                    "Allocation matrix columns must match Available resources."
                )

            if any(len(row) != len(available) for row in maximum):
                raise ValueError(
                    "Maximum matrix columns must match Available resources."
                )

            if any(x < 0 for x in available):
                raise ValueError("Available resources cannot be negative.")

            if any(x < 0 for row in allocation for x in row):
                raise ValueError("Allocation values cannot be negative.")

            if any(x < 0 for row in maximum for x in row):
                raise ValueError("Maximum values cannot be negative.")

            for i in range(len(allocation)):
                for j in range(len(available)):
                    if maximum[i][j] < allocation[i][j]:
                        raise ValueError(
                            "Maximum demand cannot be less than allocation."
                        )

        except ValueError as e:

            messagebox.showerror("Input Error", str(e))
            return

        n = len(allocation)
        m = len(available)

        need = [
            [
                maximum[i][j] - allocation[i][j]
                for j in range(m)
            ]
            for i in range(n)
        ]

        work = available.copy()
        finish = [False] * n
        safe_sequence = []
        steps = []

        steps.append(f"Initial Available/Work: {work}")
        steps.append("")

        # Banker's safety algorithm
        while True:

            found = False

            for i in range(n):

                if not finish[i]:

                    if all(need[i][j] <= work[j] for j in range(m)):

                        steps.append(
                            f"P{i} can execute. Need = {need[i]}"
                        )

                        work = [
                            work[j] + allocation[i][j]
                            for j in range(m)
                        ]

                        finish[i] = True
                        safe_sequence.append(f"P{i}")

                        steps.append(
                            f"P{i} finishes. Work becomes {work}"
                        )
                        steps.append("")

                        found = True
                        break

            if not found:
                break

        # Display Need Matrix
        self.need_text.config(state="normal")
        self.need_text.delete("1.0", tk.END)

        for i, row in enumerate(need):
            self.need_text.insert(
                tk.END,
                f"P{i}: {row}\n"
            )

        self.need_text.config(state="disabled")

        # Display steps
        self.steps_text.config(state="normal")
        self.steps_text.delete("1.0", tk.END)

        self.steps_text.insert(
            tk.END,
            "\n".join(steps)
        )

        self.steps_text.config(state="disabled")

        # Display final result
        if all(finish):

            sequence = " → ".join(safe_sequence)

            self.result_label.config(
                text=(
                    "SYSTEM IS SAFE\n\n"
                    f"Safe Sequence: {sequence}"
                ),
                fg="#0f766e"
            )

        else:

            unfinished = [
                f"P{i}" for i in range(n)
                if not finish[i]
            ]

            self.result_label.config(
                text=(
                    "SYSTEM IS UNSAFE\n\n"
                    "No safe sequence could be found.\n"
                    f"Unfinished processes: {', '.join(unfinished)}"
                ),
                fg="#dc2626"
            )

    def reset(self):

        self.available_entry.delete(0, tk.END)
        self.available_entry.insert(0, "3,3,2")

        self.allocation_text.delete("1.0", tk.END)
        self.allocation_text.insert(
            "1.0",
            "0 1 0\n"
            "2 0 0\n"
            "3 0 2\n"
            "2 1 1\n"
            "0 0 2"
        )

        self.maximum_text.delete("1.0", tk.END)
        self.maximum_text.insert(
            "1.0",
            "7 5 3\n"
            "3 2 2\n"
            "9 0 2\n"
            "4 2 2\n"
            "5 3 3"
        )

        self.result_label.config(
            text="Enter the resource matrices and click Check Safety.",
            fg="#0f766e"
        )

        self.need_text.config(state="normal")
        self.need_text.delete("1.0", tk.END)
        self.need_text.config(state="disabled")

        self.steps_text.config(state="normal")
        self.steps_text.delete("1.0", tk.END)
        self.steps_text.config(state="disabled")
