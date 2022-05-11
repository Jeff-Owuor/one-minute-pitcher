import unittest
from app.models import User

class UserTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the User class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_user = User(1234,'Jeff_Dev','xjeff37@gmail.com',2,'Live,laugh and love',"https://www.image.com","23432kja")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_user,User))