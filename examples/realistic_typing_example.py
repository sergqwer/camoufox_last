"""
Example: Ultra-realistic keyboard input with Camoufox

This example demonstrates how to use the built-in realistic typing
functionality that mimics human typing behavior perfectly.
"""

import asyncio
from camoufox import AsyncCamoufox, type_realistic, RealisticKeyboard


async def example_simple_typing():
    """Simple example using the convenience function"""
    print("Example 1: Simple realistic typing")

    async with AsyncCamoufox(headless=False) as browser:
        page = await browser.new_page()
        await page.goto('https://www.google.com')

        # Wait for search input
        await page.wait_for_selector('textarea[name="q"]')
        await page.click('textarea[name="q"]')

        # Type realistically - this will look completely human!
        print("Typing search query...")
        await type_realistic(page, 'ultra realistic browser automation')

        await asyncio.sleep(2)
        print("Done!")


async def example_custom_settings():
    """Example with custom typing settings"""
    print("\nExample 2: Custom typing settings")

    async with AsyncCamoufox(headless=False) as browser:
        page = await browser.new_page()
        await page.goto('https://www.google.com')

        await page.wait_for_selector('textarea[name="q"]')
        await page.click('textarea[name="q"]')

        # Fast typing, no mistakes
        print("Fast typing without mistakes...")
        await type_realistic(
            page,
            'fast typing test',
            typing_delay=50,  # Faster typing
            human_mistakes=False,  # No typing errors
            thinking_pauses=False,  # No pauses
        )

        await asyncio.sleep(2)
        print("Done!")


async def example_keyboard_class():
    """Example using RealisticKeyboard class for more control"""
    print("\nExample 3: Using RealisticKeyboard class")

    async with AsyncCamoufox(headless=False) as browser:
        page = await browser.new_page()
        await page.goto('https://www.google.com')

        # Create keyboard instance
        keyboard = RealisticKeyboard(page)

        await page.wait_for_selector('textarea[name="q"]')
        await page.click('textarea[name="q"]')

        # Type with full realism
        print("Typing with full human simulation...")
        await keyboard.type_realistically(
            'realistic typing with errors',
            typing_delay=120,
            random_delay=True,
            human_mistakes=True,
            thinking_pauses=True,
        )

        await asyncio.sleep(1)

        # Clear the field naturally
        print("Clearing field...")
        await keyboard.clear_field()

        await asyncio.sleep(1)

        # Type again
        print("Typing again...")
        await keyboard.type_realistically('corrected text')

        await asyncio.sleep(2)
        print("Done!")


async def example_form_filling():
    """Example: Filling a form realistically"""
    print("\nExample 4: Realistic form filling")

    async with AsyncCamoufox(headless=False) as browser:
        page = await browser.new_page()

        # Create a test form
        await page.set_content("""
        <html>
        <body style="font-family: Arial; padding: 50px;">
            <h1>Registration Form</h1>
            <form>
                <div style="margin: 10px 0;">
                    <label>Name: <input type="text" id="name" /></label>
                </div>
                <div style="margin: 10px 0;">
                    <label>Email: <input type="email" id="email" /></label>
                </div>
                <div style="margin: 10px 0;">
                    <label>Password: <input type="password" id="password" /></label>
                </div>
                <div style="margin: 10px 0;">
                    <label>Message: <textarea id="message" rows="4" cols="50"></textarea></label>
                </div>
            </form>
        </body>
        </html>
        """)

        print("Filling form realistically...")

        # Fill name
        await page.click('#name')
        await type_realistic(page, 'John Doe')
        await asyncio.sleep(0.5)

        # Fill email
        await page.click('#email')
        await type_realistic(page, 'john.doe@example.com')
        await asyncio.sleep(0.5)

        # Fill password with slower, more careful typing
        await page.click('#password')
        await type_realistic(
            page,
            'MySecureP@ssw0rd!',
            typing_delay=150,  # Slower for password
            human_mistakes=False,  # No mistakes in password
        )
        await asyncio.sleep(0.5)

        # Fill message
        await page.click('#message')
        await type_realistic(
            page,
            'This is a test message typed with ultra-realistic human simulation. '
            'Notice the natural pauses and variable typing speed!'
        )

        await asyncio.sleep(3)
        print("Form filled!")


async def main():
    """Run all examples"""
    print("=" * 60)
    print("Camoufox Ultra-Realistic Typing Examples")
    print("=" * 60)

    # Run examples
    await example_simple_typing()
    await example_custom_settings()
    await example_keyboard_class()
    await example_form_filling()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
