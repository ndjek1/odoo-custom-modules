from odoo import http
from odoo.http import request

class NationalIdApplicationController(http.Controller):

    @http.route('/website/form/national_id_application', type='http', auth="public", website=True, methods=['GET', 'POST'])
    def submit_national_id_application(self, **post):
        if request.httprequest.method == 'POST':
            picture = request.httprequest.files.get('picture')
            lc_reference_letter = request.httprequest.files.get('lc_reference_letter')

            # Ensure the files are being read as binary data
            picture_data = picture.read() if picture else False
            lc_reference_data = lc_reference_letter.read() if lc_reference_letter else False

            # Create the record with the uploaded files
            request.env['national.id.application'].sudo().create({
                'name': post.get('name'),
                'dob': post.get('dob'),
                'nationality': post.get('nationality'),
                'address': post.get('address'),
                'email': post.get('email'),
                'picture': picture_data,
                'lc_reference_letter': lc_reference_data,
                'approval_stage': 'draft',
            })
            return request.redirect('/contactus-thank-you')  # After submission redirect to a thank you page

        # If the request is GET, render the form
        return request.render('national_id_application.national_id_application_form')
