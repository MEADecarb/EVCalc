import streamlit as st

# Define the EV energy calculator function
def ev_energy_calculator():
    st.title("EV Energy Calculator")

    # Input 1: Vehicle Information
    st.header("Vehicle Information")
    st.write("How many EVs will be needed and how much energy is needed?")

    # Create a form for vehicle information inputs
    with st.form("vehicle_info"):
        total_cars_per_day = st.number_input("Total # of cars charging per day:", min_value=0, value=5, step=1)
        avg_capacity_ev = st.number_input("Average Capacity of EVs (kW/Hr):", min_value=0.0, value=150.0, step=1.0)
        capacity_charging_station = st.number_input("Capacity of Charging Station (kW):", min_value=0.0, value=50.0, step=1.0)
        rate_of_charging_per_hour = st.number_input("Rate of charging per hour (kW/Hr):", min_value=0.0, value=50.0, step=1.0)
        miles_per_vehicle_per_day = st.number_input("Miles Per Vehicle driven per day:", min_value=0.0, value=50.0, step=1.0)
        max_mileage_per_vehicle = st.number_input("Max Mileage Per Vehicle:", min_value=0.0, value=150.0, step=1.0)
        days_of_operation_per_week = st.number_input("Days of Operation per week:", min_value=0, value=5, step=1)
        number_of_stations = st.number_input("Number of Stations (dual port):", min_value=0, value=6, step=1)
        submitted = st.form_submit_button("Calculate")

    # Calculate energy needed
    energy_needed_per_vehicle = (miles_per_vehicle_per_day / max_mileage_per_vehicle) * avg_capacity_ev
    total_energy_needed_per_day = total_cars_per_day * energy_needed_per_vehicle

    # Visual separator
    st.markdown("---")

    # Input 2: Amount of Hours of Charge Needed
    st.header("Amount of Hours of Charge Needed")
    st.write("How long do you have to charge?")

    avg_charge_time_per_ev = energy_needed_per_vehicle / rate_of_charging_per_hour
    total_charge_time_all_evs = (total_energy_needed_per_day / capacity_charging_station) / number_of_stations

    st.success(f"Hours to charge average per vehicle when needed: {avg_charge_time_per_ev:.2f} hours")
    st.warning("If larger than 5 hours, recommend demand rate calculations")
    st.success(f"Hours to charge all vehicles: {total_charge_time_all_evs:.2f} hours (subtract 8 hours from total)")

    # Dynamic adjustment of other inputs
    if submitted:
        st.write("Updated Inputs based on changes:")
        st.write(f"Total Energy Needed per Vehicle: {energy_needed_per_vehicle:.2f} kWh")
        st.write(f"Total Energy Needed per Day: {total_energy_needed_per_day:.2f} kWh")
        st.write(f"Adjusted Average Charge Time per Vehicle: {avg_charge_time_per_ev:.2f} hours")
        st.write(f"Adjusted Total Charge Time for All Vehicles: {total_charge_time_all_evs:.2f} hours")

# Run the calculator
if __name__ == '__main__':
    ev_energy_calculator()
