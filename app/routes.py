from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import User, Expense, Goal, Prediction
from app.forms import (
    LoginForm,
    RegisterForm,
    ProfileForm,
    ExpenseForm,
    GoalForm
)

from app.ml_service import MLService

ml_service = MLService()


def register_routes(app):

    @app.route("/")
    def index():

        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        return redirect(url_for("login"))

    # ---------------- REGISTER ----------------

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = RegisterForm()

        if form.validate_on_submit():

            existing_user = User.query.filter_by(
                email=form.email.data
            ).first()

            if existing_user:
                flash("Email already registered", "danger")
                return redirect(url_for("register"))

            user = User(
                name=form.name.data,
                email=form.email.data,
                occupation=form.occupation.data,
                monthly_income=form.monthly_income.data or 0,
                dependents=form.dependents.data or 0
            )

            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(url_for("login"))

        return render_template(
            "register.html",
            form=form
        )

    # ---------------- LOGIN ----------------

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = LoginForm()

        if form.validate_on_submit():

            user = User.query.filter_by(
                email=form.email.data
            ).first()

            if user and user.check_password(form.password.data):

                login_user(user)

                flash("Login successful", "success")

                return redirect(url_for("dashboard"))

            flash("Invalid email or password", "danger")

        return render_template(
            "login.html",
            form=form
        )

    # ---------------- LOGOUT ----------------

    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        flash("Logged out successfully", "info")

        return redirect(url_for("login"))

    # ---------------- PROFILE ----------------

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():

        form = ProfileForm(obj=current_user)

        if form.validate_on_submit():

            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.occupation = form.occupation.data
            current_user.monthly_income = form.monthly_income.data
            current_user.dependents = form.dependents.data or 0

            if form.password.data:
                current_user.set_password(form.password.data)

            db.session.commit()

            flash("Profile updated successfully", "success")

            return redirect(url_for("dashboard"))

        return render_template(
            "profile.html",
            form=form
        )

    # ---------------- EXPENSE ----------------

    @app.route("/expense", methods=["GET", "POST"])
    @login_required
    def expense():

        form = ExpenseForm()

        if form.validate_on_submit():

            expense = Expense(
                user_id=current_user.id,
                amount=form.amount.data,
                category=form.category.data,
                note=form.note.data,
                expense_date=form.expense_date.data
            )

            db.session.add(expense)
            db.session.commit()

            flash("Expense added successfully", "success")

            return redirect(url_for("dashboard"))

        return render_template(
            "expense.html",
            form=form
        )

    # ---------------- GOALS ----------------

    @app.route("/goals", methods=["GET", "POST"])
    @login_required
    def goals():

        form = GoalForm()

        if form.validate_on_submit():

            goal = Goal(
                user_id=current_user.id,
                goal_name=form.goal_name.data,
                target_amount=form.target_amount.data,
                current_amount=form.current_amount.data or 0.0,
                deadline=form.deadline.data
            )

            db.session.add(goal)
            db.session.commit()

            flash("Goal added successfully", "success")

            return redirect(url_for("goals"))

        goals = Goal.query.filter_by(
            user_id=current_user.id
        ).all()

        return render_template(
            "goals.html",
            form=form,
            goals=goals
        )

    # ---------------- DASHBOARD ----------------

    @app.route("/dashboard")
    @login_required
    def dashboard():

        expenses = Expense.query.filter_by(
            user_id=current_user.id
        ).all()

        total_spent = sum(
            expense.amount for expense in expenses
        )

        monthly_income = current_user.monthly_income or 0

        savings_rate = 0

        if monthly_income > 0:
            savings_rate = max(
                (monthly_income - total_spent) / monthly_income,
                0
            )

        fixed_expenses = sum(
            expense.amount
            for expense in expenses
            if expense.category.lower() in [
                "bills",
                "rent",
                "emi",
                "subscription"
            ]
        )

        daily_avg = total_spent / max(len(expenses), 1)

        risk_label, confidence = ml_service.predict_risk(
            income=monthly_income,
            fixed_expenses=fixed_expenses,
            daily_avg=daily_avg,
            savings_rate=savings_rate
        )

        safety_net_amount = ml_service.safety_net(
            fixed_expenses + (daily_avg * 30)
        )

        prediction = Prediction(
            user_id=current_user.id,
            prediction_type="overspending_risk",
            prediction_value=risk_label,
            confidence=confidence
        )

        db.session.add(prediction)
        db.session.commit()

        goal_count = Goal.query.filter_by(
            user_id=current_user.id
        ).count()

        return render_template(
            "dashboard.html",
            total_spent=total_spent,
            savings_rate=savings_rate,
            risk_label=risk_label,
            confidence=confidence,
            safety_net_amount=safety_net_amount,
            goals=goal_count,
            expenses=expenses
        )