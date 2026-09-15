import csv
import zlib
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class CRCDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("CRC-32 Verification Dashboard")
        self.root.geometry("650x550")
        
        self.reference_crc = None
        self.current_payload = None
        self.report_data = []

        self.setup_ui()

    def setup_ui(self):
        # 1. Input Selection Controls
        input_frame = ttk.LabelFrame(self.root, text=" 1. Input Selection Controls ", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Input Type:").grid(row=0, column=0, sticky="w", padx=5)
        self.input_type_var = tk.StringVar(value="Message")
        type_combo = ttk.Combobox(
            input_frame, 
            textvariable=self.input_type_var, 
            values=["Message", "Packet/Record", "File"], 
            state="readonly"
        )
        type_combo.grid(row=0, column=1, sticky="w", padx=5)
        type_combo.bind("<<ComboboxSelected>>", self.toggle_input_mode)

        ttk.Label(input_frame, text="Payload / Path:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_payload = ttk.Entry(input_frame, width=40)
        self.entry_payload.grid(row=1, column=1, padx=5, pady=5)

        self.btn_browse = ttk.Button(input_frame, text="Browse File", command=self.browse_file, state="disabled")
        self.btn_browse.grid(row=1, column=2, padx=5, pady=5)

        btn_gen_crc = ttk.Button(input_frame, text="Generate Reference CRC", command=self.generate_reference_crc)
        btn_gen_crc.grid(row=2, column=1, sticky="e", pady=5)

        # 2. Reference & Current Status Display
        status_frame = ttk.LabelFrame(self.root, text=" 2. CRC Status & Verification ", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(status_frame, text="Reference CRC-32:").grid(row=0, column=0, sticky="w", padx=5)
        self.lbl_ref_crc = ttk.Label(status_frame, text="N/A", font=("Courier", 10, "bold"))
        self.lbl_ref_crc.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(status_frame, text="Current CRC-32:").grid(row=1, column=0, sticky="w", padx=5)
        self.lbl_curr_crc = ttk.Label(status_frame, text="N/A", font=("Courier", 10, "bold"))
        self.lbl_curr_crc.grid(row=1, column=1, sticky="w", padx=5)

        self.lbl_status = tk.Label(status_frame, text="STATUS: UNVERIFIED", font=("Helvetica", 12, "bold"), fg="gray")
        self.lbl_status.grid(row=2, column=0, columnspan=2, pady=10)

        # 3. Error Simulation Controls
        error_frame = ttk.LabelFrame(self.root, text=" 3. Error Simulation Controls ", padding=10)
        error_frame.pack(fill="x", padx=10, pady=5)

        btn_bit_flip = ttk.Button(error_frame, text="Simulate Bit Flip (Corrupt)", command=self.simulate_bit_flip)
        btn_bit_flip.pack(side="left", padx=10, expand=True)

        btn_verify = ttk.Button(error_frame, text="Verify Payload", command=self.verify_crc)
        btn_verify.pack(side="left", padx=10, expand=True)

        # 4. Report & Actions
        report_frame = ttk.Frame(self.root, padding=10)
        report_frame.pack(fill="x", padx=10, pady=5)

        btn_export = ttk.Button(report_frame, text="Export CSV Verification Report", command=self.export_csv)
        btn_export.pack(fill="x")

    def toggle_input_mode(self, event=None):
        if self.input_type_var.get() == "File":
            self.btn_browse.config(state="normal")
            self.entry_payload.delete(0, tk.END)
        else:
            self.btn_browse.config(state="disabled")

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.entry_payload.delete(0, tk.END)
            self.entry_payload.insert(0, filepath)

    def calculate_crc32(self, data_bytes):
        return f"{zlib.crc32(data_bytes) & 0xffffffff:08X}"

    def get_current_bytes(self):
        input_type = self.input_type_var.get()
        data_str = self.entry_payload.get()

        if not data_str:
            messagebox.showwarning("Warning", "Please provide input data or select a file.")
            return None

        if input_type == "File":
            try:
                with open(data_str, "rb") as f:
                    return f.read()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
                return None
        else:
            return data_str.encode("utf-8")

    def generate_reference_crc(self):
        raw_bytes = self.get_current_bytes()
        if raw_bytes is not None:
            self.current_payload = raw_bytes
            self.reference_crc = self.calculate_crc32(raw_bytes)
            self.lbl_ref_crc.config(text=self.reference_crc)
            self.lbl_curr_crc.config(text=self.reference_crc)
            self.lbl_status.config(text="STATUS: REFERENCE SET", fg="blue")
            messagebox.showinfo("Success", f"Reference CRC-32 generated: {self.reference_crc}")

    def simulate_bit_flip(self):
        if self.current_payload is None:
            messagebox.showwarning("Warning", "Generate a Reference CRC first!")
            return

        # Flip the first bit of the payload
        byte_array = bytearray(self.current_payload)
        if len(byte_array) > 0:
            byte_array[0] ^= 0x01
            self.current_payload = bytes(byte_array)
            corrupted_crc = self.calculate_crc32(self.current_payload)
            self.lbl_curr_crc.config(text=corrupted_crc)
            messagebox.showwarning("Error Simulated", "A bit flip was injected into the payload data.")
        else:
            messagebox.showerror("Error", "Payload is empty, cannot corrupt.")

    def verify_crc(self):
        if not self.reference_crc or self.current_payload is None:
            messagebox.showwarning("Warning", "Generate a Reference CRC before verifying.")
            return

        current_crc = self.calculate_crc32(self.current_payload)
        self.lbl_curr_crc.config(text=current_crc)

        status_str = "VALID" if current_crc == self.reference_crc else "CORRUPTED"
        color = "green" if status_str == "VALID" else "red"

        self.lbl_status.config(text=f"STATUS: {status_str}", fg=color)

        # Log for CSV report
        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Input_Type": self.input_type_var.get(),
            "Reference_CRC": self.reference_crc,
            "Current_CRC": current_crc,
            "Status": status_str
        }
        self.report_data.append(log_entry)

    def export_csv(self):
        if not self.report_data:
            messagebox.showwarning("Warning", "No verification logs available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            keys = self.report_data[0].keys()
            with open(file_path, "w", newline="") as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.report_data)
            messagebox.showinfo("Report Saved", f"CSV verification report saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRCDashboard(root)
    root.mainloop()
