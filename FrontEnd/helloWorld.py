#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 19:22:59 2021

@author: nathanyoung
"""

from flask import Flask, redirect, url_for, request, render_template, session
from markupsafe import escape
#import import_ipynb
import flaskPlay
import json


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        session['weights'] = list(request.form)[0]
        return (redirect(url_for('playComputer')))
        #return redirect('/')
    else:
        return render_template('index.html')
    
    
@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
        session.clear()
        return (redirect(url_for('index')))
    else:
        sim = flaskPlay.Simulation(session)
        victory = sim.p1.getVP() > sim.p2.getVP()
        return render_template('result.html', victory = victory)
    
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % (post_id*2)

@app.route('/playComputer', methods=['POST','GET'])
def playComputer():
    if request.method == 'POST':
        if request.form.get('quit'):
            session.clear()
            return redirect(url_for('index'))
        else: 
            if request.form.get('start'):
                sim = flaskPlay.Simulation()
            else:
                sim = flaskPlay.Simulation(session)
                if request.form.get('action'):
                    #sim.p1.updateTreasure()
                    actionCard = request.form.get('action')
                    if actionCard != "None":
                        followup = sim.p1.actionHandler.playerUse(actionCard)
                        if followup:
                            sim.p1.phase = 3
                            session['phase'] = 3
                            session['followup']=followup
                            #return redirect(url_for('playComputer'))
                        else:  
                            sim.p1.discardCard(actionCard)
                    else:
                        sim.p1.updateTreasure()
                        sim.p1.phase = 2
                        
                if request.form.get('buy'):
                    end = sim.p1.playerPurchase(request.form.get('buy'), sim.shop)
                    if end:
                        #sim.p1.cleanupPhase()
                        sim.takeTurn()
                if request.form.get('choice'):
                    followup = sim.p1.actionHandler.playerUse(session['followup']['card'], session['followup']['stage'], request.form.get('choice'))
                    if (followup):
                        session['followup']=followup
                        return redirect(url_for('playComputer'))
                    else:
                        sim.p1.discardCard(session['followup']['card'])
                if request.form.get('skip'):
                    if sim.p1.phase == 1:
                        sim.p1.phase = 2
                        sim.p1.updateTreasure()
                    else:
                        sim.p1.cleanupPhase()
                        #sim.p1.buys = 1
                        sim.takeTurn()
                        #sim.p1.phase = 1
                    
                #sim.makeDecision(sim.p1, 1)
            
            createSession(sim, session)
            #print('before action')
            #print(session)
            #if session.get('cards') and 'Shop' in session.get('cards'):
            #print('finished session: ')
            #print(session)
            if sim.shop.checkEnd():
                return redirect(url_for('result'))
            else:
                return redirect(url_for('playComputer'))
    else:
        print('weights: '+ str(session.get('weights')))
        
        shopCards = None
        actionCards = None
        opponentsCards = None
        if session.get('cards'):
            #print(session['cards']['Shop'])
            sim = flaskPlay.Simulation(session)
            if len(sim.p1.getActions()) == 0 and sim.p1.phase == 1:
                sim.p1.phase = 2
                session['phase']=2
                sim.p1.updateTreasure()
                session['treasure']=sim.p1.treasure # might be cheating fix
                #sim.p1.buys = 1
                #session['buys'] = 1
            if sim.p1.phase == 2:
                #sim.p1.updateTreasure()
                shopCards = sim.p1.buyOptions(sim.shop)
            else:
                actionCards = sim.p1.getActions()
                sim.p1.treasure=0
            opponentsCards = {}
            for card in flaskPlay.Card.options.keys():
                total = int(sim.p2.hand.get(card) or 0) + int(sim.p2.deck.get(card) or 0) + int(sim.p2.discard.get(card) or 0)
                if total > 0:
                    opponentsCards[card] = total
        #print(json.dumps(str(session), sort_keys=True, indent = 4))
        
        return render_template('playing.html', buyOptions = shopCards, actionOptions = actionCards, oppCards = opponentsCards)


def createSession(sim, session):
    state = sim.getBuyState(sim.p1)
    dictionaryKeys = ['Shop', 'Your Hand', 'Your Deck', 'Your Discard', 'ch', 'cde', 'cdi']
    session['cards']={}
    for i in range(len(state)):
        session['cards'][dictionaryKeys[i]] = state[i]
    session['treasure'] = sim.p1.treasure
    session['buys'] = sim.p1.buys
    session['actions'] = sim.p1.actions
    session['phase'] = sim.p1.phase
    return session