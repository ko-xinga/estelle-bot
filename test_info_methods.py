import unittest
import info_methods


class TestMakeDict(unittest.TestCase):
    # passes if the dict contains info about the adventurer, Estelle
    def test_adventurer_dict(self):
        testDict = info_methods.make_dict("Estelle")
        self.assertEqual(testDict["entityType"], "adventurer")

    # passes if the dict contains info about the dragon, Leviathan
    def test_dragon_dict(self):
        testDict = info_methods.make_dict("Leviathan")
        self.assertEqual(testDict["entityType"], "dragon")

    # passes if the method throws an AttributeError... handled in driver.py
    def test_neither_dict(self):
        # "EStelele" is not an actual entity
        self.assertRaises(AttributeError, info_methods.make_dict, "EStelele")


class TestGetImage(unittest.TestCase):
    # passes if the method returns a matching url of Estelle
    def test_get_adventurer_image(self):
        correctUrl = "https://gamepedia.cursecdn.com/dragalialost_gamepedia_en/" \
                     "1/10/110063_01_r03.png?version=739e5047fc27b35639c4fc688194e382"
        testUrl = info_methods.get_image("adventurer", "3", "110063", "1")
        self.assertEqual(correctUrl, testUrl)


if __name__ == '__main__':
    unittest.main()
