"""
Ultra-realistic keyboard input simulation for Camoufox.

This module provides human-like typing simulation with:
- Proper key codes (KeyA, Digit1, Shift+symbols, etc.)
- Typing errors and corrections
- Variable typing speeds
- Natural pauses and hesitations
- Context-aware delays based on character difficulty
"""

import asyncio
import random
from typing import List, Optional

from playwright.async_api import Page


class RealisticKeyboard:
    """Ultra-realistic keyboard input simulator with human-like behavior"""

    def __init__(self, page: Page):
        self.page = page

    async def type_realistically(
        self,
        text: str,
        *,
        typing_delay: int = 120,
        random_delay: bool = True,
        human_mistakes: bool = True,
        thinking_pauses: bool = True,
    ) -> None:
        """
        Type text with ultra-realistic human simulation.

        Args:
            text: Text to type
            typing_delay: Base delay between characters in milliseconds (default: 120)
            random_delay: Enable random variations in typing speed (default: True)
            human_mistakes: Simulate typing errors and corrections (default: True)
            thinking_pauses: Add random pauses as if thinking (default: True)
        """
        words = text.split(' ')

        for word_idx, word in enumerate(words):
            # Pause between words (thinking/reading)
            if word_idx > 0:
                if thinking_pauses:
                    pause_type = random.choices(
                        ['short', 'medium', 'long', 'thinking'],
                        weights=[60, 25, 10, 5]
                    )[0]

                    if pause_type == 'short':
                        await asyncio.sleep(random.uniform(0.05, 0.15))
                    elif pause_type == 'medium':
                        await asyncio.sleep(random.uniform(0.2, 0.5))
                    elif pause_type == 'long':
                        await asyncio.sleep(random.uniform(0.6, 1.2))
                    else:  # thinking
                        await asyncio.sleep(random.uniform(1.0, 2.5))
                else:
                    await asyncio.sleep(random.uniform(0.05, 0.15))

                # Type space
                await self.page.keyboard.press('Space')
                await asyncio.sleep(random.uniform(0.05, 0.12))

            # Type each character in word
            await self._type_word_realistic(
                word, typing_delay, random_delay, human_mistakes
            )

        # Final touches
        await asyncio.sleep(random.uniform(0.1, 0.3))

    async def _type_word_realistic(
        self,
        word: str,
        base_delay: int,
        random_delay: bool,
        human_mistakes: bool,
    ) -> None:
        """Type word with realistic patterns including errors"""
        for char_idx, char in enumerate(word):
            # Simulate typing errors (3% chance)
            if human_mistakes and random_delay and random.random() < 0.03:
                # Type wrong character
                wrong_char = self._get_adjacent_key(char)
                await self._type_single_char(wrong_char, base_delay, random_delay)

                # Realize mistake (reaction time)
                await asyncio.sleep(random.uniform(0.1, 0.5))

                # Correct mistake
                await self.page.keyboard.press('Backspace')
                await asyncio.sleep(random.uniform(0.05, 0.2))

            # Type correct character
            await self._type_single_char(char, base_delay, random_delay)

            # Micro-pauses within words (8% chance)
            if random.random() < 0.08:
                await asyncio.sleep(random.uniform(0.02, 0.08))

    async def _type_single_char(
        self, char: str, base_delay: int, random_delay: bool
    ) -> None:
        """Type single character with realistic timing and key events"""
        # Calculate delay based on character complexity
        if random_delay:
            multiplier = self._get_char_difficulty_multiplier(char)
            delay = base_delay * multiplier * random.uniform(0.7, 1.4)
            delay = max(20, int(delay))
        else:
            delay = base_delay

        # Type character using proper key events
        await self._press_character_key(char)

        # Wait with slight variation
        actual_delay = delay + random.randint(-15, 15)
        await asyncio.sleep(actual_delay / 1000.0)

    def _get_char_difficulty_multiplier(self, char: str) -> float:
        """Get typing difficulty multiplier for character"""
        if char.lower() in 'etaoinshrdlu':  # Home row and common
            return 0.7
        elif char.lower() in 'qzxjkv':  # Difficult keys
            return 1.6
        elif char.isupper():  # Requires Shift
            return 1.3
        elif char.isdigit():  # Number row
            return 1.2
        elif char in '!@#$%^&*()_+{}|:"<>?':  # Shifted symbols
            return 1.8
        elif char in "-=[]\\;',./":  # Unshifted symbols
            return 1.1
        else:
            return 1.0

    def _get_adjacent_key(self, char: str) -> str:
        """Get adjacent key for typing errors"""
        keyboard_layout = {
            'q': 'wa', 'w': 'qesr', 'e': 'wrdt', 'r': 'etfg', 't': 'rygf',
            'y': 'tuhg', 'u': 'yihj', 'i': 'uojk', 'o': 'ipkl', 'p': 'ol',
            'a': 'qsw', 's': 'awedz', 'd': 'serfx', 'f': 'drtgc', 'g': 'ftyhv',
            'h': 'gyujb', 'j': 'huikn', 'k': 'jiolm', 'l': 'kop',
            'z': 'sx', 'x': 'zdc', 'c': 'xfv', 'v': 'cgb', 'b': 'vhn',
            'n': 'bhm', 'm': 'nj'
        }

        adjacent = keyboard_layout.get(char.lower(), 'qwerty')
        return random.choice(adjacent)

    async def _press_character_key(self, char: str) -> None:
        """
        Press character key with proper handling of special keys.

        This is the critical method that uses proper key codes instead of
        just sending the character, which makes the input undetectable.
        """
        if char.isupper():
            # Uppercase letters: hold Shift + press Key
            await self.page.keyboard.down('Shift')
            await asyncio.sleep(random.uniform(0.02, 0.06))
            await self.page.keyboard.press(f'Key{char.upper()}')
            await asyncio.sleep(random.uniform(0.02, 0.06))
            await self.page.keyboard.up('Shift')

        elif char in '!@#$%^&*()':
            # Shifted number symbols
            shift_map = {
                '!': 'Digit1', '@': 'Digit2', '#': 'Digit3', '$': 'Digit4',
                '%': 'Digit5', '^': 'Digit6', '&': 'Digit7', '*': 'Digit8',
                '(': 'Digit9', ')': 'Digit0'
            }
            await self.page.keyboard.down('Shift')
            await asyncio.sleep(random.uniform(0.02, 0.05))
            await self.page.keyboard.press(shift_map[char])
            await asyncio.sleep(random.uniform(0.02, 0.05))
            await self.page.keyboard.up('Shift')

        elif char in '_+{}|:"<>?':
            # Other shifted symbols
            shift_map = {
                '_': 'Minus', '+': 'Equal', '{': 'BracketLeft', '}': 'BracketRight',
                '|': 'Backslash', ':': 'Semicolon', '"': 'Quote', '<': 'Comma',
                '>': 'Period', '?': 'Slash'
            }
            if char in shift_map:
                await self.page.keyboard.down('Shift')
                await asyncio.sleep(random.uniform(0.02, 0.05))
                await self.page.keyboard.press(shift_map[char])
                await asyncio.sleep(random.uniform(0.02, 0.05))
                await self.page.keyboard.up('Shift')
            else:
                # Fallback for unknown characters
                await self.page.keyboard.type(char)

        elif char.isalpha():
            # Lowercase letters
            await self.page.keyboard.press(f'Key{char.upper()}')

        elif char.isdigit():
            # Numbers
            await self.page.keyboard.press(f'Digit{char}')

        else:
            # Other special characters
            special_map = {
                '-': 'Minus', '=': 'Equal', '[': 'BracketLeft', ']': 'BracketRight',
                '\\': 'Backslash', ';': 'Semicolon', "'": 'Quote', ',': 'Comma',
                '.': 'Period', '/': 'Slash', '`': 'Backquote', ' ': 'Space'
            }
            if char in special_map:
                await self.page.keyboard.press(special_map[char])
            else:
                # Ultimate fallback
                await self.page.keyboard.type(char)

    async def clear_field(self, selector: Optional[str] = None) -> None:
        """
        Clear input field using natural human methods.

        Args:
            selector: CSS selector of the field to clear (if None, clears focused field)
        """
        if selector:
            await self.page.click(selector)
            await asyncio.sleep(random.uniform(0.1, 0.3))

        # Choose a random clearing method
        clear_method = random.choice(['ctrl_a', 'triple_click', 'select_all', 'end_shift_home'])

        if clear_method == 'ctrl_a':
            await self._press_key_combo(['Control', 'KeyA'])
        elif clear_method == 'triple_click':
            for _ in range(3):
                await self.page.mouse.click(0, 0)
                await asyncio.sleep(random.uniform(0.05, 0.1))
        elif clear_method == 'end_shift_home':
            await self.page.keyboard.press('End')
            await asyncio.sleep(random.uniform(0.02, 0.05))
            await self._press_key_combo(['Shift', 'Home'])
        else:
            await self._press_key_combo(['Shift', 'Control', 'End'])

        await asyncio.sleep(random.uniform(0.1, 0.2))
        await self.page.keyboard.press('Delete')
        await asyncio.sleep(random.uniform(0.05, 0.15))

    async def _press_key_combo(self, keys: List[str]) -> None:
        """Press key combination with realistic timing"""
        # Press keys down
        for key in keys:
            await self.page.keyboard.down(key)
            await asyncio.sleep(random.uniform(0.01, 0.03))

        await asyncio.sleep(random.uniform(0.02, 0.05))

        # Release keys up (reverse order)
        for key in reversed(keys):
            await self.page.keyboard.up(key)
            await asyncio.sleep(random.uniform(0.01, 0.03))


async def type_realistic(
    page: Page,
    text: str,
    *,
    typing_delay: int = 120,
    random_delay: bool = True,
    human_mistakes: bool = True,
    thinking_pauses: bool = True,
) -> None:
    """
    Convenience function to type text realistically on a page.

    This function provides the same ultra-realistic typing as your main_pr/run.py
    implementation, but integrated directly into Camoufox for easy use.

    Args:
        page: Playwright page object
        text: Text to type
        typing_delay: Base delay between characters in ms (default: 120)
        random_delay: Enable random variations (default: True)
        human_mistakes: Simulate typing errors (default: True)
        thinking_pauses: Add natural pauses (default: True)

    Example:
        async with AsyncCamoufox() as browser:
            page = await browser.new_page()
            await page.goto('https://example.com')
            await page.click('input[name="email"]')
            await type_realistic(page, 'user@example.com')
    """
    keyboard = RealisticKeyboard(page)
    await keyboard.type_realistically(
        text,
        typing_delay=typing_delay,
        random_delay=random_delay,
        human_mistakes=human_mistakes,
        thinking_pauses=thinking_pauses,
    )
