"""
Automated tests for the Graphical Password Authentication System
Tests registration, login, and validation using Playwright
"""

import time
from playwright.sync_api import sync_playwright, expect

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_USER = {
    "username": "testuser_auto",
    "email": "testuser_auto@example.com",
    "password": "TestPassword123"
}

# Images to select for graphical password (first 4 images)
GRAPHICAL_PASSWORD_IMAGES = [
    "anonymity.png",
    "bitcoin.png",
    "blackcoin.png",
    "block_chain.png"
]


def test_registration_success():
    """Test successful user registration with graphical password"""
    print("\n🧪 TEST 1: Registration with valid graphical password")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to registration page
        page.goto(f"{BASE_URL}/register")
        print("  ✓ Navigated to registration page")
        
        # Fill in text fields
        page.fill('input[name="username"]', TEST_USER["username"])
        page.fill('input[name="email"]', TEST_USER["email"])
        page.fill('input[name="password"]', TEST_USER["password"])
        print("  ✓ Filled registration form")
        
        # Select graphical password images
        for image_name in GRAPHICAL_PASSWORD_IMAGES:
            page.click(f'img[alt="{image_name}"]')
            time.sleep(0.2)  # Small delay for visual feedback
        
        print(f"  ✓ Selected {len(GRAPHICAL_PASSWORD_IMAGES)} images")
        
        # Verify selection count
        count_text = page.text_content('#selectionCount')
        assert count_text == str(len(GRAPHICAL_PASSWORD_IMAGES)), \
            f"Expected {len(GRAPHICAL_PASSWORD_IMAGES)} selections, got {count_text}"
        print(f"  ✓ Selection count verified: {count_text}")
        
        # Submit form
        page.click('button[type="submit"]')
        page.wait_for_url(f"{BASE_URL}/login", timeout=5000)
        print("  ✓ Redirected to login page after successful registration")
        
        # Check for success message (might be on login page after redirect)
        # The page should have redirected to login
        assert "/login" in page.url, "Should redirect to login page"
        
        browser.close()
        print("  ✅ TEST PASSED: Registration successful\n")
        return True


def test_registration_too_few_images():
    """Test registration validation - too few images selected"""
    print("🧪 TEST 2: Registration with too few images")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(f"{BASE_URL}/register")
        
        # Fill in text fields
        page.fill('input[name="username"]', "testuser_few")
        page.fill('input[name="email"]', "testfew@example.com")
        page.fill('input[name="password"]', "TestPass123")
        
        # Select only 2 images (less than minimum of 4)
        page.click(f'img[alt="anonymity.png"]')
        page.click(f'img[alt="bitcoin.png"]')
        time.sleep(0.3)
        
        # Try to submit - should be blocked by JavaScript validation
        page.on("dialog", lambda dialog: dialog.accept())
        page.click('button[type="submit"]')
        time.sleep(0.5)
        
        # Should still be on registration page
        assert "/register" in page.url, "Should stay on registration page"
        print("  ✓ Form submission blocked for insufficient images")
        
        browser.close()
        print("  ✅ TEST PASSED: Validation works for too few images\n")
        return True


def test_login_success():
    """Test successful login with correct credentials"""
    print("🧪 TEST 3: Login with correct credentials")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to login page
        page.goto(f"{BASE_URL}/login")
        print("  ✓ Navigated to login page")
        
        # Fill in credentials
        page.fill('input[name="username"]', TEST_USER["username"])
        page.fill('input[name="password"]', TEST_USER["password"])
        print("  ✓ Filled login form")
        
        # Select SAME graphical password images in SAME order
        for image_name in GRAPHICAL_PASSWORD_IMAGES:
            page.click(f'img[alt="{image_name}"]')
            time.sleep(0.2)
        
        print(f"  ✓ Selected {len(GRAPHICAL_PASSWORD_IMAGES)} images in same order")
        
        # Submit login
        page.click('button[type="submit"]')
        time.sleep(1)
        
        # Should redirect to home page
        page.wait_for_url(f"{BASE_URL}/", timeout=5000)
        print("  ✓ Redirected to home page after successful login")
        
        browser.close()
        print("  ✅ TEST PASSED: Login successful with correct credentials\n")
        return True


def test_login_wrong_graphical_password():
    """Test login failure with wrong graphical password"""
    print("🧪 TEST 4: Login with wrong graphical password")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(f"{BASE_URL}/login")
        
        # Fill in correct text credentials
        page.fill('input[name="username"]', TEST_USER["username"])
        page.fill('input[name="password"]', TEST_USER["password"])
        
        # Select DIFFERENT images (wrong graphical password)
        wrong_images = ["centralized.png", "conversion.png", "decryption.png", "dogecoin.png"]
        for image_name in wrong_images:
            page.click(f'img[alt="{image_name}"]')
            time.sleep(0.2)
        
        print("  ✓ Selected wrong graphical password images")
        
        # Submit login
        page.click('button[type="submit"]')
        time.sleep(1)
        
        # Should stay on login page with error
        assert "/login" in page.url, "Should stay on login page after failed login"
        print("  ✓ Stayed on login page (login rejected)")
        
        # Check for error message
        page_content = page.content()
        assert "Invalid graphical password" in page_content or "Invalid" in page_content, \
            "Should show error message"
        print("  ✓ Error message displayed")
        
        browser.close()
        print("  ✅ TEST PASSED: Login failed with wrong graphical password\n")
        return True


def test_login_wrong_order():
    """Test login failure with right images but wrong order"""
    print("🧪 TEST 5: Login with correct images but wrong order")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(f"{BASE_URL}/login")
        
        # Fill in correct text credentials
        page.fill('input[name="username"]', TEST_USER["username"])
        page.fill('input[name="password"]', TEST_USER["password"])
        
        # Select SAME images but in REVERSE order
        reversed_images = list(reversed(GRAPHICAL_PASSWORD_IMAGES))
        for image_name in reversed_images:
            page.click(f'img[alt="{image_name}"]')
            time.sleep(0.2)
        
        print("  ✓ Selected images in wrong order")
        
        # Submit login
        page.click('button[type="submit"]')
        time.sleep(1)
        
        # Should stay on login page
        assert "/login" in page.url, "Should stay on login page"
        print("  ✓ Login rejected for wrong order")
        
        browser.close()
        print("  ✅ TEST PASSED: Order matters for graphical password\n")
        return True


def test_login_wrong_text_password():
    """Test login failure with wrong text password"""
    print("🧪 TEST 6: Login with wrong text password")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(f"{BASE_URL}/login")
        
        # Fill in WRONG text password
        page.fill('input[name="username"]', TEST_USER["username"])
        page.fill('input[name="password"]', "WrongPassword123")
        
        # Select correct graphical password
        for image_name in GRAPHICAL_PASSWORD_IMAGES:
            page.click(f'img[alt="{image_name}"]')
            time.sleep(0.2)
        
        print("  ✓ Entered wrong text password with correct graphical password")
        
        # Submit login
        page.click('button[type="submit"]')
        time.sleep(1)
        
        # Should stay on login page
        assert "/login" in page.url, "Should stay on login page"
        print("  ✓ Login rejected for wrong text password")
        
        browser.close()
        print("  ✅ TEST PASSED: Text password validation works\n")
        return True


def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*70)
    print("🚀 GRAPHICAL PASSWORD AUTHENTICATION - AUTOMATED TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        ("Registration Success", test_registration_success),
        ("Registration Validation", test_registration_too_few_images),
        ("Login Success", test_login_success),
        ("Wrong Graphical Password", test_login_wrong_graphical_password),
        ("Wrong Image Order", test_login_wrong_order),
        ("Wrong Text Password", test_login_wrong_text_password),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASSED", None))
        except Exception as e:
            results.append((test_name, "FAILED", str(e)))
            print(f"  ❌ TEST FAILED: {test_name}")
            print(f"     Error: {e}\n")
    
    # Print summary
    print("="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, status, _ in results if status == "PASSED")
    failed = sum(1 for _, status, _ in results if status == "FAILED")
    
    for test_name, status, error in results:
        icon = "✅" if status == "PASSED" else "❌"
        print(f"{icon} {test_name}: {status}")
        if error:
            print(f"   Error: {error}")
    
    print("\n" + "="*70)
    print(f"Total: {len(results)} tests | Passed: {passed} | Failed: {failed}")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Make sure Django server is running on http://127.0.0.1:8000")
    print("   Run: python manage.py runserver\n")
    
    input("Press Enter to start tests...")
    
    success = run_all_tests()
    
    if success:
        print("🎉 All tests passed! The graphical password system is working perfectly.\n")
    else:
        print("⚠️  Some tests failed. Please review the errors above.\n")
