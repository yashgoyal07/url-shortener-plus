import time
import uuid
import logging
from flask import render_template, request, session, flash, redirect, url_for
from application import app
from helpers.utils import is_registered_customer, short_code_generator, is_customer
from controllers.links_controller import LinksController
from controllers.customers_controller import CustomersController


app.secret_key = b'\xce\xdd(B\xdd\xf1\x19\x04\x8c\xf0 BV\x93e\x8c'


@app.route('/sl/<slink_id>')
def redirection(slink_id):
    try:
        start_time = time.time()
        result = LinksController().get_long_link(slink_id=slink_id)
        time_taken = (time.time() - start_time)*1000
        print(f'time taken by cache {time_taken} ms')

        if result:
            return redirect(result.decode())

        start = time.time()
        long_link = LinksController().find_long_link(slink_id)
        time_ = (time.time() - start)*1000
        print(f'time taken by db {time_}')

        if not long_link:
            raise Exception("link not found")

        LinksController().set_long_link(slink_id=slink_id, long_link=long_link)
        return redirect(long_link)
    except Exception as err:
        logging.error(f'error from redirection occurred due to {err}')
        return "Link Expired or Not Exist"


@app.route('/')
def slink():
    try:
        if is_registered_customer():
            cus_id = session['cus_id']
            return render_template('slink.html', customer_id=cus_id)
        if not is_customer():
            cus_id = uuid.uuid4().hex
            CustomersController().create_user(cus_id=cus_id)
            session['cus_id'] = cus_id
    except Exception as err:
        flash('Something Went Wrong. Try Again', 'danger')
        logging.error(f'error from slink occurred due to {err}')
    return render_template('slink.html')


@app.route('/slink_it', methods=['POST'])
def slink_it():
    if is_registered_customer() or is_customer():
        long_link = request.form.get('long_link')
        if long_link:
            try:
                short_code = short_code_generator()
                LinksController().create_slink(slink=short_code, long_link=long_link,
                                               customer_id=session['cus_id'])
                LinksController().set_long_link(slink_id=short_code, long_link=long_link)
                flash('Slink Created', 'success')
                return redirect(url_for('panel'))
            except Exception as err:
                flash('Something Went Wrong. Try Again', 'danger')
                logging.error(f'error from slink_it occurred due to {err}')
    else:
        flash('Please Retry', 'danger')
    return render_template('slink.html')


@app.route('/panel')
def panel():
    if is_registered_customer() or is_customer():
        try:
            customer_id = session['cus_id']
            result = LinksController().show_slink(customer_id=customer_id)
            if not is_registered_customer():
                return render_template('panel.html', slink_data=result)
            customer_status = session['Registered']
            return render_template('panel.html', cus_status=customer_status, slink_data=result)
        except Exception as err:
            flash('Something Went Wrong. Try Again', 'danger')
            logging.error(f'error from panel occurred due to {err}')
    return redirect(url_for('slink'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_registered_customer():
        return redirect('panel')
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
            return redirect(url_for('panel'))
        except Exception as err:
            flash('Email or Password is incorrect', 'danger')
            logging.error(f'error from login occurred due to {err}')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('cus_id', None)
    session.pop('Registered', None)
    return redirect(url_for('slink'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if is_registered_customer():
        return redirect('panel')
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
                    CustomersController().update_customer(name=name.lower(), email=email.lower(), mobile=mobile.lower(), password=password, cus_id=session['cus_id'])
                    session['Registered'] = 'Y'
                else:
                    cus_id = uuid.uuid4().hex
                    CustomersController().create_customer(cus_id=cus_id, name=name.lower(), email=email.lower(), mobile=mobile.lower(), password=password.lower())
                    session['cus_id'] = cus_id
                    session['Registered'] = 'Y'
                flash('You are Successfully Registered', 'success')
                return redirect(url_for('panel'))
            else:
                flash('This email id is already exist.', 'danger')
        except Exception as err:
            flash('Something Went Wrong. Try Again', 'danger')
            logging.error(f'error from signup occurred due to {err}')
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
