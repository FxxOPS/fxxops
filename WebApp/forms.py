# -*- coding: utf-8 -*-
'''
Created on 2014.04.29

@author: yuan.gao6
'''

from wtforms import Form, TextField, PasswordField, validators

'''
classdocs
'''
class LoginForm(Form):
    strUser = TextField('user', [validators.Required()])
    strPassword = PasswordField('password', [validators.Required()])

class PasswordForm(Form):
    strPassword = PasswordField('password', [validators.Required(), validators.EqualTo('strConfirm', message = 'Passwords must match')])
    strConfirm = PasswordField('repeat password')
