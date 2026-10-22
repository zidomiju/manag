# from odoo import http


# class LikaCustomer(http.Controller):
#     @http.route('/lika_customer/lika_customer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_customer/lika_customer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_customer.listing', {
#             'root': '/lika_customer/lika_customer',
#             'objects': http.request.env['lika_customer.lika_customer'].search([]),
#         })

#     @http.route('/lika_customer/lika_customer/objects/<model("lika_customer.lika_customer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_customer.object', {
#             'object': obj
#         })

