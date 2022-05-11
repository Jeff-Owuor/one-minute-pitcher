import unittest
from app.models import User,Pitch
from app import db

class UserTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the User class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.user_jeff = User(username = 'theDev',password='12345678',email = 'comeon@gmail.com')
        
    def tearDown(self):
        '''
         Method that runs after every test
        '''
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.category,'music')
        self.assertEquals(self.new_pitch.pitch,'Music is food to the soul')
        self.assertEquals(self.new_pitch.user,self.user_jeff)
    