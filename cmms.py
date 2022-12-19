# -*- coding: utf-8 -*-
################################################################################
#
# Computerized maintenance management system (CMMS) module,
# Copyright (C) 
#    2015 - Ait-Mlouk Addi , (http://www.aitmlouk.info/)-- aitmlouk@gmail.com --
#    
# CMMS module is free software: you can redistribute
# it and/or modify it under the terms of the Affero GNU General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# CMMS module is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Affero GNU
# General Public License for more details.
#
# You should have received a copy of the Affero GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from openerp.osv import fields, osv, orm
import datetime
from dateutil.relativedelta import *
import time


class cmms_fabriquant(osv.osv):
    _name = 'cmms.fabriquant'
    _description = 'fabriquant '


    _columns = {
        'name': fields.char('fabriquant', size=64, required=True),
 
    }
	
cmms_fabriquant()


# class cmms_categorie(osv.osv):
    # _name = 'cmms.categorie'
    # _description = 'categorie '


    # _columns = {
        # 'name': fields.char('categorie', size=64, required=True),
 
    # }
	
# cmms_categorie()
	
class cmms_line(osv.osv):
    _name = 'cmms.line'
    _description = 'Production line'
    _inherit = ['mail.thread','ir.needaction_mixin']
	
    def create(self, cr, user, vals, context=None):
	if ('s' not in vals) or (vals.get('s')=='/'):
		vals['s'] = self.pool.get('ir.sequence').get(cr, user, 'cmms.line')
		
	return super(cmms_line, self).create(cr, user, vals, context)
	
    _columns = {
        'name': fields.char('Production line', size=64, required=True),
        'code': fields.char('Line reference', size=64, required=True),
        'location': fields.char('Location', size=64),
        'sequence': fields.integer('Sequence'),
        's': fields.char('Line', size=64,readonly=True),
    }

    _defaults = {
	 
		's': lambda self, cr, uid, context: '/',
    }
	
    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default = default.copy()
        default['s'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.line')
        return super(cmms_line, self).copy(cr, uid, id, default=default, context=context)



cmms_line()

class cmms_table(osv.osv):
    _name = 'cmms.table'
    _description = 'Table Temporaire'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _columns = {
        'line_id_periodicite': fields.many2one('cmms.line','Production line'),
        'affectation': fields.selection([('a_Errahali','a.Errahali'),('l_Chamouti','l.Chamouti'),(' m_Belkarime',' m.Belkarime'),('m_Elghour','m.Elghour'),('n_Arrabhy','n.Arrabhy')],'Affectation', size=32),
        # user2_id=fields.Many2one('res.users', 'Intervenant',required=True)
        'affectation_user': fields.many2one('res.users','Affectation ', required=True, change_default=True),
        'date': fields.datetime('Date', default= lambda self:fields.datetime.now()),
		'meters': fields.selection([('days', 'Days'),
                                   ('h', 'Hebdomadaire'),
                                   ('m', 'mensuel'),
                                   ('t', 'Trimestriel'),
                                   ('s', 'semestriel'),
                                   ('a', 'Annuel'),
                                   ('2ans', '2ans'),
                                   ('5ans', '5ans')], 'Unite de Mesure'),

    }


cmms_table()


 



class cmms_equipment(osv.osv):
    _name = "cmms.equipment"
    _description = "equipment"
    _inherit = ['mail.thread','ir.needaction_mixin']
    
    def create(self, cr, user, vals, context=None):
        if ('type' not in vals) or (vals.get('type')=='/'):
            vals['type'] = self.pool.get('ir.sequence').get(cr, user, 'cmms.equipment')
        return super(cmms_equipment, self).create(cr, user, vals, context)
    
    def _count_all(self, cr, uid, ids, field_name, arg, context=None):
        Logintervention = self.pool['cmms.intervention']
        Logpm = self.pool['cmms.pm']
        Logcm = self.pool['cmms.cm']
        Logorder = self.pool['cmms.incident']
        return {
            equipment_id: {
                'pm_count': Logpm.search_count(cr, uid, [('equipment_id', '=', equipment_id)], context=context),
                'cm_count': Logcm.search_count(cr, uid, [('equipment_id', '=', equipment_id)], context=context),
                'order_count': Logorder.search_count(cr, uid, [('equipment_id', '=', equipment_id)], context=context),
                'intervention_count': Logintervention.search_count(cr, uid, [('equipment_id', '=', equipment_id)], context=context)               
            }
            for equipment_id in ids
        }
    
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current machine """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'cmms', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_equipment_id': ids[0]})
            res['domain'] = [('equipment_id','=', ids[0])]
            return res
        return False
    

    _columns = {
        'type': fields.char('Unit of work reference', size=64,readonly=False),
        'name': fields.char('Name', size=64 , required=True),
        'trademark': fields.char('Trademark', size=64),
        'active' : fields.boolean('Active'),
        'local_id': fields.many2one('stock.location', 'Location'),
        'line_id': fields.many2one('cmms.line','Production line', required=True, change_default=True),
        'invoice_id': fields.many2one('account.invoice', 'Purchase invoice'),
        'startingdate': fields.datetime("Starting date"),
        'product_ids': fields.many2many('product.product','product_equipment_rel','product_id','equipment_id','Organes'),
        'deadlinegar': fields.datetime("Deadline of guarantee"),
        'description': fields.text('Unit of work reference'),
        'safety': fields.text('Safety instruction'),
        'intervention_id': fields.one2many('cmms.intervention','equipment_id', 'Interventions'),
        'cm_id': fields.one2many('cmms.cm','equipment_id', 'Maintenance Corrective '),
        'pm_id': fields.one2many('cmms.pm','equipment_id', 'Maintenance Preventive'),
        'incident_id': fields.one2many('cmms.incident','equipment_id', 'OT'),
        'user_id': fields.many2one('res.users', 'Manager'),
        'photo': fields.binary('Photo'),
        'intervention_count': fields.function(_count_all, type='integer', string='Intervention', multi=True),
        'pm_count': fields.function(_count_all, type='integer', string='Preventive maintenance', multi=True),
        'cm_count': fields.function(_count_all, type='integer', string='Corrective maintenance', multi=True),
        'order_count': fields.function(_count_all, type='integer', string='Work Order', multi=True),
		
    }
    _defaults = {
        'active' : lambda *a: True,
        'user_id': lambda object,cr,uid,context: uid,
        'type': lambda self, cr, uid, context: '/',
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default = default.copy()
        default['type'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.equipment')
        return super(cmms_equipment, self).copy(cr, uid, id, default=default, context=context)
    
cmms_equipment()


class cmms_intervention(osv.osv):
    _name = "cmms.intervention"
    _description = "Intervention request"
    _inherit = ['mail.thread','ir.needaction_mixin']

    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'cmms.intervention')
        return super(cmms_intervention, self).create(cr, user, vals, context)
    
    def action_done(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'done'})
    
    def action_cancel(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'cancel'})
    
    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'draft'})

    _columns = {
        'name': fields.char('Intervention reference', size=64,readonly=True),
        'equipment_id': fields.many2one('cmms.equipment', 'Unit of work', required=True),
        'date': fields.datetime('Date'),
        'user_id': fields.many2one('res.users', 'Sender', readonly=True),
        # 'user2_id': fields.many2one('res.users', 'Recipient'),
		# 'resp': fields.selection([('Samih','f.Samyh'),('mahjoubi','m.Mahjoubi')],'Responsable', size=32),
        'priority': fields.selection([('normal','Normal'),('low','Low'),('urgent','Urgent'),('other','Other')],'priority', size=32),
        'priorite': fields.selection([('normal','Normal'),('basse','Basse'),('urgent','Urgent')],'priorité', size=32, required=True),
        'observation': fields.text('Observation'),
        'motif': fields.text('Motif'),
        'date_inter_c': fields.datetime('Date Souhaitée', required=True),
        'date_end_c': fields.datetime('Date Actuelle ', required=True),
        'type': fields.selection([('check','Check'),('repair','Repair'),('revision','Revision'),('other','Other')],'Intervention type', size=32),
        'state_machine': fields.selection([('start','En Marche'),('stop','En Arret'),('degrader','Dégrader')],'Etat de machine', size=32),
        'state' : fields.selection([('draft',u'En cours'),('done',u'Validé'),('cancel',u'Annulé')],u'Statut',required=True),
    }
    _defaults = {
        'state': lambda *a: 'draft',
        'type': lambda * a:'repair',
        'priority': lambda * a:'normal',
        'user_id': lambda object,cr,uid,context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'name': lambda self, cr, uid, context: '/',
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if not context:
            context = {}
        if default is None:
            default = {}
            default = default.copy()
            default['name'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.intervention')
        return super(cmms_intervention, self).copy(cr, uid, id, default=default, context=context)
    
    """email"""
    def action_broadcast(self,cr,uid,ids,context={}):
        data_email = []
        text_inter = u"""<div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: rgb(255, 255, 255); ">
                <p>Bonjour %s, </p>
                <p>Nous vous informons que vous êtes attribué a l'intervention %s de l'émetteur  %s.</p>
                <br/>
                <p></p>
                <p>-----------------------------</p>
                <p>Référence intervention  : %s </p>
                <p>Type d'intervention : %s </p>
                <p>Machine : %s </p>
                <p>Date du debut : %s </p>
                <p>Date de fin d'intervention : %s </p>
                <p>Priorité  : %s </p>
                <p>Etat de machine  : %s </p>
                <p>Motif d'intervention  : %s </p>
                <p>------------------------------</p>
                <p> Service du Gmao</p>
                </div>
                """
        for object_inter in self.browse(cr,uid,ids):
            if not object_inter.user2_id.login:
                raise osv.except_osv(u'Email non spécifiée', u'Veuillez indiquer l\'email de Destinataire')
            if object_inter.user2_id.login:
                    text_inter = text_inter %(
                                                       object_inter.user2_id.name,
                                                       object_inter.name,object_inter.user_id.name,
                                                       object_inter.name,
                                                       object_inter.type,
                                                       object_inter.equipment_id.name,
                                                       object_inter.date_inter,
                                                       object_inter.date_end,
                                                       object_inter.priority,
                                                       object_inter.state_machine,
                                                       object_inter.motif,
                                                      
                                                       )
                    data_email.append(
                                {
                                'subject' : "Service du Gmao %s" %object_inter.name,
                                'email_to' : object_inter.user2_id.name,
                                'subtype' : 'html',
                                'body_text' : False,
                                'body_html' : text_inter,
                                }
                            )
                                   
        self.pool.get('cmms.parameter.mail').send_email(cr,uid,data_email,module='cmms',param='cmms_event_mail')      
        
"""fin"""


cmms_intervention()

AVAILABLE_PRIORITIES = [
    ('3','Normal'),
    ('2','Low'),
    ('1','High')
]

class cmms_request_link(osv.osv):
    _name = 'cmms.request.link'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'object': fields.char('Object', size=64, required=True),
        'priority': fields.integer('Priority'),
    }
    _defaults = {
        'priority': lambda *a: 5,
    }
    _order = 'priority'

cmms_request_link()

class cmms_incident(osv.osv):
    _name = "cmms.incident"
    _order = "name desc"
    _description = "Incident" 
    _inherit = ['mail.thread','ir.needaction_mixin']
    
    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'cmms.incident')
        return super(cmms_incident, self).create(cr, user, vals, context)

    def _links_get(self, cr, uid, context={}):
        obj = self.pool.get('cmms.request.link')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['object', 'name'], context)
        return [(r['object'], r['name']) for r in res]
    
    def action_done(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'done'})
    
    def action_cancel(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'cancel'})
    
    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'draft'})

    _columns = {
        'name':fields.char('Work order reference',size=64,readonly=True),
        'observation':fields.text('Observation'),
        'state' : fields.selection([('draft',u'En cours'),('done',u'Validé'),('cancel',u'Annulé')],u'Statut',required=True),
        'statut' : fields.selection([('draft',u'En cours'),('done',u'Lancer'),('cancel',u'Cloturer')],u'Statut'),
        'priority': fields.selection(AVAILABLE_PRIORITIES, 'Priority'),
		'priorite_incident': fields.selection([('normal','Normal'),('basse','Basse'),('urgent','Urgent')],'priorité', size=32,readonly=True),
        'user_id': fields.many2one('res.users', 'Emetteur', readonly=True),
		# 'user2_id': fields.many2one('res.users', 'Emetteur'),
		# 'resp': fields.selection([('Samih','f.Samyh'),('mahjoubi','m.Mahjoubi')],'Responsable', size=32),
        'date': fields.date('Work order date',readonly=True,required=True),
        'active' : fields.boolean('Active?'),
        'ref' : fields.reference('Work order source', selection=_links_get, size=128),
        'equipment_id': fields.many2one('cmms.equipment', 'Unit of work',readonly=True),
        'archiving3_ids': fields.one2many('cmms.archiving3', 'incident_id', 'follow-up history'),
		# 'ot_idp_incident_mc2': fields.many2one('cmms.incident', 'MC'),
    }
    _defaults = {
        'active': lambda * a:True,
        'name': lambda self, cr, uid, context: '/',
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'priority': lambda *a: AVAILABLE_PRIORITIES[2][0],
        'user_id': lambda object,cr,uid,context: uid,
        'state': lambda * a:'draft',
        'statut': lambda * a:'draft',
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if not context:
            context = {}
        if default is None:
            default = {}
        default = default.copy()
        default['name'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.incident')
        return super(cmms_incident, self).copy(cr, uid, id, default=default, context=context)

cmms_incident()

class cmms_archiving3(osv.osv):
    _name = "cmms.archiving3"
    _description = "Incident follow-up history"
    _columns = {
        'name': fields.char('Objet', size=32, required=True),
        'date': fields.datetime('Date'),
        'description': fields.text('Description'),
        'incident_id': fields.many2one('cmms.incident', 'Incident',required=True),
        'user_id': fields.many2one('res.users', 'Manager', readonly=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': lambda object,cr,uid,context: uid,
    }

cmms_archiving3()


class cmms_pm(osv.osv):
    _name = "cmms.pm"
    _description = "Preventive Maintenance System"
    _inherit = ['mail.thread','ir.needaction_mixin']
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context):
        res = self.name_get(cr, uid, ids, context)
        return dict(res)
    
    def _days_next_due(self, cr, uid, ids, prop, unknow_none, context):
        if ids:
            reads = self.browse(cr, uid, ids, context)
            res = []
            for record in reads:
                if (record.meter == "days"):
                    interval = datetime.timedelta(days=record.days_interval)
                    last_done = record.days_last_done 
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval   
                    res.append((record.id, next_due.strftime("%Y-%m-%d")))
                elif (record.meter == "h"):
                    interval = datetime.timedelta(days=7)          
                    last_done = record.days_last_done
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    res.append((record.id, next_due.strftime("%Y-%m-%d")))
                elif (record.meter == "m"):
                    interval = datetime.timedelta(days=30)
                    last_done = record.days_last_done
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    res.append((record.id, next_due.strftime("%Y-%m-%d")))
                elif (record.meter == "t"):
                    interval = datetime.timedelta(days=91)
                    last_done = record.days_last_done
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    res.append((record.id, next_due.strftime("%Y-%m-%d")))
                elif (record.meter == "s"):
                    interval = datetime.timedelta(days=182)
                    last_done = record.days_last_done
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    res.append((record.id, next_due.strftime("%Y-%m-%d")))
                elif (record.meter == "a"):
                    interval = datetime.timedelta(days=365)
                    last_done = record.days_last_done
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval
                    res.append((record.id, next_due.strftime("%Y-%m-%d")))
        
                else:
                    res.append((record.id, False))
					
            return dict(res)
    
    def _days_due(self, cr, uid, ids, prop, unknow_none, context):
        if ids:
            reads = self.browse(cr, uid, ids, context)
            res = []
            for record in reads:
                if (record.meter == "days"):
					
                    interval = datetime.timedelta(days=record.days_interval)
                    last_done = record.days_last_done
                    last_done = datetime.datetime.fromtimestamp(time.mktime(time.strptime(last_done, "%Y-%m-%d")))
                    next_due = last_done + interval  
                    NOW = datetime.datetime.now()
                    due_days = next_due - NOW 
                    res.append((record.id, due_days.days))
 

                else:
                    res.append((record.id, False))
            return dict(res)

    def _get_state(self, cr, uid, ids, prop, unknow_none, context):
        res = {}
        if ids:
            reads = self.browse(cr, uid, ids, context)
            for record in reads:    
                if record.meter == u'days':
                    if record.days_left <= 0:
                        res[record.id] = u'Dépassé'
                    elif record.days_left <= record.days_warn_period:
                        res[record.id] = u'Approché'
                    else:
                        res[record.id] = u'OK'
            return res															

    def create(self, cr, user, vals, context=None):
        vals['version'] =  0
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'cmms.pm')
        return super(cmms_pm, self).create(cr, user, vals, context)
    
    _columns = {
        'name':fields.char('Ref PM',size=20, readonly=True),
        'equipment_id': fields.many2one('cmms.equipment', 'Unit of work', required=True),
        'meter':fields.selection([ ('days', 'Days'),('h', 'Hebdomadaire'),('m', 'mensuel'),('t', 'Trimestriel'),('s', 'semestriel'),('a', 'Annuel'),('2ans', '2ans'),('5ans', '5ans')], 'Unit of measure',readonly=False),
        'recurrent':fields.boolean('Recurrent ?', help="Mark this option if PM is periodic"),
        'days_interval':fields.integer('Interval', readonly=True), 
        'days_last_done':fields.date('Begun the',required=True ,readonly=True),
        'days_next_due':fields.function(_days_next_due, method=True, type="datetime", string='Next date'),
        'days_next_due2':fields.datetime( string='Prochaine Date',required=True , readonly=False),
        'days_warn_period':fields.integer('Warning date'),
        'user_id': fields.many2one('res.users', 'Chef'),
        'days_left':fields.function(_days_due, method=True, type="integer", string='Staying days'),
        'state':fields.function(_get_state, method=True, type="char", string='Status')
    }
    _defaults = {
        'meter': lambda * a: 'days',
        'recurrent': lambda * a: True,
        'days_last_done': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'name': lambda self, cr, uid, context: '/',
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
            default = default.copy()
            default['name'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.pm')
        return super(cmms_pm, self).copy(cr, uid, id, default=default, context=context)
cmms_pm()

class cmms_archiving2(osv.osv):
    _name = "cmms.archiving2"
    _description = "PM follow-up history"
    _columns = {
        'name': fields.char('effect', size=32, required=True),
        'date': fields.datetime('Date'),
        'description': fields.text('Description'),
        'pm_id': fields.many2one('cmms.pm', 'Archiving',required=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

cmms_archiving2()

CHOICE = [
    ('yes','Yes'),
    ('no','No'),
]

class cmms_checklist(osv.osv):
    _name="cmms.checklist"
    _description= "checklist"
    _columns={
        'name': fields.char("Title",size=128, required=True),
        'description': fields.text('Description'), 
        'questions_ids': fields.one2many("cmms.question","checklist_id","Questions",),
        'equipment_id': fields.many2one('cmms.equipment', 'Equipment'),
        }
cmms_checklist()

class cmms_question(osv.osv):
    _name = "cmms.question"
    _description = "Question"
    _columns = {
        'name': fields.char("Question",size=128, required=True),
        'checklist_id': fields.many2one('cmms.checklist', 'Checklist', required=True), 
    }
cmms_question()

class cmms_checklist_history(osv.osv):
    _name="cmms.checklist.history"
    _description= "Checklist History"
    _inherit = ['mail.thread','ir.needaction_mixin']
    
    def onchange_checklist_id(self, cr, uid, ids, id, context={}):
        liste = self.pool.get('cmms.question').search(cr, uid, [('checklist_id', '=', id)])
        enrs = self.pool.get('cmms.question').name_get(cr, uid, liste)
        res = []
        for id, name in enrs:
            obj = {'name': name}
            res.append(obj)
        return {'value':{'answers_ids': res}}
    
    def create(self, cr, uid, vals, context=None):
        for i, obj in enumerate(vals['answers_ids']):
            vals['answers_ids'][i] = [0,0,vals['answers_ids'][i][2]]
        return osv.osv.create(self, cr, uid, vals, context=context)
    
    def action_done(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'done'})
    
    def action_confirmed(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'confirmed'})
    
    def action_draft(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'draft'})
    
    _columns={
        'name': fields.char("Checklist name",size=128, required=True),
        'checklist_id': fields.many2one('cmms.checklist', 'Checklist'), 
        'answers_ids': fields.one2many("cmms.answer.history","checklist_history_id","Responses"),
        'date_planned': fields.datetime("Planned date"), 
        'date_end': fields.datetime("End date"), 
        'equipment_id': fields.many2one('cmms.equipment', 'Unit of work'),
        'user_id': fields.many2one('res.users', 'Manager'),
        'state': fields.selection([('draft', 'Brouillon'), ('confirmed', 'Confirmé'),('done', 'Validé')], "Status"),
        }
    _defaults = {
        'state' : lambda *a: 'draft',
        'user_id': lambda object,cr,uid,context: uid,
    }
    
cmms_checklist_history()

class cmms_question_history(osv.osv):
    _name="cmms.answer.history"
    _description= "Answers"
    _columns={    
        'name': fields.char("Question",size=128, required=True),
        'checklist_history_id': fields.many2one('cmms.checklist.history', 'Checklist'),
        'etat': fields.selection([('mep','MEP'), ('ahp','AHT')],'Etat'),
        'profil': fields.selection([('mec','MEC'), ('elec','ELEC')],'Profil'),
        'pdr': fields.char("PDR",size=128),
        'consommables': fields.char("Consommables",size=128),
		'outillage': fields.char("Outillage",size=128),
        'etat_reference': fields.char("Etat Ref",size=128),
        'etat_ref': fields.float("Etat Ref min"),
        'etat_ref_max': fields.float("Etat Ref max"),
		'unite': fields.selection([('a','A'), ('mm','mm'),('v','V'), ('l','L'), ('c','C'), ('bar','BAR')],'Unite'),
        'mesure': fields.float("mesure"),
		'action': fields.integer("action",size=128),
		'duree': fields.float("Durée Prevue",size=128),
		'duree_realiser': fields.float("Durée Realiser",size=128),
		'statut_ok': fields.selection([('ok','OK'), ('nonok','NON OK')],'Statut'), 
		# 'ref_mc': fields.char("MC",size=1280),
		# 'ref_mc': fields.many2one('cmms.incident', 'Incident',required=True),
		'ot_idp_incident_mc': fields.many2one('cmms.incident', 'MC'),
		# 'user2_id': fields.many2one('res.users', 'Intervenant'),
		# ot_idp_incident_mc= fields.Many2one('cmms.incident', 'MC')
		'observation': fields.char("Observation",size=1280),   
		'Date_realisation': fields.datetime("Date realisation",size=1280),
    }
    
cmms_question_history()

class cmms_failure(osv.osv):
    _name = "cmms.failure"
    _description = "failure cause"
    _columns = {
        'name': fields.char('Type of failure', size=32, required=True),
        'code': fields.char('Code', size=32),
        'description': fields.text('failure description'),
    }

cmms_failure()

class cmms_cm(osv.osv):
    _name = "cmms.cm"
    _description = "Corrective Maintenance System"
    _inherit = ['mail.thread','ir.needaction_mixin']

    _columns = {
        'name': fields.char('CM reference',size=20,readonly=True),
        'equipment_id': fields.many2one('cmms.equipment', 'Unit of work', required=True),
        'failure_id': fields.many2one('cmms.failure', 'Failure?', required=True),
        'date': fields.datetime('Date',required=True,readonly=True),
        'note': fields.text('Notes'),
		'priorite_mc': fields.selection([('normal','Normal'),('basse','Basse'),('urgent','Urgent')],'priorité', size=32, required=True),
        'user_id': fields.many2one('res.users', 'Emetteur',readonly=True),
		# 'user2_id': fields.many2one('res.users', 'Emetteur'),
		# 'resp': fields.selection([('Samih','f.Samyh'),('mahjoubi','m.Mahjoubi')],'Responsable', size=32,readonly=True),
        'diagnosistab_ids': fields.one2many('cmms.diagnosistab', 'cm_id', 'Diagnosis Table'),
        'description_panne_cm' : fields.text('Description de panne', required=True),
    }
    _defaults = {
        'name': lambda self, cr, uid, context: '/',
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': lambda object,cr,uid,context: uid,
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        #netsvc.Logger().notifyChannel("[HNM]["+__name__+"][create]", netsvc.LOG_DEBUG,"vals:%s" % (vals,))
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.cm')
        return super(cmms_cm, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default = default.copy()
        default['name'] = self.pool.get('ir.sequence').get(cr, uid, 'cmms.cm')
        return super(cmms_cm, self).copy(cr, uid, id, default=default, context=context)

cmms_cm()

class cmms_diagnosistab(osv.osv):
    _name = "cmms.diagnosistab"
    _description = "Diagnosis List"
    _columns = {
        'symptome': fields.text('symptôme', required=True),
        'name': fields.text('Failure causes', required=True),
        'remede': fields.text('Remede'),
        'verrouillage': fields.text('Verrouillage'),
        'solution': fields.text('Solution', required=True),
        'Duree': fields.float('Duree', required=True),
        'Observation': fields.text('Observation'),
        'Date_realisation': fields.datetime('Date realisation', required=True),
        # 'user2_id': fields.many2one('res.users', 'Intervenant', required=True),
        'cm_id': fields.many2one('cmms.cm', 'Corrective Maintenance'),
    }

cmms_diagnosistab()


# class cmms_TableTemLines(osv.osv):
    # _name = "cmms.table.lines" 
    # _description = "table lines"
    # _columns = {
        # 'name': fields.char(),
		# 'meter': fields.selection([('days', 'Days'),
						   # ('h', 'Hebdomadaire'),
						   # ('m', 'mensuel'),
						   # ('t', 'Trimestriel'),
						   # ('s', 'semestriel'),
						   # ('a', 'Annuel')], 'Unit of measure'),
        # 'days_next_due2': fields.datetime('days_next_due2'),
        # 'equipment_id': fields.many2one('cmms.equipment', 'machine'),
        # 's': fields.many2one('cmms.sous.equipment.type', 'sous machine'),
        # 'recurrent':fields.boolean('Recurrent ?', help="Mark this option if PM is periodic"),
		
		
 
    # }

# cmms_TableTemLines()
 

class cmms_archiving(osv.osv):
    _name = "cmms.archiving"
    _description = "CM follow-up History"
    _columns = {
        'name': fields.char('effect', size=32, required=True),
        'date': fields.datetime('Date'),
        'description': fields.text('Description'),
	
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

class cmms_panier(osv.osv):
    _name = "cmms.panier"

class cmms_version(osv.osv):
	_name='cmms.version'

 
