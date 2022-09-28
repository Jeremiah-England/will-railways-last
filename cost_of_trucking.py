"""
See: https://www.thetruckersreport.com/infographics/cost-of-trucking/ 
"""

total_cost_per_year = 180_000

total_per_mile = 1.38

fuel_per_mile = 0.54  # Obviously dependent on fuel costs.
# TODO: Calculate this number directly from projections of fuel prices.
gallons_per_year = 20_500

truck_cost_per_mile = 0.24
# That 0.24 is 30_000 annually which is only 1/5 of the new purchase cost of a new truck/trailer.

driver_salary_per_mile = 0.36
# Standard salaries are based on distance driven.
# Drivers spend time on docks and traffic, but they only get paid by the mile.

cost_of_maintenances_per_mile = 0.12
# Issues with air line/hosts, alternators, wiring, and brakes are all common
# in commercial trucks, and can cost 15,000 annually.

insurance_per_mile = 0.05
# Insurance can cost over 6_500 per year.

tires_per_mile = 0.03

permits_licences_and_tolls = 0.02


calculated_total = sum(
    [
        fuel_per_mile,
        truck_cost_per_mile,
        driver_salary_per_mile,
        cost_of_maintenances_per_mile,
        insurance_per_mile,
        tires_per_mile,
        permits_licences_and_tolls,
    ]
)

print(calculated_total)
