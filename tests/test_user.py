import unittest
from app.models import User,db;

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username = "Jeff_dev", email ="xjeff37@gmail.com", bio = "I am a freak of nature", profile_pic_path = "image_url", password = 'Xavier41!')
        db.session.add(self.new_user)
        db.session.commit()

    def tearDown(self):
        User.query.delete()
        db.session.commit()
 
    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('oscar'))

    def test_save_user(self):
        self.new_user.save_user()
        self.assertTrue(len(User.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_user.username, 'Jeff_dev')
        self.assertEquals(self.new_user.email, 'xjeff37@gmail.com')
        self.assertEquals(self.new_user.bio, 'I am a freak of nature')
        self.assertEquals(self.new_user.profile_pic_path, 'image_url')
        self.assertTrue(self.new_user.verify_password('Xavier41!'))


    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password 
            
if __name__ == '__main':
    unittest.main()            