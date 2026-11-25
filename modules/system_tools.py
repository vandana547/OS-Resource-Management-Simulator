
import tkinter as tk
from tkinter import ttk
import subprocess
import shutil
import platform
import socket
import os
import logging
from datetime import datetime


class SystemToolsUI:

    def __init__(self, parent):

        self.parent = parent

        # Activity logging
        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            filename="logs/system_tools.log",
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

        self.build_ui()

    def build_ui(self):

        container = tk.Frame(self.parent, bg="#f1f5f9")
        container.pack(fill="both", expand=True)

        # Header card
        header = tk.Frame(container, bg="white", bd=1, relief="solid")
        header.pack(fill="x", padx=20, pady=10)

        tk.Label(
            header,
            text="System Utilities",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        tk.Label(
            header,
            text="Python and Bash integration for system resource monitoring",
            font=("Arial", 10),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # Buttons card
        controls = tk.Frame(container, bg="white", bd=1, relief="solid")
        controls.pack(fill="x", padx=20, pady=10)

        tk.Label(
            controls,
            text="System Operations",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        button_area = tk.Frame(controls, bg="white")
        button_area.pack(fill="x", padx=15, pady=10)

        buttons = [
            ("System Information", self.system_info),
            ("CPU Information", self.cpu_info),
            ("Memory Information", self.memory_info),
            ("Disk Usage", self.disk_info),
            ("Directory Listing", self.directory_listing),
            ("Network Information", self.network_info)
        ]

        for i, (name, command) in enumerate(buttons):

            tk.Button(
                button_area,
                text=name,
                command=command,
                bg="#14213d",
                fg="white",
                relief="flat",
                padx=12,
                pady=9
            ).grid(
                row=i // 3,
                column=i % 3,
                padx=8,
                pady=8,
                sticky="ew"
            )

        for col in range(3):
            button_area.columnconfigure(col, weight=1)

        # Bash status
        status_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        status_card.pack(fill="x", padx=20, pady=10)

        bash_available = shutil.which("bash")

        self.bash_status = tk.Label(
            status_card,
            text=(
                "Bash detected: " + bash_available
                if bash_available
                else "Bash not detected - Python fallback mode is available"
            ),
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#0f766e" if bash_available else "#b45309"
        )

        self.bash_status.pack(anchor="w", padx=15, pady=10)

        # Output card
        output_card = tk.Frame(container, bg="white", bd=1, relief="solid")
        output_card.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            output_card,
            text="Command Output",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#102a43"
        ).pack(anchor="w", padx=15, pady=10)

        self.output = tk.Text(
            output_card,
            height=15,
            font=("Consolas", 10),
            bg="#0f172a",
            fg="#e2e8f0",
            wrap="word"
        )

        self.output.pack(fill="both", expand=True, padx=15, pady=10)

        # Footer
        footer = tk.Frame(output_card, bg="white")
        footer.pack(fill="x", padx=15, pady=10)

        tk.Button(
            footer,
            text="Clear Output",
            command=self.clear_output,
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left")

        tk.Button(
            footer,
            text="Save Output",
            command=self.save_output,
            bg="#0f766e",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        ).pack(side="left", padx=10)

    # ----------------------------
    # Output handling
    # ----------------------------

    def display(self, title, result):

        self.output.insert(tk.END, "\n" + "=" * 65 + "\n")
        self.output.insert(tk.END, title + "\n")
        self.output.insert(tk.END, "=" * 65 + "\n")
        self.output.insert(tk.END, result + "\n")

        self.output.see(tk.END)

        logging.info("Executed operation: %s", title)

    # ----------------------------
    # Bash integration
    # ----------------------------

    def run_bash(self, command):

        bash_path = shutil.which("bash")

        if not bash_path:
            return None

        try:

            result = subprocess.run(
                [bash_path, "-lc", command],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout

            if result.stderr:
                output += "\n" + result.stderr

            return output.strip() or "Command executed successfully."

        except Exception as e:

            return f"Bash execution error: {e}"

    # ----------------------------
    # System information
    # ----------------------------

    def system_info(self):

        bash_result = self.run_bash(
            "uname -a; hostname; date"
        )

        if bash_result is None:

            result = (
                f"Operating System: {platform.system()}\n"
                f"Version: {platform.version()}\n"
                f"Machine: {platform.machine()}\n"
                f"Hostname: {socket.gethostname()}\n"
                f"Date and Time: {datetime.now()}"
            )

        else:

            result = bash_result

        self.display("System Information", result)

    # ----------------------------
    # CPU information
    # ----------------------------

    def cpu_info(self):

        bash_result = self.run_bash(
            "nproc"
        )

        if bash_result is None:

            result = (
                f"Processor: {platform.processor()}\n"
                f"Logical CPU Count: {os.cpu_count()}"
            )

        else:

            result = (
                f"Processor: {platform.processor()}\n"
                f"Logical CPU Count: {bash_result}"
            )

        self.display("CPU Information", result)

    # ----------------------------
    # Memory information
    # ----------------------------

    def memory_info(self):

        bash_result = self.run_bash(
            "free -h"
        )

        if bash_result is None:

            try:

                result = (
                    "Windows memory information can be obtained through "
                    "system monitoring tools.\n"
                    f"Operating System: {platform.system()}\n"
                    f"Logical CPUs: {os.cpu_count()}\n"
                    "For detailed RAM usage, install psutil."
                )

            except Exception as e:

                result = str(e)

        else:

            result = bash_result

        self.display("Memory Information", result)

    # ----------------------------
    # Disk information
    # ----------------------------

    def disk_info(self):

        bash_result = self.run_bash(
            "df -h"
        )

        if bash_result is None:

            result = ""

            for drive in ["C:\\", "D:\\"]:

                if os.path.exists(drive):

                    result += (
                        f"\nDrive: {drive}\n"
                        f"Total: {shutil.disk_usage(drive).total // (1024**3)} GB\n"
                        f"Used: {shutil.disk_usage(drive).used // (1024**3)} GB\n"
                        f"Free: {shutil.disk_usage(drive).free // (1024**3)} GB\n"
                    )

            if not result:
                result = "Disk information unavailable."

        else:

            result = bash_result

        self.display("Disk Usage", result)

    # ----------------------------
    # Directory listing
    # ----------------------------

    def directory_listing(self):

        bash_result = self.run_bash(
            "pwd; ls -la"
        )

        if bash_result is None:

            result = (
                f"Current Directory: {os.getcwd()}\n\n"
                + "\n".join(os.listdir("."))
            )

        else:

            result = bash_result

        self.display("Directory Listing", result)

    # ----------------------------
    # Network information
    # ----------------------------

    def network_info(self):

        bash_result = self.run_bash(
            "hostname; hostname -I"
        )

        if bash_result is None:

            try:

                result = (
                    f"Hostname: {socket.gethostname()}\n"
                    f"IP Address: {socket.gethostbyname(socket.gethostname())}"
                )

            except Exception as e:

                result = str(e)

        else:

            result = bash_result

        self.display("Network Information", result)

    # ----------------------------
    # Clear output
    # ----------------------------

    def clear_output(self):

        self.output.delete("1.0", tk.END)
        logging.info("Output cleared")

    # ----------------------------
    # Save output
    # ----------------------------

    def save_output(self):

        os.makedirs("reports", exist_ok=True)

        filename = (
            "reports/system_tools_output_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        with open(filename, "w", encoding="utf-8") as f:

            f.write(self.output.get("1.0", tk.END))

        self.display(
            "Save Output",
            f"Output saved successfully to:\n{filename}"
        )
