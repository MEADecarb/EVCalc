import streamlit as st

# Define the EV energy calculator function
def ev_energy_calculator():
    st.title("EV Energy Calculator")

    # User inputs
    total_power = st.number_input("Enter Total Available Power Capacity (kW):", min_value=0.0)
    avg_power_per_ev = st.number_input("Enter Average Power Consumption per EV (kW):", min_value=0.0)
    peak_hours = st.number_input("Enter Charging Hours per Day (Peak):", min_value=0.0)
    non_peak_hours = st.number_input("Enter Charging Hours per Day (Non-Peak):", min_value=0.0)
    charging_days = st.number_input("Enter Charging Days per Year:", min_value=0)
    peak_rate = st.number_input("Enter Utility Rate (Peak) ($ per kWh):", min_value=0.0)
    non_peak_rate = st.number_input("Enter Utility Rate (Non-Peak) ($ per kWh):", min_value=0.0)
    avg_charge_time_per_ev = st.number_input("Enter Hours to charge average per vehicle when needed:", min_value=0.0)
    total_cars_per_day = st.number_input("Enter Total # of cars charging per day:", min_value=0)
    avg_capacity_ev = st.number_input("Enter Average Capacity of EVs (kWh):", min_value=0.0)
    charge_station_capacity = st.number_input("Enter Capacity of Charging Station (kW):", min_value=0.0)
    charge_rate_per_hour = st.number_input("Enter Rate of charging per hour (kW):", min_value=0.0)
    miles_per_day = st.number_input("Enter Miles Per Vehicle driven per day:", min_value=0.0)
    max_mileage_per_ev = st.number_input("Enter Max Mileage per vehicle:", min_value=0.0)
    days_of_operation = st.number_input("Enter Days of Operation per week:", min_value=0)
    num_stations = st.number_input("Enter Number of Stations (dual port):", min_value=0)

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
            energy_needed_per_day = total_cars_per_day * avg_capacity_ev
            energy_needed_per_year = energy_needed_per_day * charging_days
            num_evs_needed = total_cars_per_day

            # Display results
            st.success(f"Max EVs Supported: {max_evs_supported:.2f}")
            st.success(f"Total Energy Consumption per Year (Peak): {peak_energy:.2f} kWh")
            st.success(f"Total Energy Consumption per Year (Non-Peak): {non_peak_energy:.2f} kWh")
            st.success(f"Annual Cost of Energy (Peak): ${annual_cost_peak:.2f}")
            st.success(f"Annual Cost of Energy (Non-Peak): ${annual_cost_non_peak:.2f}")
            st.success(f"Total Annual Cost of Energy: ${total_annual_cost:.2f}")
            st.success(f"Total Hours to Charge All Vehicles: {total_charge_time_all_evs:.2f} hours")
            st.success(f"Total Energy Needed per Day: {energy_needed_per_day:.2f} kWh")
            st.success(f"Total Energy Needed per Year: {energy_needed_per_year:.2f} kWh")
            st.success(f"Number of EVs Needed: {num_evs_needed}")

        except ValueError:
            st.error("Please enter valid numbers for all fields.")

# Run the calculator
if __name__ == '__main__':
    ev_energy_calculator()
