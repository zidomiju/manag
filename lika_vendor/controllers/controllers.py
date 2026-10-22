# from odoo import http


# class LikaVendor(http.Controller):
#     @http.route('/lika_vendor/lika_vendor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_vendor/lika_vendor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_vendor.listing', {
#             'root': '/lika_vendor/lika_vendor',
#             'objects': http.request.env['lika_vendor.lika_vendor'].search([]),
#         })

#     @http.route('/lika_vendor/lika_vendor/objects/<model("lika_vendor.lika_vendor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_vendor.object', {
#             'object': obj
#         })

