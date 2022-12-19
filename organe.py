# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

from dateutil.relativedelta import *
import time
from datetime import timedelta 
from openerp.exceptions import Warning
import datetime 
 

class organe(models.Model):
	_name = 'cmms.organe'
	_rec_name = 'description'
    
	
	description =fields.Text()
	item_no_= fields.Char()
	quantite= fields.Float()






