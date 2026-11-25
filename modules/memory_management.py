
import tkinter as tk
from tkinter import ttk, messagebox


class MemoryManagementUI:

    def __init__(self, parent):
        self.parent = parent
        self.blocks = []
        self.processes = []
        self.allocations = []
        self.build_ui()

    def build_ui(self):

        container = tk.Frame(self.parent, bg="#f1f5f9")
        container.pack(fill="both", expand=True)

        # Input card
        input_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        input_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            input_card,
            text="Memory & Process Input",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        form = tk.Frame(input_card, bg="white")
        form.pack(fill="x", padx=15, pady=10)

        tk.Label(form, text="Memory Blocks (MB)", bg="white").grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(form, text="Process Sizes (MB)", bg="white").grid(
            row=0, column=1, sticky="w"
        )

        self.blocks_entry = tk.Entry(form, width=35)
        self.processes_entry = tk.Entry(form, width=35)

        self.blocks_entry.grid(row=1, column=0, padx=10, pady=8)
        self.processes_entry.grid(row=1, column=1, padx=10, pady=8)

        self.blocks_entry.insert(0, "100,500,200,300,600")
        self.processes_entry.insert(0, "212,417,112,426")

        # Controls
        control_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        control_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            control_card,
            text="Allocation Strategy",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        controls = tk.Frame(control_card, bg="white")
        controls.pack(fill="x", padx=15, pady=10)

        self.algorithm = ttk.Combobox(
            controls,
            values=["First Fit", "Best Fit", "Worst Fit"],
            state="readonly",
            width=20
        )
        self.algorithm.set("First Fit")
        self.algorithm.pack(side="left", padx=10)

        tk.Button(
            controls,
            text="Allocate Memory",
            command=self.run_allocation,
            bg="#14213d",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=10)

        tk.Button(
            controls,
            text="Reset",
            command=self.reset,
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=10)

        # Results card
        result_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        result_card.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            result_card,
            text="Allocation Results",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        self.table = ttk.Treeview(
            result_card,
            columns=("PID", "Size", "Block", "BlockSize", "Status", "Fragment"),
            show="headings",
            height=5
        )

        headings = {
            "PID": "Process",
            "Size": "Process Size (MB)",
            "Block": "Block",
            "BlockSize": "Block Size (MB)",
            "Status": "Status",
            "Fragment": "Unused in Block (MB)"
        }

        for col, heading in headings.items():
            self.table.heading(col, text=heading)
            self.table.column(col, width=120, anchor="center")

        self.table.pack(fill="x", padx=10, pady=10)

        # Statistics
        self.stats = tk.Label(
            result_card,
            text="Enter memory blocks and processes, then allocate.",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#0f766e",
            justify="center"
        )
        self.stats.pack(pady=10)

        # Memory visualization
        tk.Label(
            result_card,
            text="Memory Block Visualization",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(pady=(5, 0))

        self.canvas = tk.Canvas(
            result_card,
            height=150,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(fill="x", padx=15, pady=10)

    def run_allocation(self):

        try:
            block_sizes = list(
                map(int, self.blocks_entry.get().split(","))
            )
            process_sizes = list(
                map(int, self.processes_entry.get().split(","))
            )

            if not block_sizes or not process_sizes:
                raise ValueError("Inputs cannot be empty.")

            if any(x <= 0 for x in block_sizes + process_sizes):
                raise ValueError("All memory sizes must be positive.")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Enter comma-separated positive integer sizes."
            )
            return

        algorithm = self.algorithm.get()

        # Every memory block is initially free
        available = block_sizes.copy()
        allocations = []

        for i, size in enumerate(process_sizes):

            chosen = -1

            if algorithm == "First Fit":

                for j in range(len(available)):
                    if available[j] >= size:
                        chosen = j
                        break

            elif algorithm == "Best Fit":

                candidates = [
                    j for j in range(len(available))
                    if available[j] >= size
                ]

                if candidates:
                    chosen = min(candidates, key=lambda j: available[j])

            elif algorithm == "Worst Fit":

                candidates = [
                    j for j in range(len(available))
                    if available[j] >= size
                ]

                if candidates:
                    chosen = max(candidates, key=lambda j: available[j])

            if chosen != -1:

                original_block_size = available[chosen]
                fragment = original_block_size - size

                # Static partition: block is assigned to one process.
                available[chosen] = -1

                allocations.append({
                    "pid": f"P{i+1}",
                    "size": size,
                    "block": f"B{chosen+1}",
                    "block_size": original_block_size,
                    "status": "Allocated",
                    "fragment": fragment,
                    "block_index": chosen
                })

            else:

                allocations.append({
                    "pid": f"P{i+1}",
                    "size": size,
                    "block": "-",
                    "block_size": "-",
                    "status": "Rejected",
                    "fragment": "-",
                    "block_index": -1
                })

        self.blocks = block_sizes
        self.processes = process_sizes
        self.allocations = allocations

        self.display_results()
        self.draw_memory()

    def display_results(self):

        for row in self.table.get_children():
            self.table.delete(row)

        allocated_count = 0
        total_process_memory = sum(self.processes)
        allocated_process_memory = 0
        total_fragment = 0

        for a in self.allocations:

            self.table.insert(
                "",
                "end",
                values=(
                    a["pid"],
                    a["size"],
                    a["block"],
                    a["block_size"],
                    a["status"],
                    a["fragment"]
                )
            )

            if a["status"] == "Allocated":
                allocated_count += 1
                allocated_process_memory += a["size"]
                total_fragment += a["fragment"]

        total_memory = sum(self.blocks)

        utilization = (
            allocated_process_memory / total_memory * 100
            if total_memory else 0
        )

        rejection_count = len(self.processes) - allocated_count

        self.stats.config(
            text=(
                f"Allocated: {allocated_count}/{len(self.processes)} processes  |  "
                f"Rejected: {rejection_count}  |  "
                f"Memory Utilization: {utilization:.2f}%  |  "
                f"Internal Fragmentation: {total_fragment} MB"
            )
        )

    def draw_memory(self):

        self.canvas.delete("all")

        if not self.blocks:
            return

        width = max(self.canvas.winfo_width(), 500)
        height = 100

        gap = 10
        total_gap = gap * (len(self.blocks) - 1)
        block_width = (width - 30 - total_gap) / len(self.blocks)

        for i, size in enumerate(self.blocks):

            x1 = 10 + i * (block_width + gap)
            x2 = x1 + block_width

            allocation = next(
                (
                    a for a in self.allocations
                    if a["block_index"] == i
                ),
                None
            )

            if allocation:
                color = "#0f766e"
                label = (
                    f"B{i+1}\n{size} MB\n"
                    f"{allocation['pid']}\n"
                    f"{allocation['size']} MB"
                )
            else:
                color = "#64748b"
                label = f"B{i+1}\n{size} MB\nFree"

            self.canvas.create_rectangle(
                x1, 20, x2, height,
                fill=color,
                outline="white",
                width=2
            )

            self.canvas.create_text(
                (x1+x2)/2,
                (height+20)/2,
                text=label,
                fill="white",
                font=("Arial", 9, "bold")
            )

    def reset(self):

        self.blocks_entry.delete(0, tk.END)
        self.processes_entry.delete(0, tk.END)

        self.blocks_entry.insert(0, "100,500,200,300,600")
        self.processes_entry.insert(0, "212,417,112,426")

        self.algorithm.set("First Fit")

        for row in self.table.get_children():
            self.table.delete(row)

        self.stats.config(
            text="Enter memory blocks and processes, then allocate."
        )

        self.canvas.delete("all")
        self.blocks = []
        self.processes = []
        self.allocations = []
