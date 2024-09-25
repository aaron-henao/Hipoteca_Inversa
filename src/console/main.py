# main.py
import sys
sys.path.append("src")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

from logic.reverse_mortgage import ReverseMortgageCalculator
from logic.input_validator import InputValidator  # Import InputValidator
from logic.exceptions import (
    DataTypeError,
    InvalidPropertyValueError,
    ExcessivePropertyValueError,
    InvalidInterestRateError,
    InvalidPropertyConditionError,
    InvalidMaritalStatusError
)

# Set window background color
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background

class ReverseMortgageApp(App):
    def build(self):
        self.title = 'Reverse Mortgage Calculator'
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Property Value
        self.layout.add_widget(self.create_label('Property Value:', font_size=16))
        self.property_value_input = self.create_text_input(
            hint_text='Enter the property value (200000000 - 900000000)',
            input_filter='float'
        )
        self.layout.add_widget(self.property_value_input)

        # Property Condition
        self.layout.add_widget(self.create_label('Property Condition:', font_size=16))
        self.property_condition_spinner = Spinner(
            text='Select',
            values=('excellent', 'good', 'average'),
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1),
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.property_condition_spinner)

        # Marital Status
        self.layout.add_widget(self.create_label('Marital Status:', font_size=16))
        self.marital_status_spinner = Spinner(
            text='Select',
            values=('married', 'single', 'divorced'),
            size_hint=(1, 0.1),
            background_color=(0.8, 0.8, 0.8, 1),
            color=(0, 0, 0, 1)
        )
        self.marital_status_spinner.bind(text=self.on_marital_status_change)
        self.layout.add_widget(self.marital_status_spinner)

        # Owner's Age
        self.layout.add_widget(self.create_label("Owner's Age:", font_size=16))
        self.owner_age_input = self.create_text_input(
            hint_text="Enter the owner's age",
            input_filter='int'
        )
        self.layout.add_widget(self.owner_age_input)

        # Spouse's Age (Optional)
        self.spouse_age_label = self.create_label("Spouse's Age (optional):", font_size=16)
        self.spouse_age_input = TextInput(
            hint_text="Enter the spouse's age (if applicable)",
            multiline=False,
            input_filter='int',
            size_hint=(1, 0.1),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
            disabled=True  # Initially disabled
        )
        self.layout.add_widget(self.spouse_age_label)
        self.layout.add_widget(self.spouse_age_input)

        # Interest Rate
        self.layout.add_widget(self.create_label('Interest Rate (e.g., 0.05 for 5%):', font_size=16))
        self.interest_rate_input = self.create_text_input(
            hint_text='Enter the interest rate',
            input_filter='float'
        )
        self.layout.add_widget(self.interest_rate_input)

        # Calculate Button
        calculate_button = Button(
            text='Calculate Monthly Payment',
            size_hint=(1, 0.2),
            font_size=18,
            background_color=(0.2, 0.6, 0.86, 1),  # Blue color
            color=(1, 1, 1, 1)  # White text
        )
        calculate_button.bind(on_press=self.calculate_mortgage)
        self.layout.add_widget(calculate_button)

        return self.layout

    def create_label(self, text, font_size=14):
        """Helper function to create a styled label."""
        return Label(text=text, font_size=font_size, color=(0, 0, 0, 1), size_hint=(1, 0.1))

    def create_text_input(self, hint_text, input_filter='string'):
        """Helper function to create a styled TextInput."""
        return TextInput(
            hint_text=hint_text,
            multiline=False,
            input_filter=input_filter,
            size_hint=(1, 0.1),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1)
        )

    def on_marital_status_change(self, spinner, text):
        """Enable or disable the spouse's age input based on marital status."""
        if text.lower() == 'married':
            self.spouse_age_input.disabled = False
        else:
            self.spouse_age_input.text = ''
            self.spouse_age_input.disabled = True

    def calculate_mortgage(self, instance):
        """Handles the mortgage calculation when the button is pressed."""
        try:
            # Retrieve and convert input values
            property_value_text = self.property_value_input.text
            if not property_value_text:
                raise DataTypeError("Property value is required.")
            property_value = float(property_value_text)

            property_condition = self.property_condition_spinner.text.lower()
            if property_condition == 'select':
                raise InvalidPropertyConditionError("Please select a valid property condition.")

            marital_status = self.marital_status_spinner.text.lower()
            if marital_status == 'select':
                raise InvalidMaritalStatusError("Please select a valid marital status.")

            owner_age_text = self.owner_age_input.text
            if not owner_age_text:
                raise DataTypeError("Owner's age is required.")
            owner_age = int(owner_age_text)

            spouse_age_text = self.spouse_age_input.text
            spouse_age = int(spouse_age_text) if spouse_age_text else None

            interest_rate_text = self.interest_rate_input.text
            if not interest_rate_text:
                raise DataTypeError("Interest rate is required.")
            interest_rate = float(interest_rate_text)

            # Validate the inputs using InputValidator
            validator = InputValidator(
                property_value=property_value,
                property_condition=property_condition,
                marital_status=marital_status,
                owner_age=owner_age,
                spouse_age=spouse_age,
                interest_rate=interest_rate
            )
            validator.validate_inputs()  # Validate all inputs

            # Calculate the monthly payment
            calculator = ReverseMortgageCalculator(
                property_value=property_value,
                property_condition=property_condition,
                marital_status=marital_status,
                owner_age=owner_age,
                spouse_age=spouse_age,
                interest_rate=interest_rate
            )
            monthly_payment = calculator.calculate_monthly_payment()

            # Display the result
            self.show_popup(f"The monthly reverse mortgage payment is: {monthly_payment}", success=True)

        except (DataTypeError, InvalidPropertyValueError, ExcessivePropertyValueError,
                InvalidInterestRateError, InvalidPropertyConditionError, InvalidMaritalStatusError) as e:
            # Display error message
            self.show_popup(f"Error: {str(e)}", success=False)

    def show_popup(self, message, success=True):
        """Helper function to display a popup with a message."""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, halign='center', valign='middle', font_size=16)
        popup_label.bind(size=popup_label.setter('text_size'))

        close_button = Button(
            text='Close',
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 0.2, 1) if success else (0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)  # White text
        )

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title='Success' if success else 'Error',
            content=popup_layout,
            size_hint=(0.75, 0.5),
            auto_dismiss=False
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    ReverseMortgageApp().run()

