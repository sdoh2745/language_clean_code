from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import sys
sys.path.append("src")
from LiquidacionNomina.Liquida_nomina import Liquidacion
from LiquidacionNomina.Validations import *

class NominaCalculatorApp(App):
    def build(self):
        contenedor = BoxLayout(orientation='vertical')

        # Cambiar el color de fondo
        contenedor.canvas.before.clear()
        with contenedor.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.8, 0.9, 1, 1)  # Celeste pastel
            self.rect = Rectangle(size=contenedor.size, pos=contenedor.pos)

        contenedor.bind(size=self._update_rect, pos=self._update_rect)
        
        contenedor.add_widget(Label(text= "NominaCalculator APP", color=(0, 0, 0, 1), bold=True))
        contenedor.add_widget(Label(text="NOTA: Si deja un campo vacío, automáticamente se le asignará cero 0 ", color=(0, 0, 0, 1),font_size='12sp'))

        contenedor.add_widget(Label(text='Salario Mensual:', color=(0, 0, 0, 1)))
        self.salary_input = TextInput(multiline=False)
        contenedor.add_widget(self.salary_input)

        contenedor.add_widget(Label(text='Semanas Trabajadas:', color=(0, 0, 0, 1)))
        self.weeks_input = TextInput(multiline=False)
        contenedor.add_widget(self.weeks_input)

        contenedor.add_widget(Label(text='Tiempo Trabajado en Festivos:', color=(0, 0, 0, 1)))
        self.holiday_time_input = TextInput(multiline=False)
        contenedor.add_widget(self.holiday_time_input)

        contenedor.add_widget(Label(text='Horas Extras Diurnas:', color=(0, 0, 0, 1)))
        self.overtime_day_input = TextInput(multiline=False)
        contenedor.add_widget(self.overtime_day_input)

        contenedor.add_widget(Label(text='Horas Extras Nocturnas:', color=(0, 0, 0, 1)))
        self.overtime_night_input = TextInput(multiline=False)
        contenedor.add_widget(self.overtime_night_input)

        contenedor.add_widget(Label(text='Horas Extras Festivos:', color=(0, 0, 0, 1)))
        self.overtime_holiday_input = TextInput(multiline=False)
        contenedor.add_widget(self.overtime_holiday_input)

        contenedor.add_widget(Label(text='Días de licencia:', color=(0, 0, 0, 1)))
        self.leave_days_input = TextInput(multiline=False)
        contenedor.add_widget(self.leave_days_input)

        contenedor.add_widget(Label(text='Días de incapacidad:', color=(0, 0, 0, 1)))
        self.sick_day_input = TextInput(multiline=False)
        contenedor.add_widget(self.sick_day_input)

        contenedor.add_widget(Label(text=""))

        self.result_label = Label(text='', color=(0, 0, 0, 1), bold=True) 
        contenedor.add_widget(self.result_label)

        # Botón personalizado
        calculate_button = Button(text='Calcular Nómina', size_hint=(None, None), size=(170, 80),
                                  background_color=(0.2, 0.6, 0.7, 1), color=(1, 1, 1, 1), bold=True)
        calculate_button.bind(on_press=self.calculate_nomi)
        centro_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100)
        centro_layout.add_widget(Label(size_hint_x=0.5)) 
        centro_layout.add_widget(calculate_button)
        centro_layout.add_widget(Label(size_hint_x=0.5)) 
        
        contenedor.add_widget(centro_layout)

        contenedor.add_widget(Label(text=""))

        return contenedor

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def calculate_nomi(self, sender):
        try:
            monthly_salary = (self.salary_input.text) if self.salary_input.text else 0
            weeks_worked = (self.weeks_input.text) if self.weeks_input.text else 0
            time_worked_on_holidays = (self.holiday_time_input.text) if self.holiday_time_input.text else 0
            overtime_day_hours = (self.overtime_day_input.text) if self.overtime_day_input.text else 0
            overtime_night_hours = (self.overtime_night_input.text) if self.overtime_night_input.text else 0
            overtime_holiday_hours = (self.overtime_holiday_input.text) if self.overtime_holiday_input.text else 0
            leave_days = (self.leave_days_input.text) if self.leave_days_input.text else 0
            sick_days = (self.sick_day_input.text) if self.sick_day_input.text else 0
            
            # Crear la instancia y calcular
            result = Liquidacion(  monthly_salary=monthly_salary, weeks_worked=weeks_worked, time_worked_on_holidays=time_worked_on_holidays,
                                  overtime_day_hours=overtime_day_hours, overtime_night_hours=overtime_night_hours, 
                                overtime_holiday_hours=overtime_holiday_hours, leave_days=leave_days, sick_days=sick_days)
            
            total_payment = result.CalcularLiquidacion()
            self.result_label.text = f'Total Liquidación de Nomina: ${total_payment}'

        except (NegativeValue, InvalidValue, MoreThan8HoursWorkedOnHoliday, 
                NotAnIntegerValue, CommaSeparator, ZeroWeeksWorked) as error:
            self.mostrar_error(str(error))

        except ValueError :
            text_error = "El valor ingresado no tiene un formato correcto.\nIngrese solo números y use punto como separador decimal"
            self.mostrar_error(text_error)

    def mostrar_error(self, mensaje_error):
        contenedor1 = BoxLayout(orientation='vertical')

        # Añadir la imagen
        imagen = Image(source='src\Recursos\precaution.png', size_hint=(1, 2))  # Ajusta el tamaño según necesites
        contenedor1.add_widget(imagen)

        mensaje = Label(text=mensaje_error, color=(1, 1, 1, 1))
        contenedor1.add_widget(mensaje)

        cerrar = Button(text="Close (X)", size_hint_y=None, height=30,background_color=(1, 0.5, 0.4, 1), color=(1, 1, 1, 1), bold=True)
        contenedor1.add_widget(cerrar)

        ventana = Popup(title="*** ERROR ***", content=contenedor1, size_hint=(0.9, 0.5))
        cerrar.bind(on_press=ventana.dismiss)
        ventana.open()

        return ventana


if __name__ == '__main__':
    NominaCalculatorApp().run()
