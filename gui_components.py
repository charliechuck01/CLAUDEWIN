import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, simpledialog
import logging

logger = logging.getLogger(__name__)

class CLAUDEWIN_GUI:
    def __init__(self, master, assistant):
        self.master = master
        self.assistant = assistant
        self.master.title("CLAUDEWIN")
        self.master.geometry("900x700")
        self.setup_ui()

    def setup_ui(self):
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=30)
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.user_input = tk.Entry(self.master, width=70)
        self.user_input.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        send_button = tk.Button(self.master, text="Send", command=self.send_message)
        send_button.grid(row=1, column=2, padx=10, pady=10)

        process_file_button = tk.Button(self.master, text="Process Large File", command=self.process_large_file)
        process_file_button.grid(row=2, column=0, padx=10, pady=10)

        generate_report_button = tk.Button(self.master, text="Generate Report", command=self.generate_report)
        generate_report_button.grid(row=2, column=1, padx=10, pady=10)

        update_data_button = tk.Button(self.master, text="Update Data", command=self.update_data)
        update_data_button.grid(row=2, column=2, padx=10, pady=10)

        check_task_button = tk.Button(self.master, text="Check Task Status", command=self.check_task_status)
        check_task_button.grid(row=3, column=1, padx=10, pady=10)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        self.chat_display.insert(tk.END, f"You: {user_message}\n")
        try:
            response = self.assistant.generate_response(user_message)
            self.chat_display.insert(tk.END, f"CLAUDEWIN: {response}\n\n")
        except Exception as e:
            logger.error(f"Error in send_message: {str(e)}")
            self.chat_display.insert(tk.END, "CLAUDEWIN: I apologize, but an error occurred while processing your request.\n\n")
        self.chat_display.see(tk.END)
        self.user_input.delete(0, tk.END)

    def process_large_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                file_name = file_path.split("/")[-1]
                result = self.assistant.process_large_file(file_name)
                messagebox.showinfo("Background Process", result)
            except Exception as e:
                logger.error(f"Error in process_large_file: {str(e)}")
                messagebox.showerror("Error", "An error occurred while processing the file.")

    def generate_report(self):
        report_type = simpledialog.askstring("Report Type", "Enter the type of report:")
        if report_type:
            parameters = simpledialog.askstring("Parameters", "Enter report parameters (comma-separated):")
            if parameters:
                try:
                    result = self.assistant.generate_report(report_type, parameters.split(','))
                    messagebox.showinfo("Report Generation", result)
                except Exception as e:
                    logger.error(f"Error in generate_report: {str(e)}")
                    messagebox.showerror("Error", "An error occurred while generating the report.")

    def update_data(self):
        data_source = simpledialog.askstring("Data Source", "Enter the data source:")
        if data_source:
            try:
                result = self.assistant.update_data(data_source)
                messagebox.showinfo("Data Update", result)
            except Exception as e:
                logger.error(f"Error in update_data: {str(e)}")
                messagebox.showerror("Error", "An error occurred while updating data.")

    def check_task_status(self):
        task_id = simpledialog.askstring("Task ID", "Enter the task ID:")
        if task_id:
            try:
                result = self.assistant.get_background_task_result(task_id)
                messagebox.showinfo("Task Status", str(result))
            except Exception as e:
                logger.error(f"Error in check_task_status: {str(e)}")
                messagebox.showerror("Error", "An error occurred while checking the task status.")
