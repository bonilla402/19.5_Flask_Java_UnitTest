import json
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_startGame(self):
        """Test Start Game has blank session and is displaying the socre and timer html"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('maxScore'))
            self.assertIsNone(session.get('playsCount'))
            self.assertIn(b'Highest Score: <b>', response.data)
            self.assertIn(b'Current Score:', response.data)
            self.assertIn(b'Time Left!:', response.data)

    def test_invalidWord(self):
        """Validate a word in the board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["L", "O", "T", "T", "T"], 
                                 ["I", "A", "V", "R", "E"], 
                                 ["P", "E", "T", "E", "A"], 
                                 ["Z", "L", "T", "R", "T"], 
                                 ["U", "Y", "T", "S", "O"]]
                

            response = self.client.post('/ValidateWord', data=json.dumps(dict(word='tea')),
                       content_type='application/json')
            self.assertIn(b'ok' ,response.data)


    def test_NotInBoard(self):
        """Validate an English word in not on the board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["L", "O", "T", "T", "T"], 
                                 ["I", "A", "V", "R", "E"], 
                                 ["P", "E", "T", "E", "A"], 
                                 ["Z", "L", "T", "R", "T"], 
                                 ["U", "Y", "T", "S", "O"]]
                

            response = self.client.post('/ValidateWord', data=json.dumps(dict(word='god')),
                       content_type='application/json')
            
            self.assertEqual(response.json['result'], 'not-on-board')      


    def test_NotWord(self):
        """Validate a word is not in English"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["L", "O", "T", "T", "T"], 
                                 ["I", "A", "V", "R", "E"], 
                                 ["P", "E", "T", "E", "A"], 
                                 ["Z", "L", "T", "R", "T"], 
                                 ["U", "Y", "T", "S", "O"]]
                

            response = self.client.post('/ValidateWord', data=json.dumps(dict(word='sfsfrgrgr')),
                       content_type='application/json')
            
            self.assertEqual(response.json['result'], 'not-word')                     


    def test_finish_Game(self):
        """Validate end game data"""

        with self.client as client:
                
            response = self.client.post('/Finish', data=json.dumps(dict(score=20)),
                       content_type='application/json')
            
            self.assertEqual(response.json['result'], 'OK')        
            self.assertIn('maxScore', session)           
            self.assertEqual(session['maxScore'], 20) 
            self.assertIn('playsCount', session)       
            self.assertGreater(session['playsCount'], 0)