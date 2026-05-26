from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    FloatField,
    IntegerField,
    DateField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional
)


# ---------------- LOGIN ----------------

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")


# ---------------- REGISTER ----------------

class RegisterForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=120)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    occupation = StringField(
        "Occupation",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

    monthly_income = FloatField(
        "Monthly Income",
        validators=[
            Optional(),
            NumberRange(min=0)
        ]
    )

    dependents = IntegerField(
        "Dependents",
        validators=[
            Optional(),
            NumberRange(min=0)
        ]
    )

    submit = SubmitField("Register")


# ---------------- PROFILE ----------------

class ProfileForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=120)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            Optional(),
            Length(min=6)
        ]
    )

    occupation = StringField(
        "Occupation",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

    monthly_income = FloatField(
        "Monthly Income",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    dependents = IntegerField(
        "Dependents",
        validators=[
            Optional(),
            NumberRange(min=0)
        ]
    )

    submit = SubmitField("Save Profile")


# ---------------- EXPENSE ----------------

class ExpenseForm(FlaskForm):

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    category = StringField(
        "Category",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    note = StringField(
        "Note",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    expense_date = DateField(
        "Date",
        validators=[
            DataRequired()
        ],
        format="%Y-%m-%d"
    )

    submit = SubmitField("Add Expense")


# ---------------- GOALS ----------------

class GoalForm(FlaskForm):

    goal_name = StringField(
        "Goal Name",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    target_amount = FloatField(
        "Target Amount",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    current_amount = FloatField(
        "Current Amount",
        validators=[
            Optional(),
            NumberRange(min=0)
        ]
    )

    deadline = DateField(
        "Deadline",
        validators=[
            Optional()
        ],
        format="%Y-%m-%d"
    )

    submit = SubmitField("Add Goal")