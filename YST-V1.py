# YST-V1.py

import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
import math
import calendar
import pandas as pd
import plotly.express as px

# GHI values of Nigeria States
ghi = {
    'Abia': 4.71, 'Adamawa': 5.70, 'Akwa Ibom': 4.21, 'Anambra': 4.81, 'Bauchi': 5.77, 'Bayelsa': 4.88,
    'Benue': 5.19, 'Borno': 5.90, 'Cross River': 4.74, 'Delta': 4.53, 'Ebonyi': 5.05, 'Edo': 4.66,
    'Ekiti': 4.94, 'Enugu': 4.92, 'FCT': 5.45, 'Gombe': 5.77, 'Imo': 4.71, 'Jigawa': 6.16, 'Kaduna': 5.64,
    'Kano': 5.87, 'Katsina': 5.94, 'Kebbi': 5.62, 'Kogi': 5.40, 'Kwara': 5.16, 'Lagos': 4.74, 'Nassarawa': 5.36,
    'Niger': 5.51, 'Ogun': 4.74, 'Ondo': 4.66, 'Osun': 4.89, 'Oyo': 5.11, 'Plateau': 5.52, 'Rivers': 4.13,
    'Sokoto': 6.24, 'Taraba': 5.53, 'Yobe': 6.11, 'Zamfara': 6.01
}

# Monthly variation factors
monthly_variation_factors = {
    'January': 0.95, 'February': 0.92, 'March': 0.97, 'April': 1.05,
    'May': 1.12, 'June': 1.18, 'July': 1.20, 'August': 1.15,
    'September': 1.08, 'October': 1.03, 'November': 0.98, 'December': 0.92
}

def calculate_monthly_pv_potential(panel_length, panel_width, panel_efficiency, inverter_efficiency, state):
    ghi_value = ghi[state]
    panel_area = panel_length * panel_width
    panel_efficiency /= 100
    inverter_efficiency /= 100

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    monthly_factors = [monthly_variation_factors[month] for month in months]

    monthly_pv_potential = [ghi_value * panel_area * panel_efficiency * inverter_efficiency * factor
                            for factor in monthly_factors]

    return monthly_pv_potential, months

def plot_monthly_pv_potential(months, monthly_pv_potential, state):
    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(months, monthly_pv_potential, marker='o', linestyle='-', color='orange')
    plt.title(f'Monthly PV Potential for a Single Panel in {state}')
    plt.xlabel('Month')
    plt.ylabel('PV Potential (kWh)')
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img = Image.open(buf)

    return img

# Main app using gradio Blocks
def main():
    with gr.Blocks() as app:
        gr.Markdown("# Yellow Sun Tool - PV System Performance Analysis")

        # Shared Inputs
        gr.Markdown("## Solar Panel Details and Project State")
        panel_length = gr.Number(label="Solar Panel Length (m)", value=1.6)
        panel_width = gr.Number(label="Solar Panel Width (m)", value=1.0)
        panel_efficiency = gr.Slider(minimum=0, maximum=100, label="Solar Panel Efficiency (%)", value=20)
        inverter_efficiency = gr.Slider(minimum=0, maximum=100, label="Inverter Efficiency (%)", value=95)
        state = gr.Dropdown(choices=list(ghi.keys()), label="Project State", value='Lagos')

        # How to Use Tab
        with gr.Tab("How to Use"):
            gr.Markdown("""
            ## How to Use the Yellow Sun Tool

            Welcome to the **Yellow Sun Tool**, a comprehensive PV system performance analysis application. This tool consists of several calculators that build upon each other to help you design and analyze photovoltaic systems.

            ### **1. Enter Solar Panel Details and Project State**

            At the top of the app, you will find inputs for:

            - **Solar Panel Length (m):** The length of a single solar panel in meters.
            - **Solar Panel Width (m):** The width of a single solar panel in meters.
            - **Solar Panel Efficiency (%):** The efficiency rating of the solar panel.
            - **Inverter Efficiency (%):** The efficiency of the inverter used in the system.
            - **Project State:** Select the Nigerian state where the project is located.

            These inputs are shared across all calculators and should be entered first.

            ### **2. Monthly PV Potential**

            - Click on the **Monthly PV Potential** tab.
            - Click the **Calculate Monthly PV Potential** button.
            - The app will display:
              - A graph showing the monthly PV potential for a single panel in the selected state.
              - A table with the numerical values of the monthly PV potential.

            ### **3. PV System Designer**

            - Click on the **PV System Designer** tab.
            - Enter additional inputs:
              - **Daily Target Energy (kWh):** The amount of energy you aim to generate daily.
              - **Autonomy Days:** Number of days the system should operate without sunlight.
              - **Battery Voltage (V):** Voltage rating of the batteries.
              - **Depth of Discharge (%):** Maximum allowable depth of discharge for the batteries.
              - **Battery Efficiency (%):** Efficiency of the batteries.
              - **Battery Capacity (Ah):** Capacity of a single battery in ampere-hours.
            - Click the **Design PV System** button.
            - The app will display:
              - The number of panels required.
              - The number of batteries required.
              - The total battery capacity needed.
              - A graph of monthly energy generation for the designed PV system.

            ### **4. Cost Simulation**

            - Click on the **Cost Simulation** tab.
            - Enter cost-related inputs for procurement, installation, and maintenance.
            - Click the **Simulate Costs** button.
            - The app will display:
              - A cost table detailing annual costs.
              - An annual cost comparison graph between the PV system and grid supply.
              - A cumulative life cycle cost comparison graph over the specified number of years.

            ### **5. Carbon Emission Matrix**

            - Click on the **Carbon Emission Matrix** tab.
            - Enter:
              - **Number of Years for Carbon Emissions Assessment**
              - **Daily Target Energy (kWh)**
            - Click the **Calculate Carbon Emissions** button.
            - The app will display:
              - Total carbon emissions from grid electricity over the specified years.
              - Total carbon emissions from the PV system's solar energy over the specified years.
              - A pie chart comparing the carbon emissions.

            ### **Tips**

            - **Ensure Inputs Are Accurate:** Double-check your inputs for accuracy to get reliable results.
            - **Navigate Between Tabs:** You can switch between tabs to access different calculators.
            - **Use Default Values:** Default values are provided for guidance; adjust them according to your project needs.

            ### **Support**

            If you have any questions or need assistance, please contact our support team at [support@example.com](mailto:support@example.com).

            """)

        # Existing tabs (Monthly PV Potential, PV System Designer, Cost Simulation, Carbon Emission Matrix)
        # Code Block 1: Monthly PV Potential
        with gr.Tab("Monthly PV Potential"):
            gr.Markdown("### Monthly PV Potential Estimation")

            btn_calculate_pv = gr.Button("Calculate Monthly PV Potential")

            pv_potential_output = gr.Image(type="pil", label="Monthly PV Potential Graph")
            pv_potential_table = gr.Dataframe(label="Monthly PV Potential (kWh)")

            def calculate_pv_potential_action(panel_length, panel_width, panel_efficiency, inverter_efficiency, state):
                monthly_pv_potential, months = calculate_monthly_pv_potential(
                    panel_length, panel_width, panel_efficiency, inverter_efficiency, state)
                img = plot_monthly_pv_potential(months, monthly_pv_potential, state)
                df = pd.DataFrame([monthly_pv_potential], columns=months)
                return img, df

            btn_calculate_pv.click(
                calculate_pv_potential_action,
                inputs=[panel_length, panel_width, panel_efficiency, inverter_efficiency, state],
                outputs=[pv_potential_output, pv_potential_table]
            )

        # Code Block 2: PV System Designer
        with gr.Tab("PV System Designer"):
            gr.Markdown("### PV System Designer for Monthly Variation")

            daily_target_energy = gr.Number(label="Daily Target Energy (kWh)", value=10)
            autonomy_days = gr.Number(label="Autonomy Days", value=2)
            battery_voltage = gr.Number(label="Battery Voltage (V)", value=12)
            depth_of_discharge = gr.Slider(minimum=0, maximum=100, label="Depth of Discharge (%)", value=50)
            battery_efficiency = gr.Slider(minimum=0, maximum=100, label="Battery Efficiency (%)", value=95)
            battery_capacity = gr.Number(label="Battery Capacity (Ah)", value=200)

            btn_design_system = gr.Button("Design PV System")

            num_panels_output = gr.Textbox(label="Number of Panels")
            num_batteries_output = gr.Textbox(label="Number of Batteries")
            total_battery_capacity_output = gr.Number(label="Total Battery Capacity (Ah)")
            monthly_generation_output = gr.Image(type="pil", label="Monthly Energy Generation Graph")

            def design_pv_system_action(panel_length, panel_width, panel_efficiency, inverter_efficiency, state,
                                        daily_target_energy, autonomy_days, battery_voltage, depth_of_discharge,
                                        battery_efficiency, battery_capacity):
                ghi_value = ghi[state]
                panel_area = panel_length * panel_width
                panel_efficiency /= 100
                inverter_efficiency /= 100

                months = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
                monthly_factors = [monthly_variation_factors[month] for month in months]

                monthly_pv_potential = [ghi_value * panel_area * panel_efficiency * inverter_efficiency * factor
                                        for factor in monthly_factors]

                min_pv_potential = min(monthly_pv_potential)
                min_panels = math.ceil(daily_target_energy / min_pv_potential)

                depth_of_discharge /= 100
                battery_efficiency /= 100
                total_battery_capacity = (((daily_target_energy * autonomy_days * 1000) / battery_voltage)
                                          * (1 / battery_efficiency) * (1 / depth_of_discharge))
                total_battery_capacity = math.ceil(total_battery_capacity)
                number_of_batteries = math.ceil(total_battery_capacity / battery_capacity)

                # Plot generation across months
                days_in_month = [calendar.monthrange(2023, i+1)[1] for i in range(12)]
                total_potential = [min_panels * potential * days for potential, days in zip(monthly_pv_potential, days_in_month)]

                plt.figure(figsize=(14, 6))
                plt.bar(months, total_potential, color='orange')
                plt.title('Monthly Energy Generation for Designed PV System')
                plt.xlabel('Month')
                plt.ylabel('Energy Generation (kWh)')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.tight_layout()

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                img = Image.open(buf)

                num_panels_text = f"{min_panels} panels ({panel_length}m x {panel_width}m)"
                num_batteries_text = f"{number_of_batteries} batteries (Rating: {battery_capacity}Ah, {battery_voltage}V)"

                return num_panels_text, num_batteries_text, total_battery_capacity, img

            btn_design_system.click(
                design_pv_system_action,
                inputs=[panel_length, panel_width, panel_efficiency, inverter_efficiency, state,
                        daily_target_energy, autonomy_days, battery_voltage, depth_of_discharge,
                        battery_efficiency, battery_capacity],
                outputs=[num_panels_output, num_batteries_output, total_battery_capacity_output, monthly_generation_output]
            )

        # Code Block 3: Cost Simulation
        with gr.Tab("Cost Simulation"):
            gr.Markdown("### PV System Cost Simulation")

            # Procurement costs
            solar_panel_unit_cost = gr.Number(label="Solar Panel Unit Cost (₦)", value=50000)
            controller_cost = gr.Number(label="Charge Controller Cost (₦)", value=20000)
            inverter_cost = gr.Number(label="Inverter Cost (₦)", value=100000)
            battery_unit_cost = gr.Number(label="Battery Unit Cost (₦)", value=60000)
            misc_procurement_cost = gr.Number(label="Miscellaneous Procurement Costs (₦)", value=10000)

            # Installation costs
            solar_panel_install_cost = gr.Number(label="Installation Cost per Solar Panel (₦)", value=5000)
            controller_install_cost = gr.Number(label="Installation Cost of Charge Controller (₦)", value=2000)
            inverter_install_cost = gr.Number(label="Installation Cost of Inverter (₦)", value=5000)
            battery_install_cost = gr.Number(label="Installation Cost per Battery (₦)", value=3000)
            misc_install_cost = gr.Number(label="Miscellaneous Installation Costs (₦)", value=5000)

            # Maintenance details
            maintenance_visits_per_year = gr.Number(label="Maintenance Visits per Year", value=2)
            warranty_years = gr.Number(label="Warranty Years", value=2)
            grid_rate = gr.Number(label="Grid Electricity Rate (₦/kWh)", value=50)
            inflation_rate = gr.Slider(minimum=0, maximum=100, label="Inflation Rate (%)", value=10)
            num_years = gr.Number(label="Number of Years for Simulation", value=10)

            # Maintenance costs
            maintenance_cost_per_panel = gr.Number(label="Maintenance Cost per Solar Panel (₦)", value=500)
            maintenance_cost_controller = gr.Number(label="Maintenance Cost of Charge Controller (₦)", value=500)
            maintenance_cost_inverter = gr.Number(label="Maintenance Cost of Inverter (₦)", value=1000)
            maintenance_cost_per_battery = gr.Number(label="Maintenance Cost per Battery (₦)", value=500)
            maintenance_misc_cost = gr.Number(label="Miscellaneous Maintenance Costs (₦)", value=500)

            btn_simulate_cost = gr.Button("Simulate Costs")

            cost_table_output = gr.Dataframe(label="Cost Table")
            annual_cost_plot = gr.Plot(label="Annual Cost Comparison")
            cumulative_cost_plot = gr.Plot(label="Cumulative Life Cycle Cost Comparison")

            def simulate_costs_action(panel_length, panel_width, panel_efficiency, inverter_efficiency, state,
                                      daily_target_energy, autonomy_days, battery_voltage, depth_of_discharge,
                                      battery_efficiency, battery_capacity,
                                      solar_panel_unit_cost, controller_cost, inverter_cost, battery_unit_cost, misc_procurement_cost,
                                      solar_panel_install_cost, controller_install_cost, inverter_install_cost, battery_install_cost, misc_install_cost,
                                      maintenance_visits_per_year, warranty_years, grid_rate, inflation_rate, num_years,
                                      maintenance_cost_per_panel, maintenance_cost_controller, maintenance_cost_inverter,
                                      maintenance_cost_per_battery, maintenance_misc_cost):
                # Reuse calculations from previous code blocks
                ghi_value = ghi[state]
                panel_area = panel_length * panel_width
                panel_efficiency /= 100
                inverter_efficiency /= 100

                months = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
                monthly_factors = [monthly_variation_factors[month] for month in months]

                monthly_pv_potential = [ghi_value * panel_area * panel_efficiency * inverter_efficiency * factor
                                        for factor in monthly_factors]

                min_pv_potential = min(monthly_pv_potential)
                min_panels = math.ceil(daily_target_energy / min_pv_potential)

                depth_of_discharge /= 100
                battery_efficiency /= 100
                total_battery_capacity = (((daily_target_energy * autonomy_days * 1000) / battery_voltage)
                                          * (1 / battery_efficiency) * (1 / depth_of_discharge))
                total_battery_capacity = math.ceil(total_battery_capacity)
                number_of_batteries = math.ceil(total_battery_capacity / battery_capacity)

                # Procurement and installation costs
                total_procurement_cost = (solar_panel_unit_cost * min_panels) + controller_cost + inverter_cost + (battery_unit_cost * number_of_batteries) + misc_procurement_cost
                total_installation_cost = (solar_panel_install_cost * min_panels) + controller_install_cost + inverter_install_cost + (battery_install_cost * number_of_batteries) + misc_install_cost
                commission_cost = total_procurement_cost + total_installation_cost

                # Maintenance costs
                maintenance_cost = (maintenance_cost_per_panel * min_panels) + maintenance_cost_controller + maintenance_cost_inverter + (maintenance_cost_per_battery * number_of_batteries) + maintenance_misc_cost
                usage_cost = maintenance_cost * maintenance_visits_per_year
                inflation_rate /= 100

                # Initialize cost tables
                pv_cost_table = []
                grid_cost_table = []

                for i in range(int(num_years)):
                    # Grid cost
                    if i == 0:
                        grid_cost_table.append(daily_target_energy * grid_rate * 365)
                    else:
                        grid_cost_table.append(grid_cost_table[i-1] * (1 + inflation_rate))

                    # PV cost
                    if warranty_years > 0 and i < warranty_years:
                        pv_cost_table.append(0)
                    else:
                        pv_cost_table.append(usage_cost * ((1 + inflation_rate) ** i))

                # Include commissioning cost
                if commission_cost is not None:
                    pv_cost_table[0] += commission_cost

                # Create DataFrame
                cost_data = {
                    'Year': list(range(1, int(num_years) + 1)),
                    'PV Cost': pv_cost_table,
                    'Grid Cost': grid_cost_table
                }
                cost_df = pd.DataFrame(cost_data)
                cost_df['Cumulative PV Cost'] = cost_df['PV Cost'].cumsum()
                cost_df['Cumulative Grid Cost'] = cost_df['Grid Cost'].cumsum()

                # Plotting
                fig1 = px.line(cost_df, x='Year', y=['PV Cost', 'Grid Cost'],
                               labels={'value': 'Cost (₦)', 'variable': 'Energy Source'},
                               title=f'Annual Cost of Electricity: PV System vs Grid Supply over {int(num_years)} Years')
                fig1.update_layout(legend_title_text='Energy Source')

                fig2 = px.line(cost_df, x='Year', y=['Cumulative PV Cost', 'Cumulative Grid Cost'],
                               labels={'value': 'Cumulative Cost (₦)', 'variable': 'Energy Source'},
                               title=f'{int(num_years)}-Year Cumulative Life Cycle Cost Comparison: PV System vs Grid Electricity')
                fig2.update_layout(legend_title_text='Energy Source')

                return cost_df, fig1, fig2

            btn_simulate_cost.click(
                simulate_costs_action,
                inputs=[panel_length, panel_width, panel_efficiency, inverter_efficiency, state,
                        daily_target_energy, autonomy_days, battery_voltage, depth_of_discharge,
                        battery_efficiency, battery_capacity,
                        solar_panel_unit_cost, controller_cost, inverter_cost, battery_unit_cost, misc_procurement_cost,
                        solar_panel_install_cost, controller_install_cost, inverter_install_cost, battery_install_cost, misc_install_cost,
                        maintenance_visits_per_year, warranty_years, grid_rate, inflation_rate, num_years,
                        maintenance_cost_per_panel, maintenance_cost_controller, maintenance_cost_inverter,
                        maintenance_cost_per_battery, maintenance_misc_cost],
                outputs=[cost_table_output, annual_cost_plot, cumulative_cost_plot]
            )

        # Code Block 4: Carbon Emission Matrix
        with gr.Tab("Carbon Emission Matrix"):
            gr.Markdown("### Carbon Emission Matrix")

            num_years_emission = gr.Number(label="Number of Years for Carbon Emissions Assessment", value=10)
            daily_target_energy_emission = gr.Number(label="Daily Target Energy (kWh)", value=10)

            btn_calculate_emissions = gr.Button("Calculate Carbon Emissions")

            grid_emissions_output = gr.Textbox(label="Grid Electricity Emissions")
            solar_emissions_output = gr.Textbox(label="PV System Solar Energy Emissions")
            emissions_plot = gr.Plot(label="Carbon Emissions Comparison")

            def calculate_emissions_action(num_years_emission, daily_target_energy_emission):
                # Carbon factors
                grid_cf = 402  # gCO2/kWh
                solar_cf = 41  # gCO2/kWh

                # Calculate carbon emissions per day
                grid_emission = daily_target_energy_emission * grid_cf / 1000  # kgCO2/day
                solar_emission = daily_target_energy_emission * solar_cf / 1000  # kgCO2/day

                # Total emissions over the years
                total_grid_emission = grid_emission * 365 * num_years_emission
                total_solar_emission = solar_emission * 365 * num_years_emission

                # Data for pie chart
                data = {
                    'Energy Source': ['Grid Electricity', 'PV System Solar Energy'],
                    'Carbon Emission (kgCO2)': [total_grid_emission, total_solar_emission]
                }

                fig = px.pie(data, values='Carbon Emission (kgCO2)', names='Energy Source',
                             title=f'Carbon Emissions over {int(num_years_emission)} Years',
                             color_discrete_sequence=['#0077c2', '#FDB813'])
                fig.update_traces(textposition='inside', textinfo='percent+label')

                grid_emissions_text = f"Total carbon emissions from Grid Electricity over {int(num_years_emission)} years: {total_grid_emission:,.2f} kgCO₂"
                solar_emissions_text = f"Total carbon emissions from PV System's Solar Energy over {int(num_years_emission)} years: {total_solar_emission:,.2f} kgCO₂"

                return grid_emissions_text, solar_emissions_text, fig

            btn_calculate_emissions.click(
                calculate_emissions_action,
                inputs=[num_years_emission, daily_target_energy_emission],
                outputs=[grid_emissions_output, solar_emissions_output, emissions_plot]
            )

    app.launch()

if __name__ == "__main__":
    main()
