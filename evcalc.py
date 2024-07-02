import streamlit as st
import pandas as pd
import base64

# Define the EV energy calculator function
def ev_energy_calculator():
    st.title("EV Energy Calculator")

    # User choice
    calc_option = st.radio(
        "Choose the calculation type:",
        ('Total Power Capacity', 'Number of EVs Charging per Day')
    )

    if calc_option == 'Total Power Capacity':
        # Inputs for total power capacity calculation
        total_power = st.number_input("Enter Total Available Power Capacity (kW):", min_value=0.0)
        avg_power_per_ev = st.number_input("Enter Average Power Consumption per EV (kW):", min_value=0.0)
        peak_hours = st.number_input("Enter Charging Hours per Day (Peak):", min_value=0.0)
        non_peak_hours = st.number_input("Enter Charging Hours per Day (Non-Peak):", min_value=0.0)
        charging_days = st.number_input("Enter Charging Days per Year:", min_value=0)
        peak_rate = st.number_input("Enter Utility Rate (Peak) ($ per kWh):", min_value=0.0)
        non_peak_rate = st.number_input("Enter Utility Rate (Non-Peak) ($ per kWh):", min_value=0.0)
        avg_charge_time_per_ev = st.number_input("Enter Hours to charge average per vehicle when needed:", min_value=0.0)

        if st.button('Calculate'):
            try:
                # Calculations
                max_evs_supported = total_power / avg_power_per_ev
                peak_energy = max_evs_supported * avg_power_per_ev * peak_hours * charging_days
                non_peak_energy = max_evs_supported * avg_power_per_ev * non_peak_hours * charging_days
                annual_cost_peak = peak_energy * peak_rate
                annual_cost_non_peak = non_peak_energy * non_peak_rate
                total_annual_cost = annual_cost_peak + annual_cost_non_peak
                total_charge_time_all_evs = max_evs_supported * avg_charge_time_per_ev

                # Display results
                st.success(f"Max EVs Supported: {max_evs_supported:.2f}")
                st.success(f"Total Energy Consumption per Year (Peak): {peak_energy:.2f} kWh")
                st.success(f"Total Energy Consumption per Year (Non-Peak): {non_peak_energy:.2f} kWh")
                st.success(f"Annual Cost of Energy (Peak): ${annual_cost_peak:.2f}")
                st.success(f"Annual Cost of Energy (Non-Peak): ${annual_cost_non_peak:.2f}")
                st.success(f"Total Annual Cost of Energy: ${total_annual_cost:.2f}")
                st.success(f"Total Hours to Charge All Vehicles: {total_charge_time_all_evs:.2f} hours")

                # Prepare data for CSV
                data = {
                    'Description': ['Max EVs Supported', 'Total Energy Consumption per Year (Peak)', 'Total Energy Consumption per Year (Non-Peak)', 
                                    'Annual Cost of Energy (Peak)', 'Annual Cost of Energy (Non-Peak)', 'Total Annual Cost of Energy', 'Total Hours to Charge All Vehicles'],
                    'Value': [max_evs_supported, peak_energy, non_peak_energy, annual_cost_peak, annual_cost_non_peak, total_annual_cost, total_charge_time_all_evs]
                }
                df = pd.DataFrame(data)
                
                # Convert DataFrame to CSV
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="ev_energy_calculator_results.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)

            except ValueError:
                st.error("Please enter valid numbers for all fields.")

    elif calc_option == 'Number of EVs Charging per Day':
        # Inputs for number of EVs charging per day calculation
        total_cars_per_day = st.number_input("Enter Total # of cars charging per day:", min_value=0)
        avg_capacity_ev = st.number_input("Enter Average Capacity of EVs (kWh):", min_value=0.0)
        peak_hours = st.number_input("Enter Charging Hours per Day (Peak):", min_value=0.0)
        non_peak_hours = st.number_input("Enter Charging Hours per Day (Non-Peak):", min_value=0.0)
        charging_days = st.number_input("Enter Charging Days per Year:", min_value=0)
        peak_rate = st.number_input("Enter Utility Rate (Peak) ($ per kWh):", min_value=0.0)
        non_peak_rate = st.number_input("Enter Utility Rate (Non-Peak) ($ per kWh):", min_value=0.0)
        avg_charge_time_per_ev = st.number_input("Enter Hours to charge average per vehicle when needed:", min_value=0.0)

        if st.button('Calculate'):
            try:
                # Calculations
                energy_needed_per_day = total_cars_per_day * avg_capacity_ev
                energy_needed_per_year = energy_needed_per_day * charging_days
                peak_energy = total_cars_per_day * avg_capacity_ev * peak_hours * charging_days
                non_peak_energy = total_cars_per_day * avg_capacity_ev * non_peak_hours * charging_days
                annual_cost_peak = peak_energy * peak_rate
                annual_cost_non_peak = non_peak_energy * non_peak_rate
                total_annual_cost = annual_cost_peak + annual_cost_non_peak
                total_charge_time_all_evs = total_cars_per_day * avg_charge_time_per_ev

                # Display results
                st.success(f"Total Energy Needed per Day: {energy_needed_per_day:.2f} kWh")
                st.success(f"Total Energy Needed per Year: {energy_needed_per_year:.2f} kWh")
                st.success(f"Total Energy Consumption per Year (Peak): {peak_energy:.2f} kWh")
                st.success(f"Total Energy Consumption per Year (Non-Peak): {non_peak_energy:.2f} kWh")
                st.success(f"Annual Cost of Energy (Peak): ${annual_cost_peak:.2f}")
                st.success(f"Annual Cost of Energy (Non-Peak): ${annual_cost_non_peak:.2f}")
                st.success(f"Total Annual Cost of Energy: ${total_annual_cost:.2f}")
                st.success(f"Total Hours to Charge All Vehicles: {total_charge_time_all_evs:.2f} hours")

                # Prepare data for CSV
                data = {
                    'Description': ['Total Energy Needed per Day', 'Total Energy Needed per Year', 'Total Energy Consumption per Year (Peak)', 
                                    'Total Energy Consumption per Year (Non-Peak)', 'Annual Cost of Energy (Peak)', 'Annual Cost of Energy (Non-Peak)', 
                                    'Total Annual Cost of Energy', 'Total Hours to Charge All Vehicles'],
                    'Value': [energy_needed_per_day, energy_needed_per_year, peak_energy, non_peak_energy, annual_cost_peak, annual_cost_non_peak, 
                              total_annual_cost, total_charge_time_all_evs]
                }
                df = pd.DataFrame(data)
                
                # Convert DataFrame to CSV
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="ev_energy_calculator_results.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)

            except ValueError:
                st.error("Please enter valid numbers for all fields.")

# Run the calculator
if __name__ == '__main__':
    ev_energy_calculator()
