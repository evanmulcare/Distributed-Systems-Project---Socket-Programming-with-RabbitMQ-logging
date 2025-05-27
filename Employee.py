class Employee:
    def __init__(self, emp_id, name, current_salary, past_salary_details, current_annual_leave_entitlement, past_annual_leave_taken):
        self.emp_id = emp_id
        self.name = name
        self.current_salary = current_salary
        self.past_salary_details = past_salary_details
        self.current_annual_leave_entitlement = current_annual_leave_entitlement
        self.past_annual_leave_taken = past_annual_leave_taken
        
    def get_employee_name(self):
        return f"Employee {self.name}:"
    
    def get_current_salary(self):
        if not isinstance(self.current_salary, (int, float)):
            return "Error: Invalid current salary data"
        return f"Current basic salary: {self.current_salary}"

    def get_total_salary_for_year(self, year):
        salary_details = f"Basic pay, {self.current_salary}"
        overtime = self.past_salary_details.get(year, {}).get("Overtime", 0)
        if overtime:
            salary_details += f"; Overtime, {overtime}"
        return f"Total salary for {year}: {salary_details}" 

    def get_current_annual_leave_entitlement(self):
        if not isinstance(self.current_annual_leave_entitlement, int) or self.current_annual_leave_entitlement < 0:
            return "Error: Invalid annual leave entitlement data"
        return f"Current annual leave entitlement: {self.current_annual_leave_entitlement} days"

    def get_leave_taken(self, year):
        leave_taken = self.past_annual_leave_taken.get(year, 0)
        return f"Leave taken in {year}: {leave_taken} days"
