
import tkinter as tk
from tkinter import ttk, messagebox


class DiskSchedulingUI:

    def __init__(self, parent):
        self.parent = parent
        self.requests = []
        self.sequence = []
        self.build_ui()

    def build_ui(self):

        container = tk.Frame(self.parent, bg="#f1f5f9")
        container.pack(fill="both", expand=True)

        # Input card
        input_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        input_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            input_card,
            text="Disk Request Input",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        form = tk.Frame(input_card, bg="white")
        form.pack(fill="x", padx=15, pady=10)

        fields = [
            ("Request Queue", "98,183,37,122,14,124,65,67"),
            ("Initial Head", "53"),
            ("Disk Size", "200")
        ]

        self.entries = {}

        for i, (label, value) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                bg="white",
                font=("Arial", 10, "bold")
            ).grid(row=0, column=i, sticky="w", padx=10)

            entry = tk.Entry(form, width=30)
            entry.grid(row=1, column=i, padx=10, pady=8)
            entry.insert(0, value)

            self.entries[label] = entry

        # Algorithm controls
        control_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        control_card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            control_card,
            text="Algorithm Selection",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        controls = tk.Frame(control_card, bg="white")
        controls.pack(fill="x", padx=15, pady=10)

        self.algorithm = ttk.Combobox(
            controls,
            values=["FCFS", "SSTF", "SCAN", "C-SCAN"],
            state="readonly",
            width=18
        )
        self.algorithm.set("FCFS")
        self.algorithm.pack(side="left", padx=10)

        self.direction = ttk.Combobox(
            controls,
            values=["Left", "Right"],
            state="readonly",
            width=12
        )
        self.direction.set("Right")
        self.direction.pack(side="left", padx=10)

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
            text="Simulation Results",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        self.result_label = tk.Label(
            result_card,
            text="Enter disk requests and run a simulation.",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0f766e",
            justify="left",
            wraplength=900
        )
        self.result_label.pack(anchor="w", padx=15, pady=10)

        # Service sequence
        tk.Label(
            result_card,
            text="Head Movement Sequence",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=5)

        self.sequence_text = tk.Text(
            result_card,
            height=3,
            font=("Consolas", 11),
            state="disabled"
        )
        self.sequence_text.pack(fill="x", padx=15, pady=5)

        # Visualization
        tk.Label(
            result_card,
            text="Head Movement Visualization",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=5)

        self.canvas = tk.Canvas(
            result_card,
            height=260,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)

    def calculate_fcfs(self, requests, head):

        sequence = [head] + requests
        return sequence

    def calculate_sstf(self, requests, head):

        pending = requests.copy()
        sequence = [head]
        current = head

        while pending:

            closest = min(
                pending,
                key=lambda x: abs(x - current)
            )

            sequence.append(closest)
            pending.remove(closest)
            current = closest

        return sequence

    def calculate_scan(self, requests, head, disk_size, direction):

        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])

        sequence = [head]

        if direction == "Right":

            sequence.extend(right)
            sequence.append(disk_size - 1)
            sequence.extend(reversed(left))

        else:

            sequence.extend(reversed(left))
            sequence.append(0)
            sequence.extend(right)

        return sequence

    def calculate_cscan(self, requests, head, disk_size, direction):

        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])

        sequence = [head]

        if direction == "Right":

            sequence.extend(right)
            sequence.append(disk_size - 1)

            if left:
                sequence.append(0)
                sequence.extend(left)

        else:

            sequence.extend(reversed(left))
            sequence.append(0)

            if right:
                sequence.append(disk_size - 1)
                sequence.extend(reversed(right))

        return sequence

    def run_simulation(self):

        try:

            requests = list(
                map(
                    int,
                    self.entries["Request Queue"].get()
                    .replace(",", " ")
                    .split()
                )
            )

            head = int(self.entries["Initial Head"].get())
            disk_size = int(self.entries["Disk Size"].get())

            if not requests:
                raise ValueError("Request queue cannot be empty.")

            if disk_size <= 0:
                raise ValueError("Disk size must be positive.")

            if head < 0 or head >= disk_size:
                raise ValueError("Initial head is outside disk range.")

            if any(r < 0 or r >= disk_size for r in requests):
                raise ValueError(
                    "All requests must be within disk range."
                )

        except ValueError as e:

            messagebox.showerror("Input Error", str(e))
            return

        algorithm = self.algorithm.get()
        direction = self.direction.get()

        if algorithm == "FCFS":
            sequence = self.calculate_fcfs(requests, head)

        elif algorithm == "SSTF":
            sequence = self.calculate_sstf(requests, head)

        elif algorithm == "SCAN":
            sequence = self.calculate_scan(
                requests, head, disk_size, direction
            )

        elif algorithm == "C-SCAN":
            sequence = self.calculate_cscan(
                requests, head, disk_size, direction
            )

        total_movement = sum(
            abs(sequence[i] - sequence[i - 1])
            for i in range(1, len(sequence))
        )

        self.requests = requests
        self.sequence = sequence

        self.result_label.config(
            text=(
                f"Algorithm: {algorithm}  |  "
                f"Initial Head: {head}  |  "
                f"Total Head Movement: {total_movement} tracks"
            ),
            fg="#0f766e"
        )

        self.sequence_text.config(state="normal")
        self.sequence_text.delete("1.0", tk.END)

        self.sequence_text.insert(
            tk.END,
            " → ".join(map(str, sequence))
        )

        self.sequence_text.config(state="disabled")

        self.draw_visualization(disk_size)

    def draw_visualization(self, disk_size):

        self.canvas.delete("all")

        sequence = self.sequence

        if len(sequence) < 2:
            return

        width = max(self.canvas.winfo_width(), 600)
        height = 240

        margin = 50

        max_track = disk_size - 1

        points = []

        for i, track in enumerate(sequence):

            x = margin + (
                track / max_track
            ) * (width - 2 * margin)

            y = 40 + i * 22

            if y > height - 20:
                y = height - 20

            points.append((x, y))

        # Horizontal track axis
        self.canvas.create_line(
            margin,
            height - 25,
            width - margin,
            height - 25,
            fill="#64748b",
            width=2
        )

        self.canvas.create_text(
            margin,
            height - 10,
            text="0",
            fill="#102a43"
        )

        self.canvas.create_text(
            width - margin,
            height - 10,
            text=str(max_track),
            fill="#102a43"
        )

        # Draw head movement
        for i in range(len(points) - 1):

            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#0f766e",
                width=2,
                arrow=tk.LAST
            )

        # Draw points
        for i, (x, y) in enumerate(points):

            self.canvas.create_oval(
                x - 5,
                y - 5,
                x + 5,
                y + 5,
                fill="#14213d",
                outline=""
            )

            self.canvas.create_text(
                x,
                y - 15,
                text=str(sequence[i]),
                fill="#102a43",
                font=("Arial", 9, "bold")
            )

        self.canvas.create_text(
            width / 2,
            height - 45,
            text="Disk Tracks",
            fill="#64748b",
            font=("Arial", 10)
        )

    def reset(self):

        self.entries["Request Queue"].delete(0, tk.END)
        self.entries["Request Queue"].insert(
            0, "98,183,37,122,14,124,65,67"
        )

        self.entries["Initial Head"].delete(0, tk.END)
        self.entries["Initial Head"].insert(0, "53")

        self.entries["Disk Size"].delete(0, tk.END)
        self.entries["Disk Size"].insert(0, "200")

        self.algorithm.set("FCFS")
        self.direction.set("Right")

        self.result_label.config(
            text="Enter disk requests and run a simulation.",
            fg="#0f766e"
        )

        self.sequence_text.config(state="normal")
        self.sequence_text.delete("1.0", tk.END)
        self.sequence_text.config(state="disabled")

        self.canvas.delete("all")
        self.requests = []
        self.sequence = []
