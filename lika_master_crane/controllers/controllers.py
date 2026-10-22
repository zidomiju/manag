# from odoo import http


# class LikaMasterCrane(http.Controller):
#     @http.route('/lika_master_crane/lika_master_crane', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lika_master_crane/lika_master_crane/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lika_master_crane.listing', {
#             'root': '/lika_master_crane/lika_master_crane',
#             'objects': http.request.env['lika_master_crane.lika_master_crane'].search([]),
#         })

#     @http.route('/lika_master_crane/lika_master_crane/objects/<model("lika_master_crane.lika_master_crane"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lika_master_crane.object', {
#             'object': obj
#         })

