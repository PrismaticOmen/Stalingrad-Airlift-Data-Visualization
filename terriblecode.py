import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StalingradAirliftCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stalingrad Airlift Calculator")
        self.root.geometry("900x700")
        
        # Historical data
        self.aircraft_data = {
            "Ju 52": {"payload_tons": 2.0, "available": 250},
            "He 111": {"payload_tons": 1.5, "available": 165},
            "Ju 86": {"payload_tons": 1.0, "available": 40},
            "Fw 200": {"payload_tons": 2.5, "available": 15},
        }
        
        # Default 6th Army requirements (tons per day)
        self.daily_requirements = {
            "Food": 300,
            "Ammunition": 250,
            "Fuel": 180,
            "Medical supplies": 50,
            "Other supplies": 20,
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create notebooks for different tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Requirements tab
        req_frame = ttk.Frame(notebook)
        notebook.add(req_frame, text="Supply Requirements")
        
        # Aircraft tab
        aircraft_frame = ttk.Frame(notebook)
        notebook.add(aircraft_frame, text="Aircraft Data")
        
        # Results tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Airlift Results")
        
        # Set up requirements tab
        self.setup_requirements_tab(req_frame)
        
        # Set up aircraft tab
        self.setup_aircraft_tab(aircraft_frame)
        
        # Set up results tab
        self.setup_results_tab(results_frame)
        
        # Calculate button
        calculate_btn = ttk.Button(self.root, text="Calculate Airlift Requirements", 
                                  command=self.calculate_and_display)
        calculate_btn.pack(pady=10)
        
    def setup_requirements_tab(self, parent):
        # Explanation label
        ttk.Label(parent, text="Enter the daily supply requirements for the 6th Army (in tons):",
                 wraplength=500).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Create input fields for each requirement
        self.requirement_vars = {}
        row = 1
        
        for requirement, amount in self.daily_requirements.items():
            ttk.Label(parent, text=f"{requirement}:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
            var = tk.DoubleVar(value=amount)
            self.requirement_vars[requirement] = var
            entry = ttk.Entry(parent, textvariable=var, width=10)
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            row += 1
        
        # Calculate total
        ttk.Label(parent, text="Total daily requirement:").grid(row=row, column=0, padx=10, pady=15, sticky="w")
        self.total_var = tk.StringVar(value="800 tons")
        ttk.Label(parent, textvariable=self.total_var, font=("Arial", 10, "bold")).grid(
            row=row, column=1, padx=10, pady=15, sticky="w")
        
        # Add a button to update total
        ttk.Button(parent, text="Update Total", command=self.update_total).grid(
            row=row+1, column=0, columnspan=2, pady=10)
        
        # Historical context
        context_frame = ttk.LabelFrame(parent, text="Historical Context")
        context_frame.grid(row=0, column=2, rowspan=row+2, padx=20, pady=10, sticky="nsew")
        
        context_text = """
The 6th Army at Stalingrad (November 1942 - February 1943):
- Approximately 270,000 soldiers trapped
- Needed minimum of 800 tons of supplies daily
- Luftwaffe promised 300 tons daily but rarely delivered
- Airlift operation ultimately failed, leading to surrender
- Weather, Soviet air defenses, and inadequate aircraft numbers contributed to failure
"""
        ttk.Label(context_frame, text=context_text, wraplength=300, justify="left").pack(padx=10, pady=10)
        
    def setup_aircraft_tab(self, parent):
        # Explanation label
        ttk.Label(parent, text="Aircraft available for the Stalingrad Airlift:",
                 wraplength=500).grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        # Headers
        ttk.Label(parent, text="Aircraft Type", font=("Arial", 10, "bold")).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(parent, text="Payload (tons)", font=("Arial", 10, "bold")).grid(
            row=1, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(parent, text="Number Available", font=("Arial", 10, "bold")).grid(
            row=1, column=2, padx=10, pady=5, sticky="w")
        
        # Create input fields for each aircraft
        self.aircraft_vars = {}
        row = 2
        
        for aircraft, data in self.aircraft_data.items():
            ttk.Label(parent, text=aircraft).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            payload_var = tk.DoubleVar(value=data["payload_tons"])
            self.aircraft_vars[aircraft] = {"payload": payload_var}
            payload_entry = ttk.Entry(parent, textvariable=payload_var, width=10)
            payload_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            
            available_var = tk.IntVar(value=data["available"])
            self.aircraft_vars[aircraft]["available"] = available_var
            available_entry = ttk.Entry(parent, textvariable=available_var, width=10)
            available_entry.grid(row=row, column=2, padx=10, pady=5, sticky="w")
            
            row += 1
        
        # Aircraft images and descriptions
        info_frame = ttk.LabelFrame(parent, text="Aircraft Information")
        info_frame.grid(row=2, column=3, rowspan=row-2, padx=20, pady=10, sticky="nsew")
        
        aircraft_info = """
Ju 52 "Tante Ju" (Aunt Ju):
- Primary transport aircraft
- Reliable but slow (maximum speed 211 km/h)
- Three-engine design
- Poor performance in winter conditions

He 111:
- Medium bomber converted for transport
- Faster but less reliable for cargo
- Less efficient for loading/unloading

Ju 86:
- Older bomber aircraft
- Limited cargo capacity
- Used as supplement

Fw 200 Condor:
- Long-range maritime patrol aircraft
- Larger payload but fewer available
- Not designed for short airfield operations
"""
        ttk.Label(info_frame, text=aircraft_info, wraplength=300, justify="left").pack(padx=10, pady=10)
        
    def setup_results_tab(self, parent):
        # Will contain the results of calculations
        self.results_frame = ttk.Frame(parent)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder text
        ttk.Label(self.results_frame, text="Click 'Calculate Airlift Requirements' to see results").pack(pady=50)
        
    def update_total(self):
        total = sum(var.get() for var in self.requirement_vars.values())
        self.total_var.set(f"{total:.1f} tons")
        
    def calculate_and_display(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Calculate total daily requirements
        total_required = sum(var.get() for var in self.requirement_vars.values())
        
        # Calculate aircraft capabilities
        aircraft_capabilities = {}
        total_potential_capacity = 0
        
        for aircraft, vars in self.aircraft_vars.items():
            payload = vars["payload"].get()
            available = vars["available"].get()
            
            daily_capacity = payload * available
            total_potential_capacity += daily_capacity
            
            aircraft_capabilities[aircraft] = {
                "payload": payload,
                "available": available,
                "daily_capacity": daily_capacity,
                "flights_needed": total_required / payload if payload > 0 else 0,
                "aircraft_needed": total_required / daily_capacity * available if daily_capacity > 0 else 0
            }
        
        # Display results
        ttk.Label(self.results_frame, 
                 text=f"Total daily requirement: {total_required:.1f} tons",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        ttk.Label(self.results_frame, 
                 text=f"Total potential airlift capacity: {total_potential_capacity:.1f} tons per day",
                 font=("Arial", 12)).pack(anchor="w", pady=5)
        
        if total_potential_capacity < total_required:
            shortage = total_required - total_potential_capacity
            ttk.Label(self.results_frame, 
                     text=f"SHORTAGE: {shortage:.1f} tons per day ({shortage/total_required*100:.1f}% deficit)",
                     foreground="red", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        else:
            surplus = total_potential_capacity - total_required
            ttk.Label(self.results_frame, 
                     text=f"Surplus capacity: {surplus:.1f} tons per day",
                     foreground="green", font=("Arial", 12)).pack(anchor="w", pady=5)
        
        # Create table for aircraft details
        ttk.Label(self.results_frame, text="Aircraft Requirements Breakdown:", 
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        # Table frame
        table_frame = ttk.Frame(self.results_frame)
        table_frame.pack(fill="both", expand=True, pady=5)
        
        # Headers
        headers = ["Aircraft Type", "Payload (tons)", "Available", "Daily Capacity (tons)", 
                  "Flights Needed", "% of Requirement"]
        for col, header in enumerate(headers):
            ttk.Label(table_frame, text=header, font=("Arial", 10, "bold")).grid(
                row=0, column=col, padx=10, pady=5, sticky="w")
        
        # Data rows
        for row, (aircraft, data) in enumerate(aircraft_capabilities.items(), start=1):
            ttk.Label(table_frame, text=aircraft).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(table_frame, text=f"{data['payload']:.1f}").grid(row=row, column=1, padx=10, pady=5, sticky="w")
            ttk.Label(table_frame, text=f"{data['available']}").grid(row=row, column=2, padx=10, pady=5, sticky="w")
            ttk.Label(table_frame, text=f"{data['daily_capacity']:.1f}").grid(row=row, column=3, padx=10, pady=5, sticky="w")
            ttk.Label(table_frame, text=f"{data['flights_needed']:.1f}").grid(row=row, column=4, padx=10, pady=5, sticky="w")
            percentage = (data['daily_capacity'] / total_required * 100) if total_required > 0 else 0
            ttk.Label(table_frame, text=f"{percentage:.1f}%").grid(row=row, column=5, padx=10, pady=5, sticky="w")
        
        # Create visualization
        self.create_visualization()
        
    def create_visualization(self):
        # Create frame for visualization
        viz_frame = ttk.LabelFrame(self.results_frame, text="Visualization")
        viz_frame.pack(fill="both", expand=True, pady=10)
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Get data for plots
        requirements = {req: var.get() for req, var in self.requirement_vars.items()}
        capacities = {aircraft: vars["payload"].get() * vars["available"].get() 
                     for aircraft, vars in self.aircraft_vars.items()}
        
        # Plot supply requirements
        ax1.bar(requirements.keys(), requirements.values(), color='darkblue')
        ax1.set_title('Daily Supply Requirements (tons)')
        ax1.set_ylabel('Tons')
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Plot aircraft capacities
        ax2.bar(capacities.keys(), capacities.values(), color='darkgreen')
        ax2.set_title('Aircraft Daily Capacity (tons)')
        ax2.set_ylabel('Tons')
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # Adjust layout
        plt.tight_layout()
        
        # Add figure to tkinter window
        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add a note about historical reality
        ttk.Label(self.results_frame, 
                 text="""
Historical Note: In reality, the Luftwaffe never achieved the promised 300 tons per day 
due to weather, Soviet air defenses, and operational difficulties. On most days, 
less than 100 tons reached the encircled forces.""",
                 wraplength=800, foreground='gray').pack(pady=10)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StalingradAirliftCalculator(root)
    root.mainloop()