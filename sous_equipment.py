# -*- coding: utf-8 -*-


from openerp import models, fields, api, _

from dateutil.relativedelta import *
import time
from datetime import timedelta 
from openerp.exceptions import Warning
import datetime 
 
from openerp import tools

class CmmsEquipemt(models.Model):
    _inherit = 'cmms.equipment'
    # _rec_name= 'ref'
    sous_equipement_type_id = fields.Many2one('cmms.sous.equipment.type')
    # type_id = fields.Many2one(related='sous_equipement_id.type_id', string='Type')
    # product_ids = fields.Many2many(related='sous_equipement_id.product_ids', string='Pieces of change')
    sous_equipement_type_ids = fields.Many2many('cmms.sous.equipment.type',
                                                'sous_equipment_type_equipment_rel',
                                                'sous_equipement_type_id',
                                                'equipment_id')
    product_ids = fields.Many2many('product.template', 'product_sous_equipment_type_rel', 'product_id', 'sous_equipment_type_id',
                                   'Organes')

# ajout code par Reda
class Product(models.Model):
    _inherit = 'product.template'
	#sequence
    # def create(self, cr, user, vals, context=None):
	# if ('Ref_Organe' not in vals) or (vals.get('Ref_Organe')=='/'):
		# vals['Ref_Organe'] = self.pool.get('ir.sequence').get(cr, user, 'product.product')
	# return super(Product, self).create(cr, user, vals, context)
	###
	
	
    # designation = fields.Char(string='designation')
    # sous_equipment_type_id = fields.Many2one('cmms.sous.equipment.type')
    interchabilite = fields.Selection([('non','Non') , ('oui','OUI')],'Interchabilite')
    ou = fields.Char(string="ou")
    a_gerer = fields.Selection([('non','Non') , ('oui','OUI')],'A Gerer')
    stock_securite = fields.Integer(string="Stock securite")
    stock_min = fields.Integer(string="Stock min")
    stock_max = fields.Integer(string="Stock max")
    consommation_moyenne = fields.Integer(string="Consommation moyenne")
    magasin = fields.Char(string="Magasin")
    famille = fields.Selection([('PDR/CONSO','PDR/CONSO')],'Famille')
    affectation = fields.Char(string="Affectation ")
    emplacement = fields.Char(string="Emplacement ")
    unit = fields.Selection([('kgs','KGS'), ('lettre','Lettre'), ('pce','PCE'), ('pcs','PCS')],'Unit')
    # type_article = fields.Selection([('m','M'), ('p','P')],'Type Article')
    designation = fields.Char(string="Designation")
    # Ref_Organe = fields.Char(string="Reference Organe",compute="compute_ref_organe")
    Ref_Organe = fields.Char(string="Reference Organe")
    sous_equipment_ids = fields.Many2many('cmms.sous.equipment.type', 'product_sous_equipment_type_rel', 'sous_equipment_type_id', 'product_id',
                                   'Sous Equipements')
    equipment_id = fields.Many2one('cmms.equipment', 'Equipement')
    fabriquant = fields.Many2one('cmms.fabriquant', 'fabriquant')
    # categorie = fields.Many2one('cmms.categorie', 'categorie')
    categorie = fields.Char(string="Categorie")
	
    # @api.one
    # def compute_ref_organe(self):
		
		
			# if(self.id<10):
				# self.Ref_Organe = 'org-'  + '00'+ str(self.id)
			# elif(self.id>=10 and self.id<100 ):
				# self.Ref_Organe = 'org-' + '0' + str(self.id)
			# else:
				# self.Ref_Organe = 'org-' + '' + str(self.id)
	
	
	
	#sequence	
    # _defaults = {
	# 'Ref_Organe': lambda self, cr, uid, context: '/',
    # }
	
    # def copy(self, cr, uid, id, default=None, context=None):
        # if context is None:
            # context = {}
        # if default is None:
            # default = {}
        # default = default.copy()
        # default['Ref_Organe'] = self.pool.get('ir.sequence').get(cr, uid, 'product.product')
        # return super(CmmsSousEquipmentType, self).copy(cr, uid, id, default=default, context=context)
	###
		
		
	
# class CmmsSousEquipment(models.Model):
#     _name = 'cmms.sous.equipment'
#     _rec_name = 'designation'
#
#     designation = fields.Char()
#     type_id = fields.Many2one('cmms.sous.equipment.type')

# <tree default_order='date_expected, picking_id, sequence'>
class CmmsSousEquipmentType(models.Model):
    _name = "cmms.sous.equipment.type"
    _rec_name = 'designation'
    _order = "nbr_ligne_prod, nbr_equipment_s asc"  
    # _order="line_production,nbr_sous_equipment"



    # def _count_all1(self, cr, uid, ids, field_name, arg, context=None):  
        # Logintervention = self.pool['cmms.intervention']
 
        # return {
            # Sous_Equip: {
 
                # 'intervention_count1': Logintervention.search_count(self,cr,ids, uid, [('Sous_Equip', '=', Sous_Equip)], context=context)
                
            # }
            # for Sous_Equip in ids
        # }
    # @api.one			
    # @api.depends('cmms.equipment')    
    # def _count_all1(self):
		# for record in self:
			# self.pm_count1 = self.env['cmms.equipment'].search_count([('equipment_id', '=', 'equipment_id')])
			 
		# def _count_all1(self, cr, uid, ids, prop, unknow_none, context=None):
        # res = {}
        # for record in self.browse(cr, uid, ids, context=context):
            # res[record.id] = record.name
        # return res
    
    def return_action_to_open1(self, cr, uid, ids, context=None):
        """ Ceci ouvre la vue xml spécifiée dans xml_id pour le sous equipment en cours."""
        if context is None:
            context = {}
        if context.get('xml_id'):
			
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'cmms', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_Sous_Equip': ids[0]})
            res['domain'] = [('Sous_Equip','=', ids[0])]
            return res
        return False 
		
		
		
    # @api.depends('nbr_ligne_prod')
    # def nbr_ligne_produc(self):
		# if(self.line_production.sequence!=0):
			  
 
			# field_name = fields.Integer(string='Name', compute='_compute_anything')
			# self.nbr_ligne_prod = unicode(self.line_production.sequence)    
	
	
	# _columns = {
		# 'intervention_count1': fields.function(_count_all1, type='integer', string='Intervention', multi=True),
	# }
    

    def return_action_to_open1(self, cr, uid, ids, context=None):
        """ Ceci ouvre la vue xml spécifiée dans xml_id pour le sous equipment en cours."""
        if context is None:
            context = {}
        if context.get('xml_id'):
			
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'cmms', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_Sous_Equip': ids[0]})
            res['domain'] = [('Sous_Equip','=', ids[0])]
            return res
        return False 
		
		
		

    ot_count= fields.Integer(string='ot count',compute='ot_counte')
    intervention_count1= fields.Integer(string='Intervention', multi=True)
    pm_count1= fields.Integer(string='MP', multi=True)
    cm_count1= fields.Integer(string='MC', multi=True)
    order_count1= fields.Integer(string='OC', multi=True)
    Ref = fields.Char(compute='compute_refff')
    designation = fields.Char(string='Sous Equipement',required=True)
    type = fields.Selection([('fr','Fr')])
    product_id = fields.Many2one('product.template')
    equipment_id = fields.Many2one('cmms.equipment',required=True)
    sous = fields.Many2one('cmms.sous.equipment.type')
    product_ids = fields.Many2many('product.template', 'product_sous_equipment_type_rel', 'product_id', 'sous_equipment_type_id',
                                   'Organes')
    line_production=fields.Many2one('cmms.line',required=True)
    nbr_equipment_s= fields.Integer('Sequence Equipement',compute='nbr_equip',store=True,group_operator="min")
# groupby='name', orderby='name DESC'
    nbr_sous_equipment= fields.Integer('Sequence Sous Equipement')
    nbr_ligne_prod= fields.Integer('Sequence Ligne de Production',compute='nbr_ligne',store=True,group_operator="min")

    @api.multi
    def open_ot(self):
    
       return {

                'name': _("ot_test"),
                
                'domain': [('Sous_Equip','=',self.id)],

                'type': 'ir.actions.act_window',

                'res_model': 'cmms.incident', 

                'view_mode': 'tree,form',

                'view_type': 'form',

                'target': 'current',

            }
             
    @api.one
    def ot_counte(self):
        for rec in self:
            ot_count = self.env['cmms.incident'].search_count([('Sous_Equip' ,'=', rec.id)])
            rec.ot_count = ot_count

            
    @api.one
    def compute_refff(self):
		
		for record in self:
			if(self.id<10):
				self.Ref = unicode(record.equipment_id.ref) + '00' + str(record.id)
			elif(self.id>=10 and self.id<100 ):
				self.Ref = unicode(record.equipment_id.ref) + '0' + str(record.id)
			else:
				self.Ref = unicode(record.equipment_id.ref) + '' + str(record.id) 
				
    @api.one			
    @api.depends('equipment_id')
    def nbr_equip(self):
		
		for record in self:
			
			self.nbr_equipment_s = unicode(int(record.equipment_id.nbr_equipment))
	
    @api.one			
    @api.depends('line_production.sequence')
    def nbr_ligne(self):
		
		for record in self:
			
			self.nbr_ligne_prod = unicode(int(record.line_production.sequence))	
 
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
		# if 'nbr_ligne_prod' in fields:
		# fields.remove('line_production')
		# fields.remove('nbr_ligne_prod')
		# fields.remove('nbr_equipment_s')
		# fields.remove('nbr_sous_equipment')
            
		# if 'nbr_ligne_prod' in groupby:

		# orderby = 'nbr_ligne_prod DESC'+ (orderby and (',' + orderby) or '')
		# orderby = 'nbr_ligne_prod Asc'+ (orderby and (',' + orderby) or '')
		orderby = 'nbr_equipment_s Asc'+ (orderby and (',' + orderby) or '')
		
		return super(CmmsSousEquipmentType, self).read_group( domain, fields, groupby, offset=0, limit=limit, orderby=orderby, lazy=lazy)
		# for line in self:
			# equipment_id = self.env['cmms.equipment_id'].browse(self.nbr_equipment)
			# self.nbr_equipment_s =self.equipment_id.nbr_equipment 
			# line.nbr_equipment_s =self.equipment_id.nbr_equipment 
		
		
		   # for partner in self:
        # user_company = self.env['res.company'].browse(self.company_id)
        #NOTE: replace code name with your real field name where you want to see value 
        # partner.code = user_company.partner_id 
		
	
			# self.nbr_equipment_s = unicode(record.equipment_id.nbr_equipment)
		
		# obj_ids = self.env['cmms.equipment_id'].search([('equipment_id', '=', self.id)])
		# obj_ids = self.env['cmms.equipment_id'].browse(self.id)
		 
		# for obj in obj_ids:
			 
			# self.nbr_equipment_s =obj.equipment_id.nbr_equipment			
 
