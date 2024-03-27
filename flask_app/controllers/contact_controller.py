from flask import request, render_template, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.contact import Contact

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        contact_data = {
             **request.form,
            "sender_id": session["user_id"],
        }
        Contact.create(contact_data)
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    else:
        return render_template('contact.html')
    

@app.route('/contact/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = Contact.get_by_id(contact_id)
    if request.method == 'POST':
        updated_data = {
            'id': contact_id,
            'name': request.form['name'],
            'email': request.form['email'],
            'message': request.form['message']
        }
        contact.update(updated_data)
        flash('Contact information updated successfully!', 'success')
        return redirect(url_for('contact'))
    else:
        return render_template('edit_contact.html', contact=contact)

@app.route('/contact/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    Contact.delete(contact_id)
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('contact'))



