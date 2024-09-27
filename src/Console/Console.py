import sys
sys.path.append("src")
from LiquidacionNomina import Liquida_nomina

detalles = {}
def validate_empty(value):
    return value if value else "0"


print("<<< PROGRAM RUNNING >>>")
print("::::::::::::::::::::::::::::::::")
print("**NOTE: For data that does not apply to your profile, please leave it blank, just press ENTER and continue with the next data point")
print("----------------------------------------------------------------------")
monthly_salary = validate_empty(input("Enter your monthly income ($COP):"))
weeks_worked = validate_empty(input("Enter the number of weeks worked to settle:"))
time_worked_on_holidays = validate_empty(input("Enter the hours worked on holidays (ONLY IF APPLICABLE):"))
overtime_day_hours = validate_empty(input("Enter the number of daytime overtime hours worked (ONLY IF APPLICABLE):"))
overtime_night_hours = validate_empty(input("Enter the number of nighttime overtime hours worked (ONLY IF APPLICABLE):"))
overtime_holiday_hours = validate_empty(input("Enter the overtime hours worked on holidays (ONLY IF APPLICABLE):"))
leave_days = validate_empty(input("Enter the number of days you had on leave during the working period (ONLY IF APPLICABLE):"))
sick_days = validate_empty(input("If you had any sick leave during the working period, enter the number of days (ONLY IF APPLICABLE):"))

try:
    liquidacion = Liquida_nomina.Liquidacion(
        monthly_salary=monthly_salary, weeks_worked=weeks_worked, time_worked_on_holidays=time_worked_on_holidays,
                                  overtime_day_hours=overtime_day_hours, overtime_night_hours=overtime_night_hours, 
                                overtime_holiday_hours=overtime_holiday_hours, leave_days=leave_days, sick_days=sick_days
    )
    total_payment, detalles= liquidacion.CalcularLiquidacion()
    print(f"The total amount of your settlement is: {total_payment}")
except Exception as up_error:
    print("*** ERROR ***")
    print(str(up_error))
