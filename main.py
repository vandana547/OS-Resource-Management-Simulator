
import tkinter as tk
from tkinter import ttk
from modules.cpu_scheduling import CPUSchedulingUI

from modules.memory_management import MemoryManagementUI
from modules.deadlock_management import DeadlockManagementUI
from modules.disk_scheduling import DiskSchedulingUI
from modules.system_tools import SystemToolsUI
from modules.reports import ReportsUI

class OSResourceSimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("OS Resource Management Simulator")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f1f5f9")

        self.create_sidebar()
        self.create_main_area()
        self.show_dashboard()

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root, bg="#14213d", width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="OS SIMULATOR",
            font=("Arial", 20, "bold"),
            bg="#14213d",
            fg="white"
        ).pack(pady=(30, 10))

        tk.Label(
            self.sidebar,
            text="Resource Management",
            font=("Arial", 10),
            bg="#14213d",
            fg="#94a3b8"
        ).pack(pady=(0, 30))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("CPU Scheduling", self.show_cpu),
            ("Memory Management", self.show_memory),
            ("Deadlock Management", self.show_deadlock),
            ("Disk Scheduling", self.show_disk),
            ("System Tools", self.show_tools),
            ("Reports", self.show_reports)
        ]

        for text, command in buttons:
            tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#223451",
                fg="white",
                activebackground="#365475",
                activeforeground="white",
                relief="flat",
                font=("Arial", 11),
                anchor="w",
                padx=20,
                pady=12
            ).pack(fill="x", padx=10, pady=5)

    def create_main_area(self):
        self.main = tk.Frame(self.root, bg="#f1f5f9")
        self.main.pack(side="left", fill="both", expand=True)

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle):

        tk.Label(
            self.main,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#f1f5f9",
            fg="#102a43"
        ).pack(anchor="w", padx=25, pady=(25, 5))

        tk.Label(
            self.main,
            text=subtitle,
            font=("Arial", 11),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(anchor="w", padx=25, pady=(0, 20))

    def show_dashboard(self):

        self.clear_main()

        self.create_header(
            "Dashboard",
            "Operating System Resource Management"
        )

        card_area = tk.Frame(self.main, bg="#f1f5f9")
        card_area.pack(fill="x", padx=20)

        self.create_card(card_area, "CPU", "Scheduling")
        self.create_card(card_area, "Memory", "Allocation")
        self.create_card(card_area, "Deadlock", "Detection")
        self.create_card(card_area, "Disk", "Scheduling")

        info = tk.Frame(self.main, bg="white", bd=1, relief="solid")
        info.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            info,
            text="Project Overview",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=20, pady=20)

        description = (
            "Welcome to the OS Resource Management Simulator.\n\n"
            "This application simulates major operating system "
            "resource management functions.\n\n"
            "Modules included:\n\n"
            "1. CPU Scheduling Algorithms\n"
            "2. Memory Allocation Strategies\n"
            "3. Deadlock Detection and Avoidance\n"
            "4. Disk Scheduling Algorithms\n"
            "5. Bash System Utilities\n"
            "6. Performance Analysis and Reports"
        )

        tk.Label(
            info,
            text=description,
            font=("Arial", 12),
            bg="white",
            fg="#334155",
            justify="left",
            anchor="nw"
        ).pack(anchor="w", padx=20, pady=10)

    def create_card(self, parent, title, description):

        card = tk.Frame(parent, bg="white", bd=1, relief="solid")

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8,
            pady=10
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#0f766e"
        ).pack(pady=(20, 5))

        tk.Label(
            card,
            text=description,
            font=("Arial", 11),
            bg="white",
            fg="#64748b"
        ).pack(pady=(0, 20))

    def show_cpu(self):
        self.clear_main()
        self.create_header(
        "CPU Scheduling",
        "Compare process scheduling algorithms"
    )
        CPUSchedulingUI(self.main)

    def show_memory(self):
        self.clear_main()
        self.create_header(
            "Memory Management",
            "Compare memory allocation strategies"
        )
        MemoryManagementUI(self.main)

    def show_deadlock(self):
        self.clear_main()
        self.create_header(
            "Deadlock Management",
            "Banker's Algorithm: Deadlock avoidance and safety analysis"
        )
        DeadlockManagementUI(self.main)

    def show_disk(self):
        self.clear_main()
        self.create_header(
            "Disk Scheduling",
            "Compare disk head scheduling algorithms"
        )
        DiskSchedulingUI(self.main)

    def show_tools(self):
        self.clear_main()
        self.create_header(
            "System Tools",
            "Python and Bash system utilities"
        )
        SystemToolsUI(self.main)

    def show_reports(self):
        self.clear_main()
        self.create_header(
            "Reports",
            "Performance analysis and export"
        )
        ReportsUI(self.main)

    def create_placeholder(self, text):

        panel = tk.Frame(self.main, bg="white", bd=1, relief="solid")
        panel.pack(fill="both", expand=True, padx=25, pady=20)

        tk.Label(
            panel,
            text=text,
            font=("Arial", 15),
            bg="white",
            fg="#64748b"
        ).pack(pady=50)


if __name__ == "__main__":
    root = tk.Tk()
    app = OSResourceSimulator(root)
    root.mainloop()
