import uuid
import logging
from flask import render_template, request, session, flash, redirect, url_for
from helpers.utils import is_registered_customer, is_customer
from controllers.customers_controller import CustomersController
from . import auth_blueprint
from tasks import celery_tasks

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if is_registered_customer():
        return redirect('main.panel')
    if request.method == 'POST':
        try:
            customer = request.form
            email = customer.get('email')
            password = customer.get('password')

            # email and password both are mandatory
            if not email or not password:
                raise ValueError

            result = CustomersController().find_customer(email=email.lower(), password=password)

            # if not a valid customer found
            if not result:
                raise ValueError

            session['cus_id'] = result[0].get('customer_id')
            session['Registered'] = 'Y'
            flash('You are Successfully Logged In', 'success')
            return redirect(url_for('main.panel'))
        except Exception as err:
            flash('Email or Password is incorrect', 'danger')
            logging.error(f'error from login occurred due to {err}')

    return render_template('auth/login.html')


@auth_blueprint.route('/logout')
def logout():
    session.pop('cus_id', None)
    session.pop('Registered', None)
    return redirect(url_for('main.slink'))


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if is_registered_customer():
        return redirect('main.panel')
    if request.method == 'POST':
        try:
            customer = request.form
            name = customer.get('name')
            email = customer.get('email')
            mobile = customer.get('mobile')
            password = customer.get('password')

            # mobile no. consists only digits
            if not all((mobile.isnumeric(), email, password)):
                raise ValueError

            result = CustomersController().check_customer(email=email.lower())
            if not result:
                if is_customer():
                    # CustomersController().update_customer(name=name.lower(), email=email.lower(), mobile=mobile.lower(), password=password, cus_id=session['cus_id'])

                    celery_tasks.update_customer_background.delay(name=name.lower(), email=email.lower(), mobile=mobile.lower(), password=password, cus_id=session['cus_id'])

                    session['Registered'] = 'Y'
                else:
                    cus_id = uuid.uuid4().hex
                    # CustomersController().create_customer(cus_id=cus_id, name=name.lower(), email=email.lower(), mobile=mobile.lower(), password=password.lower())

                    celery_tasks.create_customer_background.delay(cus_id=cus_id, name=name.lower(), email=email.lower(), mobile=mobile.lower(), password=password.lower())

                    session['cus_id'] = cus_id
                    session['Registered'] = 'Y'

                # flash('You are Successfully Registered', 'success')

                flash('Registration request submitted', 'success')
                return redirect(url_for('main.panel'))
            else:
                flash('This email id is already exist.', 'danger')
        except Exception as err:
            flash('Something Went Wrong. Try Again', 'danger')
            logging.error(f'error from signup occurred due to {err}')
    return render_template('auth/signup.html')