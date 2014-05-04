#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import foursquare
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template,request,jsonify,json
from flask.ext.bootstrap import Bootstrap
import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__,template_folder=tmpl_dir)
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/breakme/')
def breakme():
    return render_template('noformserror.html')


@app.route('/social_login')
def social_login():
	return render_template('home.html')

@app.route('/process/<access_token>')
def start_calculation(access_token):
	client = foursquare.Foursquare(client_id='OIHK2AIH43GOZWFR4EHQRQV3QEXJWZSUBPJ2WADXFBINMRWC', client_secret='VQPEDXH2DD2RM4J1D4Y4W03NEFABOQTUWKE5ZZDXSFZPPFHR', redirect_uri='http://127.0.0.1:5000/social_login')
	client.set_access_token(access_token)
	response = client.users.friends()
	app.logger.info(response.checksum)
	# checkins = []
	# for friend in response.friends.items:
	# 	app.logger.info(friend)
	# 	client.users(friend.id)
	# 	friend_checkins = client.users.all_checkins()
	# 	checkings += friend_checkins
	# 	app.logger.info(friend_checkins)
	# 	app.logger.info(checkings)
	return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
