"""
Django-based tests for Graphical Password Authentication
Uses Django's test client instead of Playwright for more reliable testing
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import GraphicalPassword
from accounts.views import hash_image_sequence
import secrets


class GraphicalPasswordAuthenticationTests(TestCase):
    """Test suite for graphical password authentication"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123'
        }
        self.graphical_password = 'anonymity.png,bitcoin.png,blackcoin.png,block_chain.png'
    
    def test_01_registration_success(self):
        """Test successful user registration with graphical password"""
        print("\n🧪 TEST 1: User Registration - Success")
        
        response = self.client.post('/register', {
            'username': self.test_user_data['username'],
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password'],
            'graphical_password': self.graphical_password
        })
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        
        # User should be created
        user = User.objects.get(username=self.test_user_data['username'])
        self.assertIsNotNone(user)
        
        # Graphical password should be stored
        gp = GraphicalPassword.objects.get(user=user)
        self.assertIsNotNone(gp)
        self.assertEqual(len(gp.salt), 32)  # Salt should be 32 chars (16 bytes in hex)
        self.assertEqual(len(gp.image_sequence_hash), 64)  # SHA-256 hash is 64 chars
        
        print("  ✅ PASSED: User registered successfully with graphical password")
    
    def test_02_registration_no_graphical_password(self):
        """Test registration failure when graphical password is missing"""
        print("\n🧪 TEST 2: Registration - Missing Graphical Password")
        
        response = self.client.post('/register', {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'TestPassword123',
            'graphical_password': ''  # Empty graphical password
        })
        
        # Should stay on registration page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/register', response.url)
        
        # User should NOT be created
        self.assertFalse(User.objects.filter(username='testuser2').exists())
        
        print("  ✅ PASSED: Registration blocked without graphical password")
    
    def test_03_registration_too_few_images(self):
        """Test registration failure with less than 4 images"""
        print("\n🧪 TEST 3: Registration - Too Few Images")
        
        response = self.client.post('/register', {
            'username': 'testuser3',
            'email': 'test3@example.com',
            'password': 'TestPassword123',
            'graphical_password': 'anonymity.png,bitcoin.png'  # Only 2 images
        })
        
        # Should stay on registration page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/register', response.url)
        
        # User should NOT be created
        self.assertFalse(User.objects.filter(username='testuser3').exists())
        
        print("  ✅ PASSED: Registration blocked with less than 4 images")
    
    def test_04_registration_too_many_images(self):
        """Test registration failure with more than 6 images"""
        print("\n🧪 TEST 4: Registration - Too Many Images")
        
        response = self.client.post('/register', {
            'username': 'testuser4',
            'email': 'test4@example.com',
            'password': 'TestPassword123',
            'graphical_password': 'a.png,b.png,c.png,d.png,e.png,f.png,g.png'  # 7 images
        })
        
        # Should stay on registration page
        self.assertEqual(response.status_code, 302)
        
        # User should NOT be created
        self.assertFalse(User.objects.filter(username='testuser4').exists())
        
        print("  ✅ PASSED: Registration blocked with more than 6 images")
    
    def test_05_login_success(self):
        """Test successful login with correct credentials"""
        print("\n🧪 TEST 5: Login - Success with Correct Credentials")
        
        # First create a user
        user = User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password']
        )
        
        # Create graphical password
        salt = secrets.token_hex(16)
        hashed = hash_image_sequence(self.graphical_password, salt)
        GraphicalPassword.objects.create(
            user=user,
            image_sequence_hash=hashed,
            salt=salt
        )
        
        # Try to login
        response = self.client.post('/login', {
            'username': self.test_user_data['username'],
            'password': self.test_user_data['password'],
            'graphical_password': self.graphical_password
        })
        
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        print("  ✅ PASSED: Login successful with correct credentials")
    
    def test_06_login_wrong_graphical_password(self):
        """Test login failure with wrong graphical password"""
        print("\n🧪 TEST 6: Login - Wrong Graphical Password")
        
        # Create user with specific graphical password
        user = User.objects.create_user(
            username='logintest1',
            password='TestPassword123'
        )
        
        salt = secrets.token_hex(16)
        correct_gp = 'anonymity.png,bitcoin.png,blackcoin.png,block_chain.png'
        hashed = hash_image_sequence(correct_gp, salt)
        GraphicalPassword.objects.create(user=user, image_sequence_hash=hashed, salt=salt)
        
        # Try to login with wrong graphical password
        wrong_gp = 'centralized.png,conversion.png,decryption.png,dogecoin.png'
        response = self.client.post('/login', {
            'username': 'logintest1',
            'password': 'TestPassword123',
            'graphical_password': wrong_gp
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        
        print("  ✅ PASSED: Login blocked with wrong graphical password")
    
    def test_07_login_wrong_order(self):
        """Test login failure with right images but wrong order"""
        print("\n🧪 TEST 7: Login - Correct Images, Wrong Order")
        
        # Create user
        user = User.objects.create_user(
            username='logintest2',
            password='TestPassword123'
        )
        
        salt = secrets.token_hex(16)
        correct_gp = 'anonymity.png,bitcoin.png,blackcoin.png,block_chain.png'
        hashed = hash_image_sequence(correct_gp, salt)
        GraphicalPassword.objects.create(user=user, image_sequence_hash=hashed, salt=salt)
        
        # Try with reversed order
        reversed_gp = 'block_chain.png,blackcoin.png,bitcoin.png,anonymity.png'
        response = self.client.post('/login', {
            'username': 'logintest2',
            'password': 'TestPassword123',
            'graphical_password': reversed_gp
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        
        print("  ✅ PASSED: Order matters - login blocked")
    
    def test_08_login_wrong_text_password(self):
        """Test login failure with wrong text password"""
        print("\n🧪 TEST 8: Login - Wrong Text Password")
        
        # Create user
        user = User.objects.create_user(
            username='logintest3',
            password='CorrectPassword123'
        )
        
        salt = secrets.token_hex(16)
        hashed = hash_image_sequence(self.graphical_password, salt)
        GraphicalPassword.objects.create(user=user, image_sequence_hash=hashed, salt=salt)
        
        # Try with wrong text password
        response = self.client.post('/login', {
            'username': 'logintest3',
            'password': 'WrongPassword123',
            'graphical_password': self.graphical_password
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        
        print("  ✅ PASSED: Login blocked with wrong text password")
    
    def test_09_password_hashing_security(self):
        """Test that same graphical password for different users produces different hashes"""
        print("\n🧪 TEST 9: Security - Password Hashing with Different Salts")
        
        # Create two users with same graphical password
        user1 = User.objects.create_user(username='user1', password='pass123')
        user2 = User.objects.create_user(username='user2', password='pass123')
        
        same_gp = 'anonymity.png,bitcoin.png,blackcoin.png,block_chain.png'
        
        salt1 = secrets.token_hex(16)
        salt2 = secrets.token_hex(16)
        
        hash1 = hash_image_sequence(same_gp, salt1)
        hash2 = hash_image_sequence(same_gp, salt2)
        
        GraphicalPassword.objects.create(user=user1, image_sequence_hash=hash1, salt=salt1)
        GraphicalPassword.objects.create(user=user2, image_sequence_hash=hash2, salt=salt2)
        
        # Salts should be different
        self.assertNotEqual(salt1, salt2)
        
        # Hashes should be different (due to different salts)
        self.assertNotEqual(hash1, hash2)
        
        print("  ✅ PASSED: Different salts produce different hashes for same password")
    
    def test_10_duplicate_username(self):
        """Test that duplicate usernames are rejected"""
        print("\n🧪 TEST 10: Registration - Duplicate Username")
        
        # Create first user
        User.objects.create_user(username='duplicate', email='first@example.com', password='pass123')
        
        # Try to create second user with same username
        response = self.client.post('/register', {
            'username': 'duplicate',
            'email': 'second@example.com',
            'password': 'pass456',
            'graphical_password': self.graphical_password
        })
        
        # Should stay on registration page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/register', response.url)
        
        # Should only have 1 user with that username
        self.assertEqual(User.objects.filter(username='duplicate').count(), 1)
        
        print("  ✅ PASSED: Duplicate username rejected")


def run_tests():
    """Run all tests and print summary"""
    from django.test.runner import DiscoverRunner
    
    print("\n" + "="*80)
    print("🚀 GRAPHICAL PASSWORD AUTHENTICATION - AUTOMATED TEST SUITE")
    print("="*80 + "\n")
    
    runner = DiscoverRunner(verbosity=2, interactive=False, keepdb=False)
    failures = runner.run_tests(['accounts'])
    
    print("\n" + "="*80)
    if failures == 0:
        print("🎉 ALL TESTS PASSED - Graphical Password System is Working Perfectly!")
    else:
        print(f"⚠️  {failures} TEST(S) FAILED")
    print("="*80 + "\n")
    
    return failures == 0
