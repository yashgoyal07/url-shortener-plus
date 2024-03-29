import logging
import uuid

from flask import render_template, request, session, flash, redirect, url_for

from controllers.customers_controller import CustomersController
from helpers.utils import is_registered_customer, is_customer
from tasks import celery_tasks
from . import auth_blueprint


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
        except ValueError:
            flash('Email or Password is incorrect', 'danger')
        except Exception as err:
            flash('Something Went Wrong. Please Try Again', 'danger')
            logging.error(f'error from login occurred due to {err}')

    return render_template('auth/login.html')


@auth_blueprint.route('/logout')
def logout():
    try:
        session.pop('cus_id', None)
        session.pop('Registered', None)
        flash('You are Successfully Logged Out', 'success')
        return redirect(url_for('main.slink'))
    except Exception as err:
        flash('Something Went Wrong. Please Try Again', 'danger')
        logging.error(f'error from logout occurred due to {err}')


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
                    CustomersController().update_customer(name=name.lower(),
                                                          email=email.lower(),
                                                          mobile=mobile.lower(),
                                                          password=password,
                                                          cus_id=session['cus_id'])

                    session['Registered'] = 'Y'

                    # celery_tasks.update_customer_background.delay(name=name.lower(),
                    #                                               email=email.lower(),
                    #                                               mobile=mobile.lower(),
                    #                                               password=password,
                    #                                               cus_id=session['cus_id'])
                else:
                    cus_id = uuid.uuid4().hex
                    CustomersController().create_customer(cus_id=cus_id,
                                                          name=name.lower(),
                                                          email=email.lower(),
                                                          mobile=mobile.lower(),
                                                          password=password)

                    session['cus_id'] = cus_id
                    session['Registered'] = 'Y'

                    # celery_tasks.create_customer_background.delay(cus_id=cus_id,
                    #                                               name=name.lower(),
                    #                                               email=email.lower(),
                    #                                               mobile=mobile.lower(),
                    #                                               password=password)

                flash('You are Successfully Registered', 'success')
                return redirect(url_for('main.panel'))

                # flash('Registration request submitted', 'success')
            else:
                flash('This email id is already exist.', 'danger')
        except ValueError:
            flash('Please provide all details. Mobile can contain only digits.')
        except Exception as err:
            flash('Something Went Wrong. Please Try Again', 'danger')
            logging.error(f'error from signup occurred due to {err}')
    return render_template('auth/signup.html')
