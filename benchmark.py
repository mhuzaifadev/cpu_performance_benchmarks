import tkinter as tk
import threading
import time
import csv
from datetime import datetime

# Define the benchmark tests (dummy functions for demonstration purposes)
def benchmark_test_1():
    time.sleep(5)  # Simulating a long-running task
    return {"Test 1": 10}

def benchmark_test_2():
    time.sleep(3)  # Simulating a long-running task
    return {"Test 2": 8}

def benchmark_test_3():
    time.sleep(7)  # Simulating a long-running task
    return {"Test 3": 12}

class CPUBenchmarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Benchmark Software")
        self.benchmark_tests = {
            "Test 1": benchmark_test_1,
            "Test 2": benchmark_test_2,
            "Test 3": benchmark_test_3
        }
        self.selected_tests = []
        self.run_button = None
        self.progress_label = None

        self.create_gui()

    def create_gui(self):
        # Create the GUI elements
        self.run_button = tk.Button(self.root, text="Run Benchmark", command=self.run_benchmarks, width=15, height=2, bg="#4CAF50", fg="white")
        self.run_button.pack(pady=20)

        self.progress_label = tk.Label(self.root, text="Progress: 0%", font=("Helvetica", 12))
        self.progress_label.pack(pady=10)

    def run_benchmarks(self):
        # Disable the Run Benchmark button during execution
        self.run_button.config(state=tk.DISABLED)

        # Get the selected benchmark tests
        self.selected_tests = [test_name for test_name in self.benchmark_tests.keys()]

        # Calculate the total number of benchmark tests
        total_tests = len(self.selected_tests)
        completed_tests = 0

        # Create a list to store the worker threads and results
        threads = []
        results = []

        # Define a function to update the progress label
        def update_progress():
            progress = (completed_tests / total_tests) * 100
            self.progress_label.config(text="Progress: {:.2f}%".format(progress))

        # Create worker threads for each selected benchmark test
        for test_name in self.selected_tests:
            test_func = self.benchmark_tests[test_name]
            thread = threading.Thread(target=self.run_benchmark_test, args=(test_name, test_func, results, update_progress))
            threads.append(thread)

        # Start the worker threads
        for thread in threads:
            thread.start()

        # Wait for all worker threads to finish
        for thread in threads:
            thread.join()

        # Generate a timestamp for the report filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate the benchmark report
        report_filename = f"benchmark_report_{timestamp}.csv"
        self.generate_report(report_filename, results)

        # Enable the Run Benchmark button after execution
        self.run_button.config(state=tk.NORMAL)

    def run_benchmark_test(self, test_name, test_func, results, update_progress):
        try:
            # Execute the benchmark test and store the results
            result = test_func()
            results.append(result)

            # Update the completed tests counter and progress label
            completed_tests = len(self.selected_tests) - len(threading.enumerate()) + 1
            self.root.after(0, update_progress)
        except Exception as e:
            # Handle any exceptions during benchmark execution
            print(f"Error occurred during {test_name}: {str(e)}")

    def generate_report(self, filename, results):
        # Generate a CSV report with the benchmark results
        fieldnames = results[0].keys() if results else []
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

# Create the main application window
root = tk.Tk()

# Set the window dimensions and position
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set the window icon
root.iconbitmap("icon.ico")  # Replace "icon.ico" with the path to your icon file

# Set the window background color
root.configure(bg="#f2f2f2")

# Create the CPU Benchmark application
app = CPUBenchmarkApp(root)

# Start the main event loop
root.mainloop()
