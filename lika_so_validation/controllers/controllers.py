# from odoo import http


# class LikaSoValidation(http.Controller):
#     @http.route('/lika_so_validation/lika_so_validation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_so_validation/lika_so_validation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_so_validation.listing', {
#             'root': '/lika_so_validation/lika_so_validation',
#             'objects': http.request.env['lika_so_validation.lika_so_validation'].search([]),
#         })

#     @http.route('/lika_so_validation/lika_so_validation/objects/<model("lika_so_validation.lika_so_validation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_so_validation.object', {
#             'object': obj
#         })

