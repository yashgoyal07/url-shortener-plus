import time
import uuid
import logging
from flask import render_template, request, session, flash, redirect, url_for
from helpers.utils import is_registered_customer, short_code_generator, is_customer
from controllers.links_controller import LinksController
from controllers.customers_controller import CustomersController
from . import main_blueprint
from tasks.celery_tasks import create_slink_background

@main_blueprint.route('/sl/<slink_id>')
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


@main_blueprint.route('/')
def slink():
    try:
        if is_registered_customer():
            cus_id = session['cus_id']
            return render_template('main/slink.html', customer_id=cus_id)
    except Exception as err:
        flash('Something Went Wrong. Try Again', 'danger')
        logging.error(f'error from slink occurred due to {err}')
    return render_template('main/slink.html')


@main_blueprint.route('/slink_it', methods=['POST'])
def slink_it():
    if not is_customer():
        cus_id = uuid.uuid4().hex
        CustomersController().create_user(cus_id=cus_id)
        session['cus_id'] = cus_id
    if is_registered_customer() or is_customer():
        long_link = request.form.get('long_link')
        if long_link:
            try:
                short_code = short_code_generator()

                # LinksController().create_slink(slink=short_code, long_link=long_link,
                #                                customer_id=session['cus_id'])
                # LinksController().set_long_link(slink_id=short_code, long_link=long_link)
                # flash('Slink Created', 'success')

                create_slink_background.delay(slink=short_code, long_link=long_link, customer_id=session['cus_id'])
                flash('Slink Creation Request Submit', 'success')
                
                return redirect(url_for('main.panel'))
            except Exception as err:
                flash('Something Went Wrong. Try Again', 'danger')
                logging.error(f'error from slink_it occurred due to {err}')
    else:
        flash('Please Retry', 'danger')
    return render_template('main/slink.html')


@main_blueprint.route('/panel')
def panel():
    if is_registered_customer() or is_customer():
        try:
            customer_id = session['cus_id']
            result = LinksController().show_slink(customer_id=customer_id)
            if not is_registered_customer():
                return render_template('main/panel.html', slink_data=result)
            customer_status = session['Registered']
            return render_template('main/panel.html', cus_status=customer_status, slink_data=result)
        except Exception as err:
            flash('Something Went Wrong. Try Again', 'danger')
            logging.error(f'error from panel occurred due to {err}')
    return redirect(url_for('main.slink'))




