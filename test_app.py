import unittest 
from unittest import TestCase
from flask import Flask, session
from boggle import Boggle

# Import the Flask app instance from your app.py file
from app import app

class BoggleAppTestCase(TestCase):

    def test_display_board(self):
        with self.app as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'board' in session)

    def test_check_guess(self):
        with self.app as client:
            # Set up a board with known letters
            session['board'] = [['A', 'B', 'C', 'D', 'E'],
                               ['F', 'G', 'H', 'I', 'J'],
                               ['K', 'L', 'M', 'N', 'O'],
                               ['P', 'Q', 'R', 'S', 'T'],
                               ['U', 'V', 'W', 'X', 'Y']]

            # Test a valid guess on the board
            response = client.post('/check_guess', json={'guess': 'DOG'})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['result'], 'ok')
            self.assertEqual(data['message'], 'Valid word on the board!')

            # Test a valid guess not on the board
            response = client.post('/check_guess', json={'guess': 'TOY'})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['result'], 'not-on-board')
            self.assertEqual(data['message'], 'Valid word, but not on the board.')

            # Test an invalid guess
            response = client.post('/check_guess', json={'guess': 'XYZ'})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['result'], 'not-a-word')
            self.assertEqual(data['message'], 'Not a valid word.')

    def test_reset_board(self):
        with self.app as client:
            response = client.get('/reset_board')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'board' in session)
            self.assertNotEqual(data['board'], session['board'])

    def test_update_score(self):
        with self.app as client:
            # Initial values
            game_count = 0
            high_score = 0

            # Test updating the score
            response = client.post('/update_score', json={'score': 10})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['game_count'], 1)
            self.assertEqual(data['high_score'], 10)

            # Test updating the score with a lower score
            response = client.post('/update_score', json={'score': 5})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['game_count'], 2)
            self.assertEqual(data['high_score'], 10)
