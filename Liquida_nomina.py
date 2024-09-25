import sys
import re
sys.path.append("src/LiquidacionNomina")
from LiquidacionNomina import Validations

class Liquidacion():
    def __init__(self,monthly_salary, weeks_worked, time_worked_on_holidays=0, overtime_day_hours=0,
                 overtime_night_hours=0, overtime_holiday_hours=0, leave_days=0, sick_days=0):
        
        self.variables = {
            'monthly_salary': [monthly_salary, True],
            'weeks_worked' :[weeks_worked, False],
            'time_worked_on_holidays':  [time_worked_on_holidays, False],
            'overtime_day_hours': [overtime_day_hours, False],
            'overtime_night_hours': [overtime_night_hours, False],
            'overtime_holiday_hours': [overtime_holiday_hours, False],
            'leave_days': [leave_days, True],
            'sick_days': [sick_days, True]
        }
        

    def CalcularLiquidacion(self):
        """
        Calculates the payroll settlement for employees in Colombia.
        """
        self.variables = Validations.validate_variables(self.variables)
        
        TOTAL_DAYS_IN_MONTH = 30
        DAILY_WORKING_HOURS = 8
        MAXIMUM_SALARY_WITH_TRANSPORT_ALLOWANCE = 2600000
        TOTAL_WORK_DAYS_PER_WEEK = 6
        VALUE_PER_HOUR_WORKED_ON_HOLIDAY = 1.75
        VALUE_PER_OVERTIME_DAY_HOUR = 1.25
        VALUE_PER_OVERTIME_NIGHT_HOUR = 1.75
        VALUE_PER_OVERTIME_HOLIDAY_HOUR = 2
        PERCENTAGE_TO_DEDUCT_FOR_HEALTH = 0.04
        PERCENTAGE_TO_DEDUCT_FOR_PENSION = 0.04
        PERCENTAGE_TO_DEDUCT_FOR_SOLIDARITY_FUND = 0.01
        SALARY_TO_DEDUCT_FOR_FUND = 4000000
        PERCENTAGE_TO_DEDUCT_FOR_WITHHOLDING = 0.05
        SALARY_TO_DEDUCT_FOR_WITHHOLDING = 4300000
        PERCENTAGE_TO_DEDUCT_FOR_DISABILITY = 0.333
        
        if self.variables['weeks_worked'][0]== 0:
            raise Validations.ZeroWeeksWorked("INVALID VALUE: Weeks worked must be a number greater than or equal to 1.")
        
        if self.variables['time_worked_on_holidays'][0] > DAILY_WORKING_HOURS:
            raise Validations.MoreThan8HoursWorkedOnHoliday("INVALID VALUE: Time worked on holidays cannot be more than 8 hours.")
        
        days_worked = self.variables['weeks_worked'][0] * TOTAL_WORK_DAYS_PER_WEEK  # Convert weeks to days worked

        # Initial calculations
        transport_allowance = 162000 if self.variables['monthly_salary'][0] <= MAXIMUM_SALARY_WITH_TRANSPORT_ALLOWANCE else 0
        daily_salary = self.variables['monthly_salary'][0] / TOTAL_DAYS_IN_MONTH
        hourly_salary = daily_salary / DAILY_WORKING_HOURS
        
        # Calculation of additional payments
        earnings_for_holidays = self.variables['time_worked_on_holidays'][0] * hourly_salary * VALUE_PER_HOUR_WORKED_ON_HOLIDAY 
        earnings_for_overtime_day = self.variables['overtime_day_hours'][0] * hourly_salary * VALUE_PER_OVERTIME_DAY_HOUR
        earnings_for_overtime_night = self.variables['overtime_night_hours'][0] * hourly_salary * VALUE_PER_OVERTIME_NIGHT_HOUR
        earnings_for_overtime_holidays = self.variables['overtime_holiday_hours'][0] * hourly_salary * VALUE_PER_OVERTIME_HOLIDAY_HOUR

        # Total income
        total_income = (daily_salary * days_worked) + transport_allowance + earnings_for_holidays + \
                    earnings_for_overtime_day + earnings_for_overtime_night + earnings_for_overtime_holidays
            
        # Deductions
        health_deduction = total_income * PERCENTAGE_TO_DEDUCT_FOR_HEALTH
        pension_deduction = total_income * PERCENTAGE_TO_DEDUCT_FOR_PENSION
        solidarity_fund_deduction = total_income * PERCENTAGE_TO_DEDUCT_FOR_SOLIDARITY_FUND if self.variables['monthly_salary'][0] > SALARY_TO_DEDUCT_FOR_FUND else 0
        leave_payment = self.variables['leave_days'][0] * daily_salary
        withholding_tax = total_income * PERCENTAGE_TO_DEDUCT_FOR_WITHHOLDING if self.variables['monthly_salary'][0] > SALARY_TO_DEDUCT_FOR_WITHHOLDING else 0
        disability_deduction = self.variables['sick_days'][0] * daily_salary * PERCENTAGE_TO_DEDUCT_FOR_DISABILITY

        # Total amount to receive
        total_settlement = total_income - (health_deduction + pension_deduction + solidarity_fund_deduction + disability_deduction + 
                                        leave_payment + withholding_tax)
        
        return round(total_settlement, 2)
